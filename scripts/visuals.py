"""Render actual triangulated CAD geometry and parameter-linked engineering diagrams."""
import os,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from cad.model import parameters,derived,build,fixture,box
P=parameters();D=derived(P)
INK='#172c45';TEAL='#008d92';ORANGE='#d88329';BG='#f5f7fa'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':INK,'axes.labelcolor':INK,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False})
COLORS={'base':'#b2c4d4','thermal_lid':'#7897b4','pcb':'#27816f','chip':'#263648','thermal_pad':'#eea340','connector':'#4b5b6c','component_keepout':'#89929c','fixture_plate':'#b2c4d4'}

def save(fig,name):
 fig.savefig(ROOT/'images'/f'{name}.png',dpi=190,bbox_inches='tight',facecolor=BG)
 fig.savefig(ROOT/'images'/f'{name}.svg',bbox_inches='tight',facecolor=BG)
 plt.close(fig)

def render(parts,name,title,explode=False,section=False,fixture_view=False):
 from scripts.raster import rasterize
 triangles=[];facecolors=[]
 for n,wp in parts.items():
  obj=wp
  if section:
   obj=obj.intersect(box(200,100,120,-30,35,-15))
   if not obj.val().Solids():continue
  v,f=obj.val().tessellate(.08,.12)
  if not f:continue
  verts=np.array([[q.x,q.y,q.z] for q in v]);faces=np.array(f)
  shift=0
  if explode:
   if n in ['pcb','chip','connector','component_keepout'] or n.startswith('pcb_screw'):shift=23
   elif n=='thermal_pad':shift=34
   elif n=='thermal_lid' or n.startswith('lid_screw'):shift=58
  verts[:,2]+=shift
  color=COLORS.get(n,ORANGE if 'locator' in n or 'pad' in n else '#66778b')
  triangles.extend(verts[faces]);facecolors.extend([color]*len(faces))
 pixels=rasterize(triangles,facecolors,width=1450,height=1100 if explode else 850)
 fig=plt.figure(figsize=(11,7.5 if explode else 6.3),facecolor=BG)
 ax=fig.add_axes([.01,.10,.75 if explode else .98,.72 if section else .80]);ax.imshow(pixels);ax.axis('off')
 fig.text(.04,.95,title,ha='left',fontsize=17,color=INK,weight='bold')
 fig.text(.04,.035,'EDGE / 01     |     Rev B     |     CAD geometry; physical validation pending',fontsize=9,color='#53677e')
 if explode:
  fig.text(.76,.76,'01  Finned thermal lid\n      Integral pedestal',fontsize=10)
  fig.text(.76,.48,'02  Thermal pad\n03  Generic PCB + chip',fontsize=10)
  fig.text(.76,.24,'04  Machined tray\n      Four PCB supports',fontsize=10)
 if section:fig.text(.06,.86,'Y = 35 mm section | Chip → pad → pedestal → fins → air',fontsize=10,color=TEAL)
 save(fig,name)

def dim(ax,a,b,label,axis='x',offset=-8):
 if axis=='x':
  x1,y1=a;x2,y2=b;y=offset
  ax.plot([x1,x1],[y1,y-1],color='#8c9aab',lw=.6);ax.plot([x2,x2],[y2,y-1],color='#8c9aab',lw=.6)
  ax.annotate('',(x1,y),(x2,y),arrowprops=dict(arrowstyle='<->',lw=.8,color=INK));ax.text((x1+x2)/2,y-1.8,label,ha='center',va='top',fontsize=9)
 else:
  x1,y1=a;x2,y2=b;x=offset
  ax.plot([x1,x+1],[y1,y1],color='#8c9aab',lw=.6);ax.plot([x2,x+1],[y2,y2],color='#8c9aab',lw=.6)
  ax.annotate('',(x,y1),(x,y2),arrowprops=dict(arrowstyle='<->',lw=.8,color=INK));ax.text(x+2,(y1+y2)/2,label,rotation=90,ha='left',va='center',fontsize=9)

def edges(ax,obj,axes=(0,1),z_filter=None,color=INK):
 for e in obj.val().Edges():
  pts,_=e.sample(.04);arr=np.array([[v.x,v.y,v.z] for v in pts])
  if z_filter is not None and not np.allclose(arr[:,2],z_filter,atol=.001):continue
  ax.plot(arr[:,axes[0]],arr[:,axes[1]],color=color,lw=.65)

