import argparse,json,time
from pathlib import Path
import serial
class Device:
 def __init__(self,port,expected_mac=None):
  self.serial=serial.Serial();self.serial.port=port;self.serial.baudrate=115200;self.serial.timeout=.1;self.serial.dtr=False;self.serial.rts=False;self.serial.open();self.serial.reset_input_buffer()
  status=self.command({'cmd':'status'},8)
  if not status.get('firmware','').startswith('MSA-WiFi-Sentinel-') or expected_mac and status.get('mac','').lower()!=expected_mac.lower():self.close();raise RuntimeError('Target identity mismatch')
 def _json(self,timeout=5):
  deadline=time.monotonic()+timeout;line=bytearray();discard=False
  while time.monotonic()<deadline:
   b=self.serial.read(1)
   if not b:continue
   if b==b'\n':
    if not discard and line:
     try:item=json.loads(line)
     except Exception:item=None
     line.clear();discard=False
     if isinstance(item,dict):return item
    else:line.clear();discard=False
   elif not discard:
    if len(line)>=16384:line.clear();discard=True
    else:line.extend(b)
  raise TimeoutError('No valid response')
 def command(self,obj,timeout=5):self.serial.write(json.dumps(obj,separators=(',',':')).encode()+b'\n');return self._json(timeout)
 def capture(self):
  from PIL import Image
  h=self.command({'cmd':'capture'});w,ht,n=(h.get(k,0) for k in ('width','height','bytes'))
  if h.get('result')!='capture_begin' or not(0<w<=170 and 0<ht<=320 and n==w*ht*2):raise RuntimeError('Invalid capture header')
  data=bytearray();deadline=time.monotonic()+20
  while len(data)<n and time.monotonic()<deadline:data.extend(self.serial.read(min(8192,n-len(data))))
  if len(data)!=n or self._json().get('result')!='capture_end':raise RuntimeError('Incomplete capture')
  rgb=bytearray()
  for i in range(0,n,2):
   v=data[i]<<8|data[i+1];rgb.extend((((v>>11)&31)*255//31,((v>>5)&63)*255//63,(v&31)*255//31))
  return Image.frombytes('RGB',(w,ht),bytes(rgb))
 def close(self):self.serial.close()
def records(d):
 if d.command({'cmd':'aps'}).get('result')!='aps_begin':raise RuntimeError('Export failed')
 out=[]
 while len(out)<64:
  item=d._json(10)
  if item.get('result')=='aps_end':return out
  if item.get('record')=='ap':out.append(item)
 raise RuntimeError('Export bound exceeded')
def main():
 p=argparse.ArgumentParser();p.add_argument('--port',default='COM4');p.add_argument('--mac');sub=p.add_subparsers(dest='action',required=True)
 for a in ('status','aps','clear','forget-baseline'):sub.add_parser(a)
 sub.add_parser('select').add_argument('id',type=int);sub.add_parser('monitor').add_argument('state',choices=('on','off'));sub.add_parser('page').add_argument('index',type=int,choices=range(5));sub.add_parser('baseline').add_argument('--confirm-owned-network',action='store_true',required=True);sub.add_parser('capture').add_argument('path',type=Path)
 a=p.parse_args();d=Device(a.port,a.mac)
 try:
  if a.action=='aps':result=records(d)
  elif a.action=='capture':d.capture().save(a.path);result={'saved':str(a.path)}
  else:
   cmd=a.action.replace('-','_');obj={'cmd':cmd}
   if a.action=='select':obj['id']=a.id
   elif a.action=='monitor':obj['enabled']=a.state=='on'
   elif a.action=='page':obj['index']=a.index
   elif a.action=='baseline':obj['confirmed']=True
   result=d.command(obj)
  print(json.dumps(result,indent=2))
 finally:d.close()
if __name__=='__main__':main()
