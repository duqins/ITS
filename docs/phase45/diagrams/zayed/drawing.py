from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
CAT=[]
class Diagram:
 def __init__(self,name,title,w=1150,h=800):
  self.name,self.title,self.w,self.h=name,title,w,h
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#243b33"/></marker><marker id="open" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#243b33"/></marker></defs><rect width="100%" height="100%" fill="white"/>']
  self.mx=ET.Element('mxfile',host='app.diagrams.net',version='24.7.17');di=ET.SubElement(self.mx,'diagram',name=title,id=name);self.model=ET.SubElement(di,'mxGraphModel',page='1',pageWidth=str(w),pageHeight=str(h),grid='1',gridSize='10');self.root=ET.SubElement(self.model,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0');self.i=1
 def cell(self,value,x,y,w,h,style):
  self.i+=1;c=ET.SubElement(self.root,'mxCell',id=str(self.i),value=value,style=style+';fontFamily=Arial;'+('fontSize=16;' if 'fontSize=' not in style else '')+'whiteSpace=wrap;html=0;',vertex='1',parent='1');ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'});return str(self.i)
 def text(self,x,y,t,size=16,bold=False,anchor='middle',halo=False):
  # A white halo keeps a label readable where lifelines or flows pass behind it.
  lines=t.split('\n');self.svg.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="#172d27"'+(' stroke="white" stroke-width="5" stroke-linejoin="round" paint-order="stroke"' if halo else '')+'>'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.2}">{escape(l)}</tspan>' for i,l in enumerate(lines))+'</text>')
  width=max(len(l) for l in lines)*size*.55;self.cell(t,x-{'middle':width/2,'end':width}.get(anchor,0),y-size,width,size*1.25*len(lines),'text;strokeColor=none;fillColor=none;align='+{'middle':'center','end':'right'}.get(anchor,'left')+f';fontSize={size};'+('fontStyle=1;' if bold else '')+('labelBackgroundColor=#ffffff;' if halo else ''))
 def box(self,x,y,w,h,t,kind='rect',fill='#f0f5f1',size=16):
  style=f'fillColor={fill};strokeColor=#385247;align=center;verticalAlign=middle;'
  if kind=='ellipse':self.svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="#385247"/>');style+='ellipse;'
  elif kind=='diamond':self.svg.append(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" fill="{fill}" stroke="#385247"/>');style+='rhombus;'
  else:self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{9 if kind=="round" else 0}" fill="{fill}" stroke="#385247"/>');style+=('rounded=1;arcSize=15;' if kind=='round' else '')
  # Shape and label are independently editable.
  self.cell('',x,y,w,h,style)
  lines=t.split('\n');self.text(x+w/2,y+h/2-(len(lines)-1)*size*.6+size*.34,t,size)
 def line(self,points,label='',dashed=False,arrow=True,reply=False,labelpos=None,labelanchor='middle'):
  pts=' '.join(f'{x},{y}' for x,y in points);self.svg.append(f'<polyline points="{pts}" fill="none" stroke="#243b33" stroke-width="1.4"'+(' stroke-dasharray="5 4"' if dashed else '')+(f' marker-end="url(#{"open" if reply else "arrow"})"' if arrow else '')+'/>')
  self.i+=1;c=ET.SubElement(self.root,'mxCell',id=str(self.i),value='',style=f'edgeStyle=none;rounded=0;strokeColor=#243b33;endArrow={"open" if reply else "block" if arrow else "none"};endFill={0 if reply else 1};dashed={1 if dashed else 0};',edge='1',parent='1');g=ET.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'});ET.SubElement(g,'mxPoint',x=str(points[0][0]),y=str(points[0][1]),**{'as':'sourcePoint'});ET.SubElement(g,'mxPoint',x=str(points[-1][0]),y=str(points[-1][1]),**{'as':'targetPoint'});
  if len(points)>2:
   ar=ET.SubElement(g,'Array',**{'as':'points'})
   for x,y in points[1:-1]:ET.SubElement(ar,'mxPoint',x=str(x),y=str(y))
  if label:
   x,y=labelpos or ((points[0][0]+points[-1][0])/2,(points[0][1]+points[-1][1])/2-8);self.text(x,y,label,15,anchor=labelanchor,halo=True)
 def actor(self,x,y,name):
  self.svg.append(f'<circle cx="{x}" cy="{y}" r="10" fill="white" stroke="#243b33"/><path d="M{x},{y+10}v29 M{x-19},{y+21}h38 M{x},{y+39}l-16,22 M{x},{y+39}l16,22" stroke="#243b33" fill="none"/>');self.cell('',x-20,y-10,40,72,'shape=umlActor;fillColor=#ffffff;strokeColor=#243b33;');self.text(x,y+83,name,16)
 def frame(self,x,y,w,h,label):
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#6e8378"/>');self.cell('',x,y,w,h,'fillColor=none;strokeColor=#6e8378;');self.text(x+10,y+19,label,15,bold=True,anchor='start')
 def dot(self,x,y,final=False):
  if final:self.box(x-10,y-10,20,20,'',kind='ellipse',fill='white')
  self.svg.append(f'<circle cx="{x}" cy="{y}" r="{6 if final else 8}" fill="#243b33"/>');self.cell('',x-6,y-6,12,12,'ellipse;fillColor=#243b33;strokeColor=#243b33;')
 def save(self,caption,refs,explanation):
  # Keep connector strokes under nodes and their labels.
  edge_items=[s for s in self.svg if s.startswith('<polyline')]
  self.svg=self.svg[:1]+edge_items+[s for s in self.svg[1:] if not s.startswith('<polyline')]
  (ROOT/'images'/f'{self.name}.svg').write_text(''.join(self.svg)+'</svg>',encoding='utf-8');ET.indent(self.mx);ET.ElementTree(self.mx).write(ROOT/'diagrams'/'zayed'/f'{self.name}.drawio',encoding='utf-8',xml_declaration=True)
  CAT.append(dict(name=self.name,title=self.title,caption=caption,refs=refs,explanation=explanation))
