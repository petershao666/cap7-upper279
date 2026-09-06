"""Post-freeze exact catalogue and histogram comparison; no H generator import."""
import hashlib
import itertools
import json
from pathlib import Path

here=Path(__file__).resolve().parent
hdir=here.parents[1]/'hist105106'/'h20_20201'
own_freeze=json.loads((here/'FROZEN.json').read_text())
h_freeze=json.loads((hdir/'FROZEN.json').read_text())
for directory, files in [(here,own_freeze['files']),(hdir,h_freeze['artifacts'])]:
    for name, digest in files.items():
        assert hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest, name
own_centered=[line.split()[0] for line in (here/'CENTERED20_MASKS_COEFFICIENTS.txt').read_text().splitlines()]
h_centered=json.loads((hdir/'centered20.json').read_text())
assert own_centered==sorted(entry['mask'] for entry in h_centered['centered'])
assert (here/'ALL20_MASKS.txt').read_bytes()==(hdir/'all20_masks.txt').read_bytes()
own=json.loads((here/'HISTOGRAMS.json').read_text())
h=json.loads((hdir/'histograms41.json').read_text())
def vectors(packet):
    return {tuple(sorted((tuple(t),n) for t,n in zip(packet['types'],row['counts']) if n)) for row in packet['histograms']}
assert vectors(own)==vectors(h)
checks=0
for row in h['histograms']:
    cap=[tuple(p) for p in row['points']]
    assert len(cap)==len(set(cap))==41
    assert [sum(x*3**i for i,x in enumerate(p)) for p in cap]==row['point_ids']
    lookup=set(cap)
    for a,b in itertools.combinations(cap,2):
        assert tuple((-x-y)%3 for x,y in zip(a,b)) not in lookup
        checks+=1
    hist={}
    for d in itertools.product(range(3),repeat=5):
        if not any(d): continue
        counts=[0,0,0]
        for p in cap: counts[sum(x*y for x,y in zip(d,p))%3]+=1
        t=tuple(sorted(counts,reverse=True))
        hist[t]=hist.get(t,0)+1
    assert all(n%2==0 for n in hist.values())
    assert [hist.get(tuple(t),0)//2 for t in h['types']]==row['counts']
report={
    'status':'POST_FREEZE_COMPLETE_CATALOGUE_HISTOGRAM_AND_H_POINT_COMPARISON_PASS',
    'identical_centered_mask_count':len(own_centered),
    'all20_mask_files_byte_identical':True,
    'identical_complete_histogram_count':len(vectors(own)),
    'H_representative_pairs_checked':checks,
    'H_generator_imported':False,
    'P_freeze_preceded_H_output_read':True,
    'H_reported_timing_disclosure':h_freeze['method_independence'],
    'own_histograms_sha256':hashlib.sha256((here/'HISTOGRAMS.json').read_bytes()).hexdigest(),
    'H_histograms_sha256':hashlib.sha256((hdir/'histograms41.json').read_bytes()).hexdigest(),
}
(here/'H_COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
