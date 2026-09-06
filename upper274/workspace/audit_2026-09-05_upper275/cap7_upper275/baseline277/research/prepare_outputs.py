#!/usr/bin/env python3
"""Seed an output directory with the recorded ordinary stages for downstream discovery."""
from pathlib import Path
import shutil
D=Path(__file__).resolve().parent;out=D/'outputs';out.mkdir(exist_ok=True)
p=out/'new_certificate.json'
if p.exists():print('Existing output retained:',p)
else:shutil.copy2(D/'recorded/new_certificate.json',p);print('Seeded ordinary-stage checkpoint:',p)
