from pathlib import Path
import json,hashlib,csv
W=Path(__file__).resolve().parent;R=W.parents[1];H=R/'hist105106/fullraw41'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for directory in (W,H):
 f=json.loads((directory/'FROZEN.json').read_text());assert all(sha(directory/n)==v for n,v in f['files'].items())
ours=[list(map(int,l.split()))for l in (W/'CHECK_INPUT.txt').read_text().splitlines()];other=[list(map(int,l.split()))for l in (H/'point_rows.txt').read_text().splitlines()];assert other.pop(0)==[34345];assert ours==other and len(ours)==34345
op=json.loads((W/'HISTOGRAM_PACKET.json').read_text());hp=json.loads((H/'HISTOGRAMS.json').read_text());assert op['types']==hp['types'];oh={x['id']:tuple(x['counts'])for x in op['histograms']};hh={x['id']:tuple(x['counts'])for x in hp['histograms']};assert set(oh.values())==set(hh.values())and len(oh)==len(hh)==41
ol=[json.loads(l)for l in (W/'ROW_LEDGER.jsonl').read_text().splitlines()];hl=list(csv.DictReader((H/'ROW_LEDGER.tsv').open(),delimiter='\t'));assert len(ol)==len(hl)==34345
for o,h,p in zip(ol,hl,ours):
 assert o['index']==int(h['row_id'])==p[0]
 assert h['source_file']==f"Dim5_41_{['180617','180716'][o['file']]}_SetDim5Cap43_9And8_ExclPtCounts_Data.txt"
 assert o['source_line']==int(h['source_line'])and o['block_line']==int(h['header_line'])and o['kind']==h['shape']
 assert hashlib.sha256(bytes(p[10:])).hexdigest()==h['point_sha256']
 assert oh[o['histogram_id']]==hh[int(h['histogram_id'])]
res={'status':'FULL34345_POINT_ROWS_AND_ROW_HISTOGRAMS_EXACT_MATCH','rows':34345,'histograms':41,'point_rows_byte_identical':sha(W/'CHECK_INPUT.txt')==sha(H/'point_rows.txt'),'all_original_source_rows_and_headers_match':True,'every_row_histogram_matches':True,'own_freeze_sha256':sha(W/'FROZEN.json'),'producer_freeze_sha256':sha(H/'FROZEN.json'),'first_read_other_outputs':'Only after both freezes; no producer source decoder imported.','independence_boundary':'Independent workbook/primary-named-data decoder and homogeneous matrix arithmetic vs producer staticJava strings; both share raw source files and published format/coverage. C++ point checkers independently written.'}
(W/'INDEPENDENT_COMPARISON.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
