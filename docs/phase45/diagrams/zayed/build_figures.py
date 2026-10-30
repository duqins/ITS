"""Export the approved sequence content in readable portrait-page parts."""
from pathlib import Path
from html import escape
import json,textwrap,xml.etree.ElementTree as ET
from drawing import Diagram,ROOT

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'design-data.json').read_text())

class PrintSequence(Diagram):
 def __init__(self,name,title,participants):
  super().__init__(name,title,900,900);self.x={};self.y=152;self.group=None
  for i,(key,label) in enumerate(participants):
   x=80+i*185;self.x[key]=x
   lines=[]
   for line in label.split('\n'):lines+=textwrap.wrap(line,18)
   self.box(x-76,58,152,74,'\n'.join(lines),size=17)
 def msg(self,a,b,text,reply=False):
  left,right=self.x[a],self.x[b]
  lines=textwrap.wrap(text,65 if abs(right-left)>380 else 45,break_long_words=False)
  width=max(map(len,lines))*18*.55
  centre=max(30+width/2,min(870-width/2,(left+right)/2))
  self.text(centre,self.y+18,'\n'.join(lines),18)
  arrow=self.y+len(lines)*22+7
  self.line([(left,arrow),(right,arrow)],dashed=reply,reply=reply)
  if not reply:self.box(right-4,arrow,8,12,'',fill='#cfdfd4')
  self.y=arrow+20
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
  self.text(22,self.y+25,'\n'.join(lines),15,bold=True,anchor='start')
  self.y+=len(lines)*18+25
 def end(self):
  top,kind,guard=self.group;bottom=self.y+5
  self.svg.append(f'<rect x="10" y="{top}" width="880" height="{bottom-top}" fill="none" stroke="#6e8378"/>')
  self.cell('',10,top,880,bottom-top,'fillColor=none;strokeColor=#6e8378;')
  self.box(10,top,42,27,kind,fill='white',size=15)
  self.text(64,top+20,guard,15,bold=True,anchor='start')
  self.y=bottom+15;self.group=None
 def finish(self,refs):
  assert self.group is None
  height=int(self.y+45)
  self.svg[0]=self.svg[0].replace('height="900"',f'height="{height}"',1).replace('viewBox="0 0 900 900"',f'viewBox="0 0 900 {height}"')
  self.h=height;self.model.set('pageHeight',str(height))
  for x in self.x.values():self.line([(x,132),(x,height-40)],dashed=True,arrow=False)
  self.save(self.title,refs,'')

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
 for i,part in enumerate((events[:split],events[split:]),1):
  drawing=PrintSequence(name+f'-part-{i}',seq['title']+f' ({i} of 2)',seq['participants'])
  for method,*args in part:getattr(drawing,method)(*args)
  drawing.finish(seq['refs'])

# Enlarged halves of the existing activity drawings. The same A connector joins them.
for number,name in [(6,'figure-9-6-request-activity'),(7,'figure-9-7-maintenance-activity')]:
 original=ET.parse(HERE/(name+'.svg')).getroot()
 body=''.join(ET.tostring(child,encoding='unicode') for child in original)
 for part,(left,width) in enumerate(((0,590),(590,560)),1):
  x=(720-width)/2
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="747" viewBox="0 0 720 960"><rect width="720" height="960" fill="white"/><text x="360" y="26" text-anchor="middle" font-family="Arial" font-size="19" font-weight="bold">Figure 9.{number} Activity diagram ({part} of 2)</text><svg x="{x}" y="43" width="{width}" height="902" viewBox="{left} 48 {width} 902">{body}</svg></svg>'
  (ROOT/'images'/f'{name}-part-{part}.svg').write_text(svg,encoding='utf-8')
print('Exported eight sequence parts and four activity parts; original content is preserved.')
