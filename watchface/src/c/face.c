#include "face.h"
#include <stdio.h>
#include <string.h>
#include "trig.h"
#include "fonts.h"
/* White, black, amber, red, blue, green, purple, gray, teal; native 2-bit channels. */
const uint8_t face_palette[FACE_PALETTE_SIZE][3]={
 {255,255,255},{0,0,0},{255,170,0},{170,0,0},{0,0,170},
 {0,85,0},{85,0,170},{85,85,85},{0,85,85},{170,170,170},
/* Fragments of this file use .h names because CloudPebble imports only .c/.h sources. */
#include "face_colors.h"
};
static int hour_radius=48;
static int active_font=0,primary_color=2,secondary_color=2,primary_width=1,secondary_width=1;
static int hour_label_scale=3,minute_label_scale=2,show_ticks=0;
static int stroke_ink(float across,int width) {
 /* Negative values preserve the original optical weights. Explicit pixel
  * widths use a half-open span so even widths remain distinct on axis. */
 if(width<0) {float half=width==-3 ? 1.1f : 0.6f;return across>=-half && across<half;}
 return across>=-width*0.5f && across<width*0.5f;
}
static const uint8_t glyphs[11][7] = {
 {14,17,19,21,25,17,14}, {4,12,4,4,4,4,14},
 {14,17,1,2,4,8,31}, {30,1,1,14,1,1,30},
 {2,6,10,18,31,2,2}, {31,16,16,30,1,1,30},
 {14,16,16,30,17,17,14}, {31,1,2,4,8,8,8},
 {14,17,17,14,17,17,14}, {14,17,17,15,1,1,14},
 {0,0,4,0,4,0,0}
};
int face_special(int h, int m) { return m == 0 && h % 3 == 0; }
/* Half-degree units clockwise from top. */
int face_angle(int h, int m) { return (h % 12) * 60 + m; }
void face_label(int h, int m, char *out) {
 int hour=h%12; if (!hour) hour=12;
 if (face_special(h,m)) snprintf(out,6,"%d",hour);
 else snprintf(out,6,"%d:%02d",hour,m);
}
static int ink(const char *s,int x,int y,int scale) {
 if(x<0 || y<0 || y>=7*scale) return 0;
 int cell=x/(6*scale), col=(x/scale)%6;
 if(cell>=(int)strlen(s) || col>=5) return 0;
 int g=s[cell]==':' ? 10 : s[cell]-'0';
 return ((g==10 ? glyphs[10][y/scale] : numeral_fonts[active_font][g][y/scale])>>(4-col))&1;
}
static int nearest(float v) { return (int)(v>=0 ? v+0.5f : v-0.5f); }
static int label_scale(int setting,int fallback) {
 /* 0 keeps the optical default; 1/2/3 are compact, medium and large. */
 return setting>=1 && setting<=3 ? setting+1 : fallback;
}
static int clamp_label_start(int value,int width) {
 if(value<3) return 3;
 if(value+width>FACE_W-3) return FACE_W-3-width;
 return value;
}
static void render_original(int h,int m,uint8_t *pixels) {
 char label[6]; face_label(h,m,label);
 int step=face_angle(h,m);
 /* Shared lookup ensures preview and device use identical direction values. */
 float dx=(float)face_sine[step]/16384;
 float dy=-(float)face_sine[(step+180)%720]/16384;
 memset(pixels,0,FACE_W*FACE_H);
 if(face_special(h,m)) {
  int scale=hour_label_scale==3 ? 4 : hour_label_scale;
  int width=((int)strlen(label)*6-1)*scale;
  int left=clamp_label_start(nearest(100+73*dx)-width/2,width), top=nearest(114+78*dy)-7*scale/2;
  for(int y=0;y<FACE_H;++y) for(int x=0;x<FACE_W;++x)
   if(ink(label,x-left,y-top,scale)) pixels[y*FACE_W+x]=1;
  return;
 }
 int scale=hour_label_scale;
 int width=((int)strlen(label)*6-1)*scale, flip=step>360;
 for(int y=0;y<FACE_H;++y) for(int x=0;x<FACE_W;++x) {
  float xx=x-100, yy=y-114;
  float radial=xx*dx+yy*dy, lateral=xx*(-dy)+yy*dx;
  uint8_t c=0;
  if(radial>=5 && radial<=86 && stroke_ink(lateral,primary_width)) c=primary_color;
  if(radial>=84 && radial<=88 && lateral>=-2 && lateral<=2) c=primary_color;
  float tx=radial-46,ty=lateral;
  if(flip) {tx=-tx;ty=-ty;}
  if(ink(label,nearest(tx+width/2.0f),nearest(ty+8*scale),scale)) c=1;
  if(xx*xx+yy*yy<=9) c=1;
  pixels[y*FACE_W+x]=c;
 }
}

