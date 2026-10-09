"""Parametric millimetre B-rep model. Run scripts/build.py from repository root."""
import json, math
from pathlib import Path
import cadquery as cq
ROOT = Path(__file__).resolve().parents[1]

def parameters(path=None):
    return json.loads(Path(path or ROOT/'cad/parameters.json').read_text())

def derived(p):
    L,W = p['length'],p['width']
    body = p['height']-p['lid_thickness']-p['fin_height']
    board_z=p['floor']+p['support_height']
    chip_z=board_z+p['board_thickness']
    pad_z=chip_z+p['chip_height']
    ped_z=pad_z+p['pad_compressed']
    bx=p['board_x']+p['board_length']/2
    by=p['board_y']+p['board_width']/2
    return dict(body=body,board_z=board_z,chip_z=chip_z,pad_z=pad_z,ped_z=ped_z,
        lid_holes=[(x,y) for x in [p['lid_screw_inset'],L-p['lid_screw_inset']] for y in [p['lid_screw_inset'],W-p['lid_screw_inset']]],
        pcb_holes=[(bx+sx*p['board_hole_pitch_x']/2,by+sy*p['board_hole_pitch_y']/2) for sx in [-1,1] for sy in [-1,1]],
        fan_holes=[(L/2+sx*p['fan_pitch']/2,W/2+sy*p['fan_pitch']/2) for sx in [-1,1] for sy in [-1,1]],
        mounts=[(L/2-p['mount_pitch']/2,W/2),(L/2+p['mount_pitch']/2,W/2)])

def validate_parameters(p):
    for k,v in p.items():
        if isinstance(v,(int,float)) and not isinstance(v,bool):
            if not math.isfinite(v) or v<=0: raise ValueError(f'{k} must be finite and positive')
    d=derived(p); L,W=p['length'],p['width']; w=p['wall']
    def check(ok,msg):
        if not ok: raise ValueError(msg)
    check(w>=2.5 and p['floor']>=2.5,'minimum structural wall/floor 2.5 mm')
    check(p['lid_thickness']>=2,'lid minimum 2 mm')
    check(p['fin_count']>=2 and int(p['fin_count'])==p['fin_count'],'fin_count integer >=2')
    check(p['sink_length']>p['fin_count']*p['fin_thickness'],'fin spacing positive')
    check((p['sink_length']-p['fin_count']*p['fin_thickness'])/(p['fin_count']-1)>=3,'fin channel requires 3 mm cutter')
    check(p['pocket_radius']>=3,'main pocket requires radius >=3 mm')
    check(p['corner_radius']<min(L,W)/2 and p['pocket_radius']<min(L-2*w,W-2*w)/2,'radii fit rectangles')
    check(d['body']>d['ped_z']+1,'thermal pedestal must have positive depth')
    check(d['body']>=d['chip_z']+p['component_height']+p['minimum_clearance'],'component to lid clearance')
    check(0<p['pad_compressed']<p['pad_free'],'pad must be compressed')
    for origin,size,total in [(p['board_x'],p['board_length'],L),(p['board_y'],p['board_width'],W)]:
        check(origin>=w+p['minimum_clearance'] and origin+size<=total-w-p['minimum_clearance'],'PCB wall clearance')
    check(p['board_hole_pitch_x']<p['board_length'] and p['board_hole_pitch_y']<p['board_width'],'PCB pitch within board')
    check((p['board_length']-p['board_hole_pitch_x'])/2-p['board_hole_diameter']/2>=2,'PCB X hole edge ligament')
    check((p['board_width']-p['board_hole_pitch_y'])/2-p['board_hole_diameter']/2>=2,'PCB Y hole edge ligament')
    for x,y in d['pcb_holes']:
        check(min(x,y,L-x,W-y)>=w+p['support_radius'],'PCB boss wall separation')
        for a,b in d['lid_holes']:
            check(math.hypot(a-x,b-y)>p['support_radius']+p['lid_boss_radius'],'PCB and lid boss collision')
    check(p['lid_screw_inset']>=p['lid_boss_radius'],'lid boss fits outline')
    check(p['lid_screw_inset']-p['lid_boss_radius']<w,'lid bosses must join walls')
    check(p['lid_boss_radius']-p['lid_tap_drill']/2>=2,'lid boss ligament')
    check(p['lid_screw_clearance']>=3.2,'M3 screw clearance')
    check(p['board_hole_diameter']>=2.6,'M2.5 screw clearance')
    check(p['connector_radius']>=1.5 and 2*p['connector_radius']<min(p['connector_width'],p['connector_height']),'connector cutter radius')
    check(p['connector_x']>=12 and p['connector_x']+p['connector_width']<=L-12,'connector end ligament')
    check(p['connector_bottom']>=p['floor']+2 and p['connector_bottom']+p['connector_height']<=d['body']-2,'connector top/bottom ligament')
    check(p['sink_length']>=p['chip_length'] and p['sink_width']>=p['chip_width'],'pedestal covers chip')
    check(p['sink_length']<L-2*w and p['sink_width']<W-2*w,'heatsink within lid')
    check(p['fan_pitch']>p['sink_length'] and p['fan_pitch']>p['sink_width'],'fan holes outside fins')
    check(p['fan_size']<min(L,W)-2*w and p['fan_pitch']<p['fan_size']-4,'fan fits lid')
    check(p['mount_pitch']+p['mount_hole_diameter']<L-2*w,'mount hole edge distance')
    check(p['support_height']>=2.5+p['minimum_clearance']/2,'mount bolt head below PCB')
    return d