def drawing(parts):
 L,W=P['length'],P['width']
 fig,axs=plt.subplots(1,2,figsize=(13,5.8),facecolor=BG)
 for ax in axs:ax.set_aspect('equal');ax.set_facecolor(BG);ax.axis('off')
 ax=axs[0];edges(ax,parts['base']);dim(ax,(0,0),(L,0),f'{L:g} ±0.10',offset=-10);dim(ax,(L,0),(L,W),f'{W:g} ±0.10','y',L+8)
 for i,(x,y) in enumerate(D['pcb_holes']):ax.text(x+4,y,f'P{i+1}',color=TEAL,fontsize=9)
 for i,(x,y) in enumerate(D['lid_holes']):ax.text(x+3,y,f'L{i+1}',fontsize=8)
 for i,(x,y) in enumerate(D['mounts']):ax.text(x+4,y,f'M{i+1}',fontsize=8)
 ax.text(0,-22,'Base | top view\nDatum B: Y=0 face; C: X=0 face\nDatum A: underside Z=0',fontsize=9,va='top')
 ax.set(xlim=(-12,123),ylim=(-48,80))
 ax=axs[1];edges(ax,parts['thermal_lid']);dim(ax,(35,23),(65,23),'30.00 fins / pedestal',offset=-10)
 ax.text(0,-22,'Thermal lid | top projection\nSix fins: 2.00 thick × 6.00 high; 3.60 channels\nFour F holes: Ø3.40 through for optional fan',fontsize=9,va='top')
 ax.set(xlim=(-12,123),ylim=(-48,80))
 fig.suptitle('E01 / E02  •  Housing and thermal lid  |  mm',x=.08,ha='left',fontsize=17)
 save(fig,'dimensioned_plan')
 for name,title in [('base','E01 / Base enclosure'),('thermal_lid','E02 / Thermal lid')]:
  fig,ax=plt.subplots(figsize=(8.8,6.2),facecolor=BG);ax.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off')
  edges(ax,parts[name]);dim(ax,(0,0),(L,0),f'{L:g} ±0.10',offset=-9);dim(ax,(L,0),(L,W),f'{W:g} ±0.10','y',L+8)
  holes=D['pcb_holes'] if name=='base' else D['fan_holes']
  prefix='P' if name=='base' else 'F'
  for i,(x,y) in enumerate(holes):ax.text(x+4,y+2,f'{prefix}{i+1}',color=TEAL,fontsize=9)
  for i,(x,y) in enumerate(D['lid_holes']):ax.text(x+3,y+2,f'L{i+1}',fontsize=8)
  if name=='base':
   for i,(x,y) in enumerate(D['mounts']):ax.text(x+4,y+2,f'M{i+1}',fontsize=9)
   note='A: underside Z0 | B: front Y0 | C: left X0\nHole coordinates and tolerances in table below.\nTop projection; underside and pocket edges included.'
  else:note='D: underside mating plane | E: front | F: left\nFin field 30 × 24; six fins 2 thick × 6 high.\nTop projection; underside pedestal edges included.'
  ax.text(0,-21,note,fontsize=10,va='top',linespacing=1.6)
  ax.set(xlim=(-8,123),ylim=(-48,81));ax.set_title(title+' | mm',loc='left',fontsize=16,pad=15)
  save(fig,name+'_drawing')
 # Section diagram dimensions use the same model values. Actual CAD geometry shown separately.
 fig,ax=plt.subplots(figsize=(11,4.5),facecolor=BG);ax.set_facecolor(BG);ax.set_aspect('equal')
 for n in ['base','thermal_lid','pcb','chip','thermal_pad']:
  obj=parts[n].intersect(box(200,.05,100,-30,W/2,-15));edges(ax,obj,axes=(0,2),color=COLORS[n])
 dim(ax,(0,0),(0,P['height']),'25.00','y',-10)
 ax.annotate('TIM gap: 0.50 nominal\n0.31–0.69 worst case',(50,D['pad_z']+.25),(58,38),arrowprops=dict(arrowstyle='->',color=ORANGE),fontsize=10,color=ORANGE)
 ax.annotate('PCB underside Z=6.00',(20,6),(3,-13),arrowprops=dict(arrowstyle='->',color=TEAL),fontsize=10)
 ax.text(2,34,'Seat Z=17.00  |  Lid plate Z=17..19  |  Fins to Z=25',fontsize=10)
 ax.set(xlim=(-18,119),ylim=(-20,45));ax.axis('off');ax.set_title('E03  •  Center section and thermal interface | Y = 35 mm',loc='left',pad=18)
 save(fig,'dimensioned_section')

def fixture_layout(p,fx):
 fig,ax=plt.subplots(figsize=(10,7),facecolor=BG);ax.set_facecolor(BG);ax.set_aspect('equal')
 for n,obj in fx.items():edges(ax,obj,color=TEAL if 'locator' in n else '#8092a7')
 ax.add_patch(Rectangle((0,0),100,70,fill=False,lw=1.4,ec=INK))
 labels=[(18,12,'A1'),(82,12,'A2'),(50,58,'A3'),(20,-3,'B1'),(80,-3,'B2'),(-3,35,'C1')]
 for x,y,t in labels:ax.text(x+4,y+4,t,color=TEAL,weight='bold')
 for x,y,dx,dy in [(50,79,0,-7),(110,35,-7,0)]:ax.annotate('',(x+dx,y+dy),(x,y),arrowprops=dict(arrowstyle='->',lw=2,color=ORANGE))
 dim(ax,(-15,-15),(115,-15),'130.00 plate',offset=-24);dim(ax,(115,-15),(115,85),'100.00','y',125)
 ax.text(-12,93,'Three Z pads + two Y stops + one X stop',fontsize=12,color=TEAL)
 ax.set(xlim=(-25,140),ylim=(-35,105));ax.axis('off');ax.set_title('F01  •  3–2–1 locating fixture | top view',loc='left',fontsize=18)
 save(fig,'fixture_layout')

