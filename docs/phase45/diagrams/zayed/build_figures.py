"""Export the approved sequence content in readable portrait-page parts."""
from pathlib import Path
from html import escape
import json,textwrap,xml.etree.ElementTree as ET
from drawing import Diagram,ROOT

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'design-data.json').read_text())

class PrintSequence(Diagram):
 def __init__(self,name,title,participants):
  super().__init__(name,title,900,900);self.x={};self.y=152;self.group=None;self.msgs=[];self.carry_in=self.carry_out=()
  # Five lifelines keep the original spacing; six or more share the same 900-unit page width.
  n=len(participants)
  if n<=5:step,first,width,size,wrap=185,80,152,17,18
  else:step=900//n;first=(900-(n-1)*step)/2;width=step-10;size=16 if n==6 else 15;wrap=16 if n==6 else 14
  for i,(key,label) in enumerate(participants):
   x=first+i*step;self.x[key]=x
   lines=[]
   for line in label.split('\n'):lines+=textwrap.wrap(line,wrap,break_long_words=False)
   self.box(x-width/2,58,width,74,'\n'.join(lines),size=size)
 def msg(self,a,b,text,reply=False):
  if a==b:return self.self_msg(a,text)
  left,right=self.x[a],self.x[b]
  lines=textwrap.wrap(text,65 if abs(right-left)>380 else 45,break_long_words=False)
  width=max(map(len,lines))*18*.55
  centre=max(30+width/2,min(870-width/2,(left+right)/2))
  self.text(centre,self.y+18,'\n'.join(lines),18,halo=True)
  arrow=self.y+len(lines)*22+7
  self.msgs.append(dict(a=a,b=b,y=arrow,reply=reply,self=False))
  self.y=arrow+20
 def self_msg(self,a,text):
  # A call from a participant to itself, drawn as a loop with a nested activation.
  x=self.x[a]
  lines=textwrap.wrap(text,40,break_long_words=False)
  self.text(x+14,self.y+18,'\n'.join(lines),18,anchor='start',halo=True)
  top=self.y+len(lines)*22+7
  self.msgs.append(dict(a=a,b=a,y=top,reply=False,self=True))
  self.y=top+52
 def bar(self,x,top,bottom):
  self.svg.append(f'<rect x="{x}" y="{top}" width="8" height="{bottom-top}" fill="#cfdfd4" stroke="#385247"/>')
  self.cell('',x,top,8,bottom-top,'fillColor=#cfdfd4;strokeColor=#385247;')
 def activations(self):
  # A call starts the receiver's activation. It lasts until that participant's last
  # message or received reply before its next incoming call, or 12 units if it does nothing more.
  # An activation that continues across the printed split runs to the end of part 1
  # and from the top of part 2.
  bars=[];start={p:140 for p in self.carry_in};last=dict(start)
  for m in self.msgs:
   a,b,y=m['a'],m['b'],m['y']
   if m['self']:
    if a in start:last[a]=y+38
   elif m['reply']:
    for p in (a,b):
     if p in start:last[p]=y
   else:
    if a in start:last[a]=y
    if b in start:bars.append((b,start[b],last[b]))
    start[b]=last[b]=y
  bars+=[(p,start[p],self.y-5 if p in self.carry_out else last[p]) for p in start]
  return [(p,top,max(bottom,top+12)) for p,top,bottom in bars]
 def draw_messages(self):
  bars=self.activations()
  def active(p,y):return any(q==p and top<=y<=bottom for q,top,bottom in bars)
  first=len(self.svg)
  for p,top,bottom in bars:self.bar(self.x[p]-4,top,bottom)
  for m in self.msgs:
   if m['self']:
    x,y=self.x[m['a']],m['y'];self.bar(x+1,y+14,y+38)
    self.line([(x+4,y),(x+44,y),(x+44,y+24),(x+9,y+24)])
    continue
   a,b,y=self.x[m['a']],self.x[m['b']],m['y'];d=1 if b>a else -1
   if active(m['a'],y):a+=4*d
   if active(m['b'],y):b-=4*d
   self.line([(a,y),(b,y)],dashed=m['reply'],reply=m['reply'])
  # Activations sit above lifelines but below message labels and frames.
  drawn=self.svg[first:];del self.svg[first:];self.svg[1:1]=drawn
 def note(self,text):
  lines=[]
  for paragraph in text.split('\n'):lines+=textwrap.wrap(paragraph,91,break_long_words=False)
  height=len(lines)*21+22
  self.box(15,self.y+5,870,height,'\n'.join(lines),fill='#fff6e3',size=17)
  self.y+=height+20
 def begin(self,kind,guard):
  assert self.group is None
  self.group=(self.y,kind,guard);self.y+=43
 def otherwise(self,guard):
  self.line([(10,self.y+3),(890,self.y+3)],dashed=True,arrow=False)
  lines=textwrap.wrap(guard,99,break_long_words=False)
  self.text(22,self.y+25,'\n'.join(lines),15,bold=True,anchor='start',halo=True)
  self.y+=len(lines)*18+25
 def end(self):
  top,kind,guard=self.group;bottom=self.y+5
  self.svg.append(f'<rect x="10" y="{top}" width="880" height="{bottom-top}" fill="none" stroke="#6e8378"/>')
  self.cell('',10,top,880,bottom-top,'fillColor=none;strokeColor=#6e8378;')
  self.box(10,top,42,27,kind,fill='white',size=15)
  self.text(64,top+20,guard,15,bold=True,anchor='start',halo=True)
  self.y=bottom+15;self.group=None
 def finish(self,refs):
  assert self.group is None
  self.draw_messages()
  height=int(self.y+45)
  self.svg[0]=self.svg[0].replace('height="900"',f'height="{height}"',1).replace('viewBox="0 0 900 900"',f'viewBox="0 0 900 {height}"')
  self.h=height;self.model.set('pageHeight',str(height))
  for x in self.x.values():self.line([(x,132),(x,height-40)],dashed=True,arrow=False)
  self.save(self.title,refs,'')

