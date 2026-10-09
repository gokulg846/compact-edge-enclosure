"""Generate editable OpenSCAD companion from shared JSON; B-rep is release source."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cadquery as cq
from cad.model import parameters,derived

def main():
 p=parameters();d=derived(p);L,W,w=p['length'],p['width'],p['wall'];a=10
 pts=[(a,w),(L-a,w),(L-a,a),(L-w,a),(L-w,W-a),(L-a,W-a),(L-a,W-w),(a,W-w),(a,W-a),(w,W-a),(w,a),(a,a)]
 cavity=cq.Workplane('XY').polyline(pts).close().extrude(1).edges('|Z').fillet(p['pocket_radius'])
 wire=cavity.faces('<Z').val().outerWire();points,_=wire.sample(.01)
 values={**p,**d,'pocket_outline':[[round(v.x,5),round(v.y,5)] for v in points]}
 (ROOT/'cad/generated_parameters.scad').write_text('// Generated from parameters.json by scripts/scad.py. Units mm.\n'+'\n'.join(k+' = '+json.dumps(v)+';' for k,v in values.items())+'\n')
 print('Generated OpenSCAD parameters and sampled R3 pocket profile; OpenSCAD execution not available.')
if __name__=='__main__':main()