int face_minute_angle(int minute) { return minute*12; }

static void split_layout_radius_scaled(int h,int m,FaceNumber *labels,int radius,int hour_scale,int minute_scale) {
 int steps[2]={face_angle(h,m),face_minute_angle(m)};
 /* Distinct tracks keep labels separate even when hands align at noon. */
 int radii[2]={radius,82};
 snprintf(labels[0].text,3,"%d",h%12 ? h%12 : 12);
 snprintf(labels[1].text,3,"%02d",m);
 for(int i=0;i<2;++i) {
  FaceNumber *n=&labels[i];
  n->scale=i==0 ? hour_scale : minute_scale;
  n->width=((int)strlen(n->text)*6-1)*n->scale;
  n->height=7*n->scale;
  float dx=(float)face_sine[steps[i]]/16384;
  float dy=-(float)face_sine[(steps[i]+180)%720]/16384;
  n->x=clamp_label_start(nearest(100+radii[i]*dx)-n->width/2,n->width);
  n->y=nearest(114+radii[i]*dy)-n->height/2;
 }
}
static void split_layout_radius(int h,int m,FaceNumber *labels,int radius) {
 split_layout_radius_scaled(h,m,labels,radius,3,2);
}

void face_split_layout(int h,int m,FaceNumber *labels) {
 split_layout_radius(h,m,labels,48);
}

static void render_split(int h,int m,uint8_t *pixels) {
 FaceNumber labels[2];split_layout_radius_scaled(h,m,labels,hour_radius,hour_label_scale,minute_label_scale);
 int steps[2]={face_angle(h,m),face_minute_angle(m)};
 float dx[2],dy[2];
 for(int i=0;i<2;++i) {
  dx[i]=(float)face_sine[steps[i]]/16384;
  dy[i]=-(float)face_sine[(steps[i]+180)%720]/16384;
 }
 for(int y=0;y<FACE_H;++y) for(int x=0;x<FACE_W;++x) {
  float xx=x-100,yy=y-114;uint8_t c=0;
  for(int i=1;i>=0;--i) {
   float along=xx*dx[i]+yy*dy[i],across=xx*(-dy[i])+yy*dx[i];
   if(along>=0 && along<=(i==0 ? hour_radius : 82) && stroke_ink(across,i==0 ? primary_width : secondary_width)) c=i==0 ? primary_color : secondary_color;
  }
  /* White clearance prevents either hand crossing either number. */
  for(int i=0;i<2;++i) {
   FaceNumber *n=&labels[i];
   if(x>=n->x-2 && x<n->x+n->width+2 && y>=n->y-2 && y<n->y+n->height+2) c=0;
  }
  for(int i=0;i<2;++i)
   if(ink(labels[i].text,x-labels[i].x,y-labels[i].y,labels[i].scale)) c=1;
  if(xx*xx+yy*yy<=9) c=1;
  pixels[y*FACE_W+x]=c;
 }
}

static void set_style(int edition,int font,int color,int minute_color,int width,int minute_width) {
 hour_radius=48;
 active_font=font>=0 && font<12 ? font : 0;
 primary_color=color>=1 && color<FACE_PALETTE_SIZE ? color : (edition ? 1 : 2);
 secondary_color=minute_color>=1 && minute_color<FACE_PALETTE_SIZE ? minute_color : (edition==3 ? 1 : edition==4 ? 46 : 2);
 primary_width=width>=1 && width<=8 ? width : (edition==4 ? 4 : edition==3 ? 1 : edition ? -3 : -1);
 secondary_width=minute_width>=1 && minute_width<=8 ? minute_width : (edition==4 ? 2 : edition==3 ? 1 : -1);
}
void face_render(int h,int m,uint8_t *pixels) {
 set_style(0,0,-1,-1,0,0);render_original(h,m,pixels);
}
void face_render_split(int h,int m,uint8_t *pixels) {
 set_style(1,0,-1,-1,0,0);render_split(h,m,pixels);
}