def continuing(first,second):
 # Participants still handling a call at the split: they act in part 2 before receiving a new call.
 messages=lambda events:[(e[1],e[2],len(e)>4 and e[4]) for e in events if e[0]=='msg' and e[1]!=e[2]]
 called={b for a,b,reply in messages(first) if not reply};carried=set()
 for p in called:
  for a,b,reply in messages(second):
   if b==p and not reply:break
   if p in (a,b):carried.add(p);break
 return carried

for seq in DATA['sequences']:
 events=seq['events'];name=seq['name']
 full=PrintSequence(name,seq['title'],seq['participants'])
 for method,*args in events:getattr(full,method)(*args)
 full.finish(seq['refs'])
 (ROOT/'images'/(name+'.svg')).replace(HERE/(name+'.svg'))
 if '9-3-' in name:split=next(i for i,e in enumerate(events) if e[0]=='begin')
 else:
  split=next(i+1 for i,e in enumerate(events) if e[0]=='end')
  if '9-4-' in name:split+=1 # Keep the confidence note with the AI branches.
 carried=continuing(events[:split],events[split:])
 for i,part in enumerate((events[:split],events[split:]),1):
  drawing=PrintSequence(name+f'-part-{i}',seq['title']+f' ({i} of 2)',seq['participants'])
  if i==1:drawing.carry_out=carried
  else:drawing.carry_in=carried
  for method,*args in part:getattr(drawing,method)(*args)
  drawing.finish(seq['refs'])

# Enlarged halves of the existing activity drawings. The same A connector joins them.
for number,name in [(6,'figure-9-6-request-activity'),(7,'figure-9-7-maintenance-activity')]:
 original=ET.parse(HERE/(name+'.svg')).getroot()
 body=''.join(ET.tostring(child,encoding='unicode') for child in original)
 for part,(left,width) in enumerate(((0,590),(590,560)),1):
  x=(720-width)/2
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="716" viewBox="0 0 720 920"><rect width="720" height="920" fill="white"/><svg x="{x}" y="0" width="{width}" height="902" viewBox="{left} 48 {width} 902">{body}</svg></svg>'
  (ROOT/'images'/f'{name}-part-{part}.svg').write_text(svg,encoding='utf-8')
print('Exported eight sequence parts and four activity parts; original content is preserved.')
