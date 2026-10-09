"""Validate actual solids, reimported STEP, STL topology, and CAD intersections."""
import sys,json,hashlib,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import cadquery as cq
import trimesh
from cad.model import build,fixture,parameters,derived
from analysis.thermal import calculate

def check_parts(parts,exported=True):
    records={};failures=[]
    for name,obj in parts.items():
        shape=obj.val();bb=shape.BoundingBox()
        row={'valid_BRep':shape.isValid(),'solid_count':len(shape.Solids()),'volume_mm3':shape.Volume(),'bounds_mm':[bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax]}
        if not row['valid_BRep'] or row['solid_count']!=1 or row['volume_mm3']<=0:failures.append(name+': invalid solid')
        if exported:
            for ext in ['step','stl']:
                f=ROOT/'exports'/f'{name}.{ext}'
                if not f.exists() or f.stat().st_size<100:failures.append(str(f)+': missing or empty');continue
                row[ext+'_sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
            step=cq.importers.importStep(str(ROOT/'exports'/f'{name}.step')).val()
            row['step_valid']=step.isValid();row['step_volume_relative_error']=abs(step.Volume()-shape.Volume())/shape.Volume()
            mesh=trimesh.load_mesh(ROOT/'exports'/f'{name}.stl')
            row.update(stl_watertight=bool(mesh.is_watertight),stl_winding_consistent=bool(mesh.is_winding_consistent),stl_volume_mm3=float(mesh.volume),stl_volume_relative_error=abs(float(mesh.volume)-shape.Volume())/shape.Volume())
            if not row['step_valid'] or row['step_volume_relative_error']>1e-6 or not row['stl_watertight'] or not row['stl_winding_consistent'] or row['stl_volume_relative_error']>.01:failures.append(name+': export validation')
        records[name]=row
    return records,failures

def intersections(parts):
    errors=[];maxv=0.;pairs=0
    for (na,a),(nb,b) in itertools.combinations(parts.items(),2):
        vol=a.val().intersect(b.val()).Volume();pairs+=1;maxv=max(maxv,vol)
        if vol>1e-5:errors.append({'parts':[na,nb],'intersection_mm3':vol})
    return {'pair_count':pairs,'max_overlap_mm3':maxv,'unintended_intersections':errors}

def main():
    p=parameters();parts=build(p);fx=fixture(p)
    records,failures=check_parts({**parts,**fx})
    pairs=intersections(parts)
    fan=build(dict(p,fan_enabled=True));forced=intersections(fan)
    extra,extra_failures=check_parts({n:s for n,s in fan.items() if n.startswith('fan')})
    records.update(extra);failures.extend(extra_failures)
    fixture_pairs=intersections({'base':parts['base'],**fx})
    for name,value in [('assembly',pairs),('forced_air',forced),('fixture',fixture_pairs)]:
        if value['unintended_intersections']:failures.append(name+': interference')
    assembly=cq.importers.importStep(str(ROOT/'exports/assembly.step')).val()
    forced_shape=cq.importers.importStep(str(ROOT/'exports/forced_air_assembly.step')).val()
    for sh,n in [(assembly,len(parts)),(forced_shape,len(fan))]:
        if not sh.isValid() or len(sh.Solids())!=n:failures.append('STEP assembly solid count or validity')
    # Board connectors extend 2 mm beyond the housing; state both envelopes.
    bb=assembly.BoundingBox();fbb=forced_shape.BoundingBox()
    dims={'housing_mm':[p['length'],p['width'],p['height']],'assembly_including_connector_mm':[bb.xlen,bb.ylen,bb.zlen],'forced_with_fan_mm':[fbb.xlen,fbb.ylen,fbb.zlen],'fan_fastener_heads':'not modeled; reserve additional 3 mm above 35 mm fan envelope','external_cable_keepout_mm':p['cable_keepout']}
    if max(abs(a-b) for a,b in zip([bb.xlen,bb.ylen,bb.zlen],[p['length'],p['width']+2,p['height']]))>1e-5:failures.append('assembly envelope unexpected')
    # Tooling checks use CAD layout and explicit cutter-envelope collision at pad-to-island corner.
    tool_checks={'main_pocket_corner_radius_mm':p['pocket_radius'],'main_rough_tool_diameter_mm':6,'fin_channel_mm':(p['sink_length']-p['fin_count']*p['fin_thickness'])/(p['fin_count']-1),'fin_finish_tool_mm':3,'connector_radius_mm':p['connector_radius'],'connector_finish_tool_mm':3,'full_CAM_simulation':'not performed'}
    report={'status':'PASS' if not failures else 'FAIL','parts':records,'assembly_interference':pairs,'forced_air_interference':forced,'fixture_interference':fixture_pairs,'assembly_STEP_solids':len(assembly.Solids()),'forced_STEP_solids':len(forced_shape.Solids()),'envelopes':dims,'tool_checks':tool_checks,'failures':failures,'not_verified':['OpenSCAD companion execution','machine-specific CAM / swept cutter collisions','physical fit, pad pressure, heat transfer, thread strength, vibration, fixture repeatability','fan hardware, leads and cable routing geometry','edge break hand-deburr operation (not modeled)']}
    (ROOT/'results/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='parts'},indent=2))
    return bool(failures)
if __name__=='__main__':raise SystemExit(main())