static const uint8_t letters[26][7]={
 {14,17,17,31,17,17,17},{30,17,17,30,17,17,30},
 {14,17,16,16,16,17,14},{30,17,17,17,17,17,30},
 {31,16,16,30,16,16,31},{31,16,16,30,16,16,16},
 {14,17,16,23,17,17,15},{17,17,17,31,17,17,17},
 {14,4,4,4,4,4,14},{7,2,2,2,18,18,12},
 {17,18,20,24,20,18,17},{16,16,16,16,16,16,31},
 {17,27,21,21,17,17,17},{17,25,21,19,17,17,17},
 {14,17,17,17,17,17,14},{30,17,17,30,16,16,16},
 {14,17,17,17,21,18,13},{30,17,17,30,20,18,17},
 {15,16,16,14,1,1,30},{31,4,4,4,4,4,4},
 {17,17,17,17,17,17,14},{17,17,17,17,17,10,4},
 {17,17,17,21,21,21,10},{17,17,10,4,10,17,17},
 {17,17,10,4,4,4,4},{31,1,2,4,8,16,31}
};
void face_date_text(int year,int month,int day,int weekday,int mask,char *out) {
 static const char *days[]={"SUN","MON","TUE","WED","THU","FRI","SAT"};
 static const char *months[]={"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};
 out[0]=0;
 if(year<1 || year>9999 || month<1 || month>12 || day<1 || day>31 || weekday<0 || weekday>6) return;
 char date[3],yr[5];snprintf(date,sizeof(date),"%02d",day);snprintf(yr,sizeof(yr),"%04d",year);
 const char *parts[]={days[weekday],date,months[month-1],yr};
 for(int i=0;i<4;++i) if(mask&(1<<i)) {
  if(out[0]) strcat(out," ");
  strcat(out,parts[i]);
 }
}
void face_render_custom(int h,int m,int edition,int year,int month,int day,
                        int weekday,int mask,int position,int font,int color,
                        int minute_color,int width,int minute_width,
                        int hour_size,int minute_size,int ticks,uint8_t *pixels) {
 set_style(edition,font,color,minute_color,width,minute_width);
 hour_label_scale=label_scale(hour_size,3);
 minute_label_scale=label_scale(minute_size,2);
 show_ticks=ticks ? 1 : 0;
 if(edition) render_split(h,m,pixels);else render_original(h,m,pixels);
 if(show_ticks) {
  for(int k=0;k<12;++k) {
   int step=k*60;
   float dx=(float)face_sine[step]/16384,dy=-(float)face_sine[(step+180)%720]/16384;
   int cx=nearest(100+92*dx),cy=nearest(114+92*dy);
   for(int yy=-1;yy<=1;++yy) for(int xx=-1;xx<=1;++xx)
    if(cx+xx>=0 && cx+xx<FACE_W && cy+yy>=0 && cy+yy<FACE_H) pixels[(cy+yy)*FACE_W+cx+xx]=1;
  }
 }
 /* Keep orientation marks outside the tested numeral envelope and date bands.
  * The three-pixel marks remain visible when a number reaches a cardinal. */
 if(edition==3 || edition==4) {
  const int origins[4][2]={{99,19},{197,113},{99,206},{0,113}};
  for(int k=0;k<4;++k) for(int y=0;y<3;++y) for(int x=0;x<3;++x)
   pixels[(origins[k][1]+y)*FACE_W+origins[k][0]+x]=1;
 }
 char text[32];face_date_text(year,month,day,weekday,mask,text);
 int len=(int)strlen(text),left=(FACE_W-(len*6-1)*2)/2;
 int top=position==1 ? FACE_H-18 : 4;
 for(int i=0;i<len;++i) for(int row=0;row<7;++row) {
  char c=text[i];uint8_t bits=0;
  if(c>='A' && c<='Z') bits=letters[c-'A'][row];
  else if(c>='0' && c<='9') bits=glyphs[c-'0'][row];
  for(int col=0;col<5;++col) if(bits&(1<<(4-col)))
   for(int sy=0;sy<2;++sy) for(int sx=0;sx<2;++sx)
    pixels[(top+row*2+sy)*FACE_W+left+i*12+col*2+sx]=1;
 }
}
void face_render_config(int h,int m,int edition,int year,int month,int day,
                        int weekday,int mask,int position,uint8_t *pixels) {
 face_render_custom(h,m,edition,year,month,day,weekday,mask,position,0,-1,-1,0,0,0,0,0,pixels);
}
#include "face_globe.h"
