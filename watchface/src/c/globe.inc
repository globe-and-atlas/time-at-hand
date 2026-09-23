/* Included by face.c so host fixtures and Pebble compile the same renderer.
 * NOAA fractional-year solar approximation; all solar inputs are UTC.
 * Projection cache: 2 bits per display pixel, refreshed only on location change. */
#include <math.h>
#include "land.h"
#define EARTH_PI 3.14159265358979323846f
#define EARTH_RAD (EARTH_PI/180.0f)
static uint8_t earth_cache[(FACE_W*FACE_H+3)/4];
static int earth_last_lat=99999,earth_last_lon=99999;
static float earth_slat,earth_clat,earth_slon,earth_clon;
/* Range-reduced atan2 without newlib's indexed constant tables. Those tables
 * produced invalid longitudes in the relocatable Pebble binary. Error below
 * 1e-6 radians is negligible beside the one-degree land mask. */
static float earth_atan2(float y,float x) {
 float ax=fabsf(x),ay=fabsf(y);
 if(ax==0 && ay==0) return 0;
 float r=ay>ax ? ax/ay : ay/ax,offset=0;
 if(r>0.41421356237f) {r=(r-1)/(r+1);offset=EARTH_PI/4;}
 float q=r*r;
 float angle=offset+r*(1+q*(-1.0f/3+q*(1.0f/5+q*(-1.0f/7+q*(1.0f/9+q*(-1.0f/11+q*(1.0f/13+q*(-1.0f/15+q/17))))))));
 if(ay>ax) angle=EARTH_PI/2-angle;
 if(x<0) angle=EARTH_PI-angle;
 return y<0 ? -angle : angle;
}

void face_sun(int year,int doy,int utc_minute,float *declination,float *longitude) {
 int leap=year%4==0 && (year%100!=0 || year%400==0);
 float g=2*EARTH_PI/(365+leap)*(doy-1+(utc_minute/60.0f-12)/24);
 float eq=229.18f*(0.000075f+0.001868f*cosf(g)-0.032077f*sinf(g)-0.014615f*cosf(2*g)-0.040849f*sinf(2*g));
 *declination=0.006918f-0.399912f*cosf(g)+0.070257f*sinf(g)-0.006758f*cosf(2*g)+0.000907f*sinf(2*g)-0.002697f*cosf(3*g)+0.00148f*sinf(3*g);
 *longitude=(180-(utc_minute+eq)/4)*EARTH_RAD;
}
static void earth_project(int lat,int lon) {
 if(lat==earth_last_lat && lon==earth_last_lon) return;
 earth_last_lat=lat;earth_last_lon=lon;
 earth_slat=sinf(lat*0.01f*EARTH_RAD);earth_clat=cosf(lat*0.01f*EARTH_RAD);
 earth_slon=sinf(lon*0.01f*EARTH_RAD);earth_clon=cosf(lon*0.01f*EARTH_RAD);
 memset(earth_cache,0,sizeof(earth_cache));
 for(int y=38;y<=190;++y) for(int x=24;x<=176;++x) {
  float e=(x-100)/76.0f,n=(114-y)/76.0f,rr=e*e+n*n;
  if(rr>1) continue;
  float z=sqrtf(1-rr);
  float zz=n*earth_clat+z*earth_slat;
  float north=asinf(fmaxf(-1,fminf(1,zz)))/EARTH_RAD;
  float east=earth_atan2(e,z*earth_clat-n*earth_slat)/EARTH_RAD+lon*0.01f;
  if(east>=180) east-=360;
  if(east< -180) east+=360;
  if(!isfinite(east) || !isfinite(north) || east< -180 || east>180) continue;
  int mx=(int)(east+180),my=(int)(90-north);
  if(mx>359) mx=359;
  if(my>179) my=179;
  if(my<0) my=0;
  int mi=my*360+mx,land=(earth_land[mi/8]>>(mi%8))&1;
  /* Thin dotted 30-degree meridians and parallels. */
  float a=fabsf(remainderf(north,30)),b=fabsf(remainderf(east,30));
  int grid=(a<0.5f || b<0.5f) && ((x+y)%3==0);
  int i=y*FACE_W+x;
  earth_cache[i/4]|=(land|(grid<<1))<<((i%4)*2);
 }
}
/* Glyph-shaped clearance: no globe within (numeral scale) pixels of a stroke,
 * so numbers stay legible without a rectangular hole in the globe. */
static int halo_near(const FaceNumber *labels,int x,int y) {
 for(int j=0;j<2;++j) {
  const FaceNumber *n=&labels[j];
  const int r=n->scale;
  if(x<n->x-r || x>=n->x+n->width+r || y<n->y-r || y>=n->y+n->height+r) continue;
  for(int dy=-r;dy<=r;++dy) for(int dx=-r;dx<=r;++dx) {
   if(dx*dx+dy*dy>r*r+1) continue;
   if(ink(n->text,x+dx-n->x,y+dy-n->y,n->scale)) return 1;
  }
 }
 return 0;
}
void face_globe_overlay(int h,int m,int utc_year,int doy,int utc_minute,
                        int latitude,int longitude,int marker,uint8_t *pixels) {
 if(latitude< -9000 || latitude>9000 || longitude< -18000 || longitude>18000) return;
 earth_project(latitude,longitude);
 float dec,lon;face_sun(utc_year,doy,utc_minute,&dec,&lon);
 float sx=cosf(dec)*cosf(lon),sy=cosf(dec)*sinf(lon),sz=sinf(dec);
 float sun_e=-sx*earth_slon+sy*earth_clon;
 float sun_n=-sx*earth_slat*earth_clon-sy*earth_slat*earth_slon+sz*earth_clat;
 float sun_z=sx*earth_clat*earth_clon+sy*earth_clat*earth_slon+sz*earth_slat;
 FaceNumber labels[2];face_split_layout(h,m,labels);
 for(int y=37;y<=191;++y) for(int x=23;x<=177;++x) {
  int i=y*FACE_W+x;if(pixels[i]) continue;
  if(halo_near(labels,x,y)) continue;
  float e=(x-100)/76.0f,n=(114-y)/76.0f,rr=e*e+n*n;
  if(rr>1.025f) continue;
  if(rr>=0.985f) {pixels[i]=7;continue;}
  int value=(earth_cache[i/4]>>((i%4)*2))&3;
  float light=e*sun_e+n*sun_n+sqrtf(1-rr)*sun_z;
  /* Land is gray; the dotted graticule is gray over sea and white over land. */
  uint8_t c=(value&1) ? 9 : 0;
  if(value&2) c=(value&1) ? 0 : 9;
  /* Night is visibly textured; land retains a darker silhouette. */
  if(light<0 && ((x+y)&1)==0) c=(value&1) ? 7 : 9;
  if(marker && (x-100)*(x-100)+(y-114)*(y-114)>=30 && (x-100)*(x-100)+(y-114)*(y-114)<=42) c=8;
  pixels[i]=c;
 }
}
