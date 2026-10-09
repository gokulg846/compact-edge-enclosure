import sys,copy,math
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cad.model import parameters,validate_parameters,build,derived
from analysis.thermal import temperature,calculate

@pytest.mark.parametrize('key,value',[
 ('length',0),('width',-1),('height',float('nan')),('wall',2.49),('floor',2.49),
 ('lid_thickness',1.99),('board_length',99),('component_height',20),
 ('board_hole_pitch_x',79),('fin_count',1),('fin_count',2.5),('fin_thickness',5),
 ('connector_x',2),('connector_height',12),('pad_compressed',1.1),
 ('pocket_radius',2.99),('fan_pitch',20),('mount_pitch',99),('support_height',2)
])
def test_reject_bad_parameters(key,value):
 p=parameters();p[key]=value
 with pytest.raises(ValueError):validate_parameters(p)

def test_default_and_boundary():
 p=parameters();assert validate_parameters(p)['body']==17
 p['wall']=2.5;p['floor']=2.5;assert validate_parameters(p)

def test_changed_envelope_build():
 p=parameters();p['length']=110;p['width']=80;p['height']=28
 parts=build(p);assert all(s.val().isValid() for s in parts.values())
 assert parts['base'].val().BoundingBox().xlen==pytest.approx(110)

def test_component_clearance_boundary():
 p=parameters();d=derived(p);p['component_height']=d['body']-d['chip_z']-p['minimum_clearance']
 validate_parameters(p);p['component_height']+=.001
 with pytest.raises(ValueError):validate_parameters(p)

def test_thermal_independent_hand_calculation():
 assert temperature(8,35,.8,.5,6)==pytest.approx(93.4)
 assert temperature(8,35,.8,.5,2)==pytest.approx(61.4)
 assert temperature(0,35,.8,.5,2)==35
 assert temperature(8,45,.8,.5,2)-temperature(8,35,.8,.5,2)==pytest.approx(10)

@pytest.mark.parametrize('args',[(-1,35,.8,.5,6),(8,35,-.8,.5,6),(8,float('inf'),.8,.5,6)])
def test_thermal_bad_inputs(args):
 with pytest.raises(ValueError):temperature(*args)

def test_worst_case_stack():
 s=calculate()['pad_stack_mm'];assert s['gap_min']==pytest.approx(.31);assert s['gap_max']==pytest.approx(.69)
 assert s['compression_min_pct']>25;assert s['compression_max_pct']<75

def test_passive_does_not_meet_screen():
 d=calculate();assert not d['configurations']['passive']['target_met_nominal'];assert d['configurations']['forced']['target_met_nominal']

def test_empty_repeatability_is_not_a_pass(tmp_path):
 from scripts.repeatability import analyze
 p=tmp_path/'empty.csv';p.write_text('operator,trial,x_mm,y_mm,z_mm\n')
 with pytest.raises(ValueError,match='No measurements'):analyze(p)

def test_repeatability_arithmetic_on_synthetic_unit_fixture(tmp_path):
 # Explicitly synthetic unit-test data, never emitted as physical evidence.
 from scripts.repeatability import analyze
 p=tmp_path/'synthetic.csv';p.write_text('operator,trial,x_mm,y_mm,z_mm\n'+''.join(f'{op},{i},{i*.001},{i*.001},0\n' for op in ['A','B'] for i in range(10)))
 result=analyze(p)
 assert result['A']['x_mm']['range']==pytest.approx(.009)
 assert result['combined']['x_mm']['operator_mean_shift']==0
 assert result['combined']['x_mm']['pooled_target_met']

def test_repeatability_rejects_insufficient_trials(tmp_path):
 from scripts.repeatability import analyze
 p=tmp_path/'short.csv';p.write_text('operator,trial,x_mm,y_mm,z_mm\nA,1,0,0,0\n')
 with pytest.raises(ValueError,match='two operators'):analyze(p)
