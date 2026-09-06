from pathlib import Path
import sys, subprocess, json, hashlib, time, runpy, contextlib

ROOT=Path('/Users/hengshao/Desktop/math')
R=ROOT/'research_2026-09-05-upper274-continuation-r2'
OUT=Path('/private/tmp/cap274-review-20260906')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
mode=sys.argv[1]
start=time.monotonic()
if mode=='global':
    source=R/'root_audit/global274/verify.py'
    original_write=Path.write_text
    def redirect(p, data, *args, **kwargs):
        assert p==source.parent/'VERIFICATION.json',str(p)
        return original_write(OUT/'global_replay.json',data,*args,**kwargs)
    Path.write_text=redirect
    try:
        with (OUT/'global_replay.log').open('w') as f, contextlib.redirect_stdout(f):
            runpy.run_path(str(source),run_name='__main__')
    finally:
        Path.write_text=original_write
    fresh=json.loads((OUT/'global_replay.json').read_text())
    frozen=json.loads((source.parent/'VERIFICATION.json').read_text())
    assert fresh==frozen
    result={'status':'PASS','same_as_frozen':True,'original_source_sha256':sha(source),
            'original_source_unmodified':True,'output_only_redirected':True,
            'checks':'Original exact global bridge rerun; not an independently implemented checker',
            'global_upper':fresh['global_upper'],'remaining':fresh['remaining_minimum_states']}
elif mode in ('lower_outer','nc106'):
    if mode=='lower_outer':
        directory=R/'root_audit/three40_complete42'
        source=directory/'verify.cpp'
        input_file=directory/'input.txt'
    else:
        directory=R/'root_potential/three40_complete42_nc106_verify'
        source=directory/'replay_raw.cpp'
        input_file=directory/'REPLAY_INPUT.txt'
    executable=OUT/(mode+'.bin')
    compile_cmd=['c++','-O2','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all',str(source),'-o',str(executable)]
    cp=subprocess.run(compile_cmd,capture_output=True,text=True,timeout=120)
    (OUT/(mode+'.compile.log')).write_text(cp.stdout+cp.stderr)
    assert cp.returncode==0,cp.stderr
    command=[str(executable)]
    if mode=='nc106': command += [str(input_file),str(R/'root_potential/complete41_domain_audit')]
    with input_file.open('rb') as fi,(OUT/(mode+'.stdout')).open('wb') as fo,(OUT/(mode+'.stderr')).open('wb') as fe:
        cp=subprocess.run(command,stdin=fi if mode=='lower_outer' else subprocess.DEVNULL,stdout=fo,stderr=fe,timeout=650)
    assert cp.returncode==0,cp.returncode
    assert not (OUT/(mode+'.stderr')).read_bytes()
    result={'status':'PASS','source_sha256':sha(source),'input_sha256':sha(input_file),
            'compiler_command':compile_cmd,'undefined_behavior_sanitizer':True,
            'kernel_provenance':'Fresh build and replay of previously independent research verifier; shared source and frozen inputs disclosed'}
    if mode=='lower_outer':
        fresh=(OUT/(mode+'.stdout')).read_text().splitlines()
        frozen=(directory/'verify.log').read_text().splitlines()
        a=[s for s in fresh if s.startswith('CASE ')]
        b=[s for s in frozen if s.startswith('CASE ')]
        assert len(a)==133 and a==b
        assert fresh[-1].split(' seconds ')[0]==frozen[-1].split(' seconds ')[0]
        result.update(cases=133,raw_rows=7701024,case_records_equal=True,summary=fresh[-1])
    else:
        fresh=json.loads((OUT/(mode+'.stdout')).read_text())
        frozen=json.loads((directory/'RAW_VERIFICATION.json').read_text())
        assert fresh['cases']==frozen['cases'] and len(fresh['cases'])==14
        assert fresh['all_raw_count']==frozen['all_raw_count']==1106094
        result.update(cases=14,raw_rows=fresh['all_raw_count'],case_records_equal=True)
else: raise ValueError(mode)
result['elapsed_seconds']=time.monotonic()-start
(OUT/(mode+'_result.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
