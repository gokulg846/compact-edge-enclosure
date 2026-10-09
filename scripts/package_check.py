"""Deliverable completeness, PDF structure and export manifest checks."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from pypdf import PdfReader
import ezdxf

def main():
 expected={'report/engineering-report.pdf':8,'report/portfolio-summary.pdf':1,'drawings/drawing-package.pdf':5}
 check={}
 for file,count in expected.items():
  doc=PdfReader(ROOT/file);texts=[p.extract_text() or '' for p in doc.pages]
  assert len(doc.pages)==count,(file,len(doc.pages),count)
  assert all(len(t)>100 for t in texts),(file,'blank page')
  assert not any('\u25a0' in t for t in texts),(file,'missing glyph square')
  check[file]={'pages':len(doc.pages),'bytes':(ROOT/file).stat().st_size,'text_present':True}
 for name in ['base_section','thermal_lid_section']:
  doc=ezdxf.readfile(ROOT/'exports'/f'{name}.dxf');audit=doc.audit();assert not audit.has_errors
  check[name+'.dxf']={'entities':len(doc.modelspace()),'audit_errors':len(audit.errors)}
 for file in (ROOT/'images').glob('*.svg'):ET.parse(file)
 for file in ['cad/model.py','cad/enclosure.scad','cad/generated_parameters.scad','manufacturing/cnc/setup-plan.md','manufacturing/printing/print-plan.md','fixture/README.md','drawings/inspection-plan.md','report/application-email.txt','report/walkthrough.md']:
  assert (ROOT/file).stat().st_size>50,file
 check['status']='PASS'
 (ROOT/'results/package-check.json').write_text(json.dumps(check,indent=2)+'\n')
 manifest={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for folder in ['cad','exports','drawings','manufacturing','fixture','analysis','scripts','tests','images','report'] for f in (ROOT/folder).rglob('*') if f.is_file() and '__pycache__' not in f.parts}
 (ROOT/'results/manifest.sha256').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(manifest.items())))
 paths=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','.venv','.cache','.pytest_cache','__pycache__','tmp']) and p.name!='file-inventory.txt']
 (ROOT/'results/file-inventory.txt').write_text('\n'.join(sorted(paths)+['results/file-inventory.txt'])+'\n')
 print(json.dumps(check,indent=2))
if __name__=='__main__':main()
