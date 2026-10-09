"""Fail-fast regeneration of the complete engineering package."""
import os,sys,subprocess,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))

def run(args,log=None):
 print('+',sys.executable,*args,flush=True)
 if log:
  with (ROOT/log).open('w') as out:
   result=subprocess.run([sys.executable,*args],stdout=out,stderr=subprocess.STDOUT)
  print((ROOT/log).read_text(),flush=True)
  result.check_returncode()
 else:subprocess.run([sys.executable,*args],check=True)

def main():
 for d in ['exports','drawings','images','results','report']:(ROOT/d).mkdir(exist_ok=True)
 run(['scripts/build.py'])
 run(['scripts/scad.py'])
 run(['analysis/thermal.py'],'results/thermal_console.txt')
 run(['scripts/validate.py'],'results/validation_console.txt')
 run(['-m','pytest','-q','--junitxml=results/tests.xml'],'results/tests.txt')
 run(['scripts/visuals.py'])
 run(['scripts/report.py'])
 run(['scripts/package_check.py'])
 print('Complete package generated. Review PDFs visually after any design/layout change.')
if __name__=='__main__':main()
