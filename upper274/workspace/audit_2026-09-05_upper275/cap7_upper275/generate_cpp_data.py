#!/usr/bin/env python3
from pathlib import Path
import runpy,sys
sys.argv=[str(Path(__file__).with_name('generate_step_data.py')),'276']
runpy.run_path(sys.argv[0],run_name='__main__')
