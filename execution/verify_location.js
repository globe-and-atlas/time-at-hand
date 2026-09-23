/* Deterministic phone sandbox: no real geolocation or Pebble device access. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const names=JSON.parse(fs.readFileSync(path.join(root,'watchface/package.json'),'utf8')).pebble.messageKeys;
const keys=Object.fromEntries(names.map((name,i)=>[name,i]));
const data={};let callbacks={},requests=[],messages=[];
class Clay {
  constructor() {}
  getSettings(raw) {const settings=JSON.parse(raw);data['clay-settings']=JSON.stringify(settings);return Object.fromEntries(Object.entries(settings).map(([k,v])=>[keys[k],v]));}
  generateUrl() {return 'mock-settings';}
}
const context={require:name=>name==='@rebble/clay'?Clay:name==='message_keys'?keys:[{defaultValue:'G&A Meridian: Hemisphere'}],
  localStorage:{getItem:key=>data[key],setItem:(key,value)=>{data[key]=value;}},
  Pebble:{addEventListener:(name,fn)=>{callbacks[name]=fn;},sendAppMessage:(payload,ok)=>{messages.push({...payload});ok();},openURL:()=>{}},
  navigator:{geolocation:{getCurrentPosition:(ok,fail)=>{requests.push({ok,fail});}}},console,setInterval:()=>{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'watchface/src/pkjs/index.js'),'utf8'),context);
callbacks.ready();assert.equal(requests.length,0);assert.equal(messages.length,0,'Empty phone storage must preserve watch settings');
function save(s) {callbacks.webviewclosed({response:JSON.stringify(s)});}
save({LocationPreset:2,UsePhoneLocation:false});assert.equal(requests.length,0);assert.equal(messages.at(-1)[keys.Longitude],-8760);
save({LocationPreset:2,UsePhoneLocation:true,TimeFont:3});assert.equal(requests.length,1);assert.equal(messages.at(-1)[keys.TimeFont],3);
requests[0].ok({coords:{latitude:35.6895,longitude:139.6917}});
assert.equal(messages.at(-1)[keys.Latitude],3570);assert.equal(messages.at(-1)[keys.Longitude],13970);
callbacks.ready();requests.at(-1).fail();assert.equal(messages.at(-1)[keys.Longitude],13970);
const pending=requests.at(-1);
save({LocationPreset:1,UsePhoneLocation:false});pending.ok({coords:{latitude:0,longitude:0}});
assert.equal(messages.at(-1)[keys.Latitude],5150,'Late GPS callback cannot override manual mode');
save({LocationPreset:5,ManualLatitude:999,ManualLongitude:0});assert.equal(messages.at(-1)[keys.Latitude],5150);
save({LocationPreset:0,UsePhoneLocation:false});assert.equal(messages.at(-1)[keys.LocationValid],0);
console.log('PASS: opt-in, coarse coordinates, saved fallback, manual switch, stale callback, invalid coordinates, world reset');