def box(l,w,h,x=0,y=0,z=0):
    return cq.Workplane('XY').box(l,w,h,centered=(False,False,False)).translate((x,y,z))

def rounded(l,w,h,r,x=0,y=0,z=0):
    return box(l,w,h,x,y,z).edges('|Z').fillet(r)

def cyl(r,h,x,y,z=0):
    return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z))

def build(p):
    d=validate_parameters(p); L,W=p['length'],p['width']; b=d['body']; w=p['wall']
    base=rounded(L,W,b,p['corner_radius'])
    island=10.0
    outline=[(island,w),(L-island,w),(L-island,island),(L-w,island),(L-w,W-island),(L-island,W-island),(L-island,W-w),(island,W-w),(island,W-island),(w,W-island),(w,island),(island,island)]
    pocket=cq.Workplane('XY').polyline(outline).close().extrude(b).edges('|Z').fillet(p['pocket_radius']).translate((0,0,p['floor']))
    base=base.cut(pocket)
    for x,y in d['lid_holes']:
        base=base.cut(cyl(p['lid_tap_drill']/2,8,x,y,b-7))
    for x,y in d['pcb_holes']:
        base=base.union(cyl(p['support_radius'],p['support_height'],x,y,p['floor']))
        base=base.cut(cyl(p['pcb_tap_drill']/2,4.5,x,y,d['board_z']-4))
    for x,y in d['mounts']: base=base.cut(cyl(p['mount_hole_diameter']/2,p['floor']+2,x,y,-1))
    # Rounded rectangle in XZ, extruded through front (Y=0) wall.
    opening=rounded(p['connector_width'],p['connector_height'],w+2,p['connector_radius'])
    opening=opening.rotate((0,0,0),(1,0,0),90).translate((p['connector_x'],w+1,p['connector_bottom']))
    base=base.cut(opening)
    lid=rounded(L,W,p['lid_thickness'],p['corner_radius'],z=b)
    pedestal=rounded(p['sink_length'],p['sink_width'],b-d['ped_z'],3,L/2-p['sink_length']/2,W/2-p['sink_width']/2,d['ped_z'])
    lid=lid.union(pedestal)
    for i in range(p['fin_count']):
        x=L/2-p['sink_length']/2+i*(p['sink_length']-p['fin_thickness'])/(p['fin_count']-1)
        lid=lid.union(box(p['fin_thickness'],p['sink_width'],p['fin_height'],x,W/2-p['sink_width']/2,b+p['lid_thickness']))
    for x,y in d['lid_holes']: lid=lid.cut(cyl(p['lid_screw_clearance']/2,4,x,y,b-1))
    # Optional fan uses four loose 6 mm spacers, not permanent mounting towers.
    for x,y in d['fan_holes']: lid=lid.cut(cyl(1.7,4,x,y,b-1))
    pcb=box(p['board_length'],p['board_width'],p['board_thickness'],p['board_x'],p['board_y'],d['board_z'])
    for x,y in d['pcb_holes']: pcb=pcb.cut(cyl(p['board_hole_diameter']/2,4,x,y,d['board_z']-1))
    chip=box(p['chip_length'],p['chip_width'],p['chip_height'],L/2-p['chip_length']/2,W/2-p['chip_width']/2,d['chip_z'])
    tim=box(p['chip_length'],p['chip_width'],p['pad_compressed'],L/2-p['chip_length']/2,W/2-p['chip_width']/2,d['pad_z'])
    # Actual assumed connector envelope is inset 0.75 on all XZ sides.
    connector=box(p['connector_width']-1.5,p['board_y']+2,p['connector_height']-1.5,p['connector_x']+.75,-2,p['connector_bottom']+.75)
    # Secondary component keep-out: X=70..82, Y=26..44; configurable board-relative position.
    components=box(12,18,p['component_height'],p['board_x']+p['board_length']-20,W/2-9,d['chip_z'])
    parts={'base':base,'thermal_lid':lid,'pcb':pcb,'chip':chip,'thermal_pad':tim,'connector':connector,'component_keepout':components}
    for i,(x,y) in enumerate(d['lid_holes']):
        # Root-diameter shaft, not an explicit thread. M3x8 under-head length.
        parts[f'lid_screw_{i+1}']=cyl(1.2,8,x,y,b+p['lid_thickness']-8).union(cyl(2.75,2,x,y,b+p['lid_thickness']))
    for i,(x,y) in enumerate(d['pcb_holes']):
        parts[f'pcb_screw_{i+1}']=cyl(.95,5,x,y,d['chip_z']-5).union(cyl(2.25,1.7,x,y,d['chip_z']))
    if p['fan_enabled']:
        fan=box(p['fan_size'],p['fan_size'],p['fan_height'],L/2-p['fan_size']/2,W/2-p['fan_size']/2,p['height'])
        fan=fan.cut(cyl(p['fan_size']/2-3,p['fan_height']+2,L/2,W/2,p['height']-1))
        for i,(x,y) in enumerate(d['fan_holes']):
            fan=fan.cut(cyl(1.7,p['fan_height']+2,x,y,p['height']-1))
            parts[f'fan_spacer_{i+1}']=cyl(3,p['fin_height'],x,y,b+p['lid_thickness']).cut(cyl(1.7,p['fin_height']+2,x,y,b+p['lid_thickness']-1))
        parts['fan_envelope']=fan
    return parts