def setups():
 fig,axs=plt.subplots(1,3,figsize=(13,4.8),facecolor=BG)
 for ax,title in zip(axs,['SETUP 1 / pocket up','SETUP 2 / finish underside','SETUP 3 / connector face up']):
  ax.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off');ax.set(xlim=(-18,118),ylim=(-20,85));ax.set_title(title,fontsize=12,loc='left')
  ax.add_patch(Rectangle((-8,-10),116,12,color='#687d94'));ax.add_patch(Rectangle((0,2),100,30,facecolor='#b2c4d4',edgecolor=INK))
  ax.add_patch(Rectangle((-12,-10),12,40,color='#8497ab'));ax.add_patch(Rectangle((100,-10),12,40,color='#8497ab'))
  ax.add_patch(Rectangle((46,53),8,24,color=TEAL));ax.annotate('',(50,36),(50,51),arrowprops=dict(arrowstyle='->',lw=2,color=TEAL))
 axs[0].add_patch(Rectangle((8,15),84,17,facecolor=BG,edgecolor=INK));axs[0].text(2,-20,'Sacrificial 5 mm grip below part\nG54 at faced stock corner',va='top',fontsize=9)
 axs[1].add_patch(Rectangle((8,2),84,17,facecolor='#e7b16b',edgecolor=INK));axs[1].text(2,-20,'Soft jaws + cavity support insert\nProbe finished B/C; face to A',va='top',fontsize=9)
 axs[2].add_patch(Rectangle((25,12),16,7,facecolor=BG,edgecolor=INK));axs[2].text(2,-20,'90° nest; support walls near cut\n3 mm tool; R1.5 opening corners',va='top',fontsize=9)
 fig.suptitle('CNC setup concepts | review before programming',x=.06,ha='left',fontsize=18)
 fig.text(.06,.015,'Illustrative setup geometry. No generated or verified machine toolpaths; clamp and tool envelopes require CAM review.',fontsize=9)
 save(fig,'cnc_setups')

def concepts():
 criteria=['Packaging','Thermal','Manufacturing','Service','Assembly','Inspection','Cost / iteration'];weights=np.array([.15,.2,.2,.15,.1,.1,.1]);scores=np.array([[5,4,3,5,4,4,3],[4,3,5,3,3,3,5],[5,2,4,4,4,4,5]])
 fig,ax=plt.subplots(figsize=(11,3.9),facecolor=BG);ax.set_facecolor(BG);ax.imshow(scores,cmap='GnBu',vmin=1,vmax=5,aspect='auto',alpha=.7)
 ax.set_xticks(range(7),[f'{c}\n{int(w*100)}%' for c,w in zip(criteria,weights)],fontsize=9);ax.set_yticks(range(3),['A / CNC tray + thermal lid','B / bent sheet + heat spreader','C / printed shell + insert'],fontsize=10)
 for i in range(3):
  for j in range(7):ax.text(j,i,str(scores[i,j]),ha='center',va='center',fontsize=14,color=INK)
  ax.text(6.7,i,f'{scores[i]@weights:.2f}',va='center',weight='bold')
 ax.set_title('Concept selection | weighted score / 5, engineering judgment',loc='left',pad=20)
 ax.spines[['left','bottom']].set_visible(False);fig.tight_layout();save(fig,'concept_matrix')
 (ROOT/'results/concepts.json').write_text(json.dumps({'criteria':criteria,'weights':weights.tolist(),'scores':scores.tolist(),'totals':(scores@weights).tolist(),'selected':'A','status':'subjective screening, not experimentally validated'},indent=2)+'\n')

def main():
 parts=build(P);fx=fixture(P)
 render(parts,'assembly','EDGE / 01  Compact edge-compute enclosure')
 render(parts,'exploded','Built for access. Designed around the thermal path.',explode=True)
 render(parts,'section','One thermal path. Visible assumptions.',section=True)
 render({'base':parts['base'],**fx},'fixture','Locate once. Reinstall repeatably.',fixture_view=True)
 render(build(dict(P,fan_enabled=True)),'forced_air','Optional forced air | 35 mm fan envelope')
 drawing(parts);fixture_layout(P,fx);setups();concepts()
 print('Generated five CAD mesh views, two dimensioned views, fixture layout, setup diagram, concept matrix.')
if __name__=='__main__':main()
