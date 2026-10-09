import sys,json,hashlib,platform,shutil,importlib.metadata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cadquery as cq
from cad.model import build,fixture,parameters

def export_part(name,obj):
    cq.exporters.export(obj,str(ROOT/'exports'/f'{name}.step'))
    cq.exporters.export(obj,str(ROOT/'exports'/f'{name}.stl'),tolerance=.03,angularTolerance=.1)

def main():
    p=parameters();parts=build(p);fx=fixture(p)
    for folder in ['exports','results','images']: (ROOT/folder).mkdir(exist_ok=True)
    for name,obj in {**parts,**fx}.items():export_part(name,obj)
    assembly=cq.Assembly(name='compact_edge_enclosure')
    for name,obj in parts.items():assembly.add(obj,name=name)
    assembly.export(str(ROOT/'exports/assembly.step'))
    fan=build(dict(p,fan_enabled=True))
    a=cq.Assembly(name='forced_air_option')
    for name,obj in fan.items():a.add(obj,name=name)
    a.export(str(ROOT/'exports/forced_air_assembly.step'))
    for name,obj in fan.items():
        if name.startswith('fan'):export_part(name,obj)
    # Genuine CAD-generated hidden-line SVGs; styling is handled by the drawing generator.
    for name in ['base','thermal_lid']:
        cq.exporters.export(parts[name],str(ROOT/'drawings'/f'{name}_cad.svg'),opt={'width':900,'height':650,'projectionDir':(1,-1,1),'showAxes':False,'strokeWidth':.5})
    # DXF sections are actual closed B-rep sections, not dimensioned release drawings.
    for name,z in [('base',8),('thermal_lid',18)]:
        section=parts[name].section(z)
        cq.exporters.export(section,str(ROOT/'exports'/f'{name}_section.dxf'))
    env={'python':sys.version,'platform':platform.platform(),'packages':{n:importlib.metadata.version(n) for n in ['cadquery','cadquery-ocp','trimesh','matplotlib','reportlab','pytest']},'tools':{n:shutil.which(n) for n in ['FreeCAD','openscad','gh','pdftoppm']},'CAD_route':'CadQuery installed in isolated venv; OpenSCAD companion generated but not executed; no native CAM available'}
    (ROOT/'results/environment.json').write_text(json.dumps(env,indent=2)+'\n')
    print(f'Exported {len(parts)} enclosure and {len(fx)} fixture components, passive + forced STEP assemblies.')
if __name__=='__main__':main()
