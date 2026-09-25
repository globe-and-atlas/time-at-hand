#!/usr/bin/env python3
"""Keep preview option catalogs and bundled phone settings aligned."""
import json
from pathlib import Path
from generate_fonts import FONTS
ROOT=Path(__file__).resolve().parents[1]
COLORS=[(-1,'Edition default'),(1,'Black'),(2,'Amber'),(3,'Brick red'),(4,'Cobalt'),(5,'Forest'),(6,'Violet'),(7,'Graphite'),(8,'Teal')]
WIDTHS=[(0,'Edition default')]+[(i,f'{i} px') for i in range(1,9)]
LABEL_SIZES=[(0,'Edition default'),(1,'Small'),(2,'Medium'),(3,'Large')]
DATE_FORMATS=[(0,'Weekday · day · month · year'),(1,'Day · month · year · weekday'),(2,'Month · day · year · weekday'),(3,'ISO date · weekday')]
BATTERY_MODES=[(0,'Off'),(1,'Percent'),(2,'Thin bar'),(3,'Low battery only')]
THEMES=[(0,'Light'),(1,'Dark')]
def select(key,label,default,options):
    return {'type':'select','messageKey':key,'label':label,'defaultValue':str(default),'serializeValueAs':'integer','options':[{'value':str(value),'label':name} for value,name in options]}
def configuration(edition):
    date_fields=[{'type':'toggle','messageKey':key,'label':label,'defaultValue':False} for key,label in [('ShowWeekday','Weekday · WED'),('ShowDay','Day · 23'),('ShowMonth','Month · SEP'),('ShowYear','Year · 2026')]]
    style=[select('TimeFont','Time numerals',0,[(i,group+' / '+name) for i,(group,name,_) in enumerate(FONTS)]),{'type':'color','messageKey':'HandColorRGB','label':'Hour hand color' if edition else 'Hand color','defaultValue':'000000' if edition else 'FFAA00','layout':'COLOR'},select('HandWidth','Hour hand width' if edition else 'Hand width',0,WIDTHS),select('HourLabelSize','Hour label size',0,LABEL_SIZES),{'type':'toggle','messageKey':'ShowTicks','label':'Show twelve tick marks','defaultValue':False}]
    if edition:style.extend([{'type':'color','messageKey':'MinuteColorRGB','label':'Minute hand color','defaultValue':'000000' if edition==3 else 'AA5500' if edition==4 else 'FFAA00','layout':'COLOR'},select('MinuteWidth','Minute hand width',0,WIDTHS),select('MinuteLabelSize','Minute label size',0,LABEL_SIZES)])
    display=[select('DialTheme','Dial theme',0,THEMES),{'type':'toggle','messageKey':'ShowPivot','label':'Show center pivot','defaultValue':True},select('BatteryMode','Battery indicator',0,BATTERY_MODES),{'type':'toggle','messageKey':'BluetoothMode','label':'Show disconnect marker','defaultValue':True}, {'type':'toggle','messageKey':'HourFormat','label':'Leading zero on hour','defaultValue':False},{'type':'toggle','messageKey':'MinuteFormat','label':'Leading zero on minute','defaultValue':True}]
    location=[]
    if edition==2:
        location=[{'type':'section','items':[
          {'type':'heading','defaultValue':'Hemisphere location'},
          {'type':'toggle','messageKey':'UsePhoneLocation','label':'Use phone location (optional)','defaultValue':False},
          select('LocationPreset','Manual view / initial fallback',0,[(0,'World view'),(1,'London'),(2,'Chicago'),(3,'Tokyo'),(4,'Sydney'),(5,'Custom coordinates')]),
          {'type':'input','messageKey':'ManualLatitude','label':'Custom latitude (-90 to 90)','defaultValue':'0','attributes':{'type':'number','min':-90,'max':90,'step':0.1}},
          {'type':'input','messageKey':'ManualLongitude','label':'Custom longitude (-180 to 180)','defaultValue':'0','attributes':{'type':'number','min':-180,'max':180,'step':0.1}},
          {'type':'color','messageKey':'WaterColorRGB','label':'Water color','defaultValue':'FFFFFF','layout':'COLOR'},
          {'type':'color','messageKey':'LandColorRGB','label':'Land color','defaultValue':'555555','layout':'COLOR'},
          {'type':'text','defaultValue':'Phone location is rounded to 0.1 degrees, refreshed on launch, Save, then hourly. If unavailable, the last saved view remains. No location is sent to a web service. Sunlight uses UTC; hands use your watch clock. Location does not set the time zone.'}
        ]}]
    return [
      {'type':'heading','defaultValue':['Origin','Vector','Meridian','Cardinal','Clarity'][edition]},
      {'type':'text','defaultValue':'Each edition remembers its own choices. Time numerals stay black; the date uses a consistent small pixel font.'},
      {'type':'section','items':[{'type':'heading','defaultValue':'Type & hands'},*style]},
      {'type':'section','items':[{'type':'heading','defaultValue':'Dial status'},*display]},
      {'type':'section','items':[{'type':'heading','defaultValue':'Date line'},*date_fields,select('DatePosition','Position',0,[(0,'Top'),(1,'Bottom')]),select('DateFormat','Order',0,DATE_FORMATS)]},
      {'type':'text','defaultValue':'Choose any date combination, for example WED 23 SEP 2026. Turn every field off for a clean dial. Dates follow watch local time.'},
      *location,{'type':'submit','defaultValue':'Save settings'}]
def main():
    catalog={'fonts':[{'id':i,'group':group,'name':name} for i,(group,name,_) in enumerate(FONTS)],'colors':[{'id':i,'name':n} for i,n in COLORS],'widths':[{'id':i,'name':n} for i,n in WIDTHS],'labelSizes':[{'id':i,'name':n} for i,n in LABEL_SIZES],'dateFormats':[{'id':i,'name':n} for i,n in DATE_FORMATS],'batteryModes':[{'id':i,'name':n} for i,n in BATTERY_MODES],'themes':[{'id':i,'name':n} for i,n in THEMES]}
    (ROOT/'src/settings.js').write_text('/* Generated by execution/generate_settings.py. */\nconst WatchStyles = '+json.dumps(catalog)+';\n')
    (ROOT/'watchface/src/pkjs/config.json').write_text(json.dumps(configuration(0),indent=2)+'\n')
    print('Generated preview catalog and Origin phone settings.')
if __name__=='__main__':main()