def fixture(p):
    L,W=p['length'],p['width']
    plate=rounded(L+30,W+30,6,3,-15,-15,-10)
    points=[(18,12),(L-18,12),(L/2,W-12),(20,-3),(L-20,-3),(-3,W/2)]
    parts={}
    for i,(x,y) in enumerate(points):
        plate=plate.cut(cyl(1.65,8,x,y,-11))
        h=4 if i<3 else 9
        parts[f'locator_{i+1}']=cyl(3,h,x,y,-4).union(cyl(1.5,10,x,y,-14))
    # Two low lateral clamp blocks: threaded bores and sliding pads simplified.
    clamp_y=box(24,6,10,L/2-12,W+5,-4)
    clamp_x=box(6,24,10,L+5,W/2-12,-4)
    for x,y in [(L/2-8,W+8),(L/2+8,W+8),(L+8,W/2-8),(L+8,W/2+8)]:
        plate=plate.cut(cyl(1.65,8,x,y,-11))
        clamp_y=clamp_y.cut(cyl(2.25,12,x,y,-5))
        clamp_x=clamp_x.cut(cyl(2.25,12,x,y,-5))
    # Horizontal M4 tapping pilots; pads and screws are conceptual, no thread geometry.
    ybore=cyl(1.65,8,0,0).rotate((0,0,0),(1,0,0),90).translate((L/2,W+12,1.5))
    xbore=cyl(1.65,8,0,0).rotate((0,0,0),(0,1,0),90).translate((L+4,W/2,1.5))
    parts['fixture_plate']=plate
    parts['clamp_y']=clamp_y.cut(ybore)
    parts['clamp_x']=clamp_x.cut(xbore)
    parts['clamp_pad_y']=box(10,5,3,L/2-5,W,0)
    parts['clamp_pad_x']=box(5,10,3,L,W/2-5,0)
    return parts
