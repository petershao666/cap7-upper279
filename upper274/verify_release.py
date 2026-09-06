#!/usr/bin/env python3
"""Portable exact replay of the published upper-274 certificate package.

The quick and final modes inherit older large-domain audits; neither claims to
independently reproduce published classification searches. Frozen sources are
never edited. All output-writing research helpers execute in a temporary copy.
"""
from pathlib import Path
import argparse, contextlib, hashlib, json, os, runpy, shutil, subprocess, sys, tempfile, time

HERE = Path(__file__).resolve().parent
R2_NAME = 'research_2026-09-05-upper274-continuation-r2'
R1_NAME = 'research_2026-09-05-capset-round1-r1'
ORIGINAL_ROOT = '/Users/hengshao/Desktop/math/'

def require(test, message):
    if not test:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def check_hashes():
    manifest = read(HERE/'SOURCE_MANIFEST.json')
    for row in manifest['files']:
        path = HERE/row['path']
        require(path.is_file(), 'Missing frozen source: '+row['path'])
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],
                'Frozen source mismatch: '+row['path'])
    actual = {str(p.relative_to(HERE)) for p in (HERE/'workspace').rglob('*') if p.is_file()}
    require(actual == {r['path'] for r in manifest['files']}, 'Unmanifested/missing workspace files')
    return {'status':'PASS', 'files':len(manifest['files']), 'bytes':sum(r['bytes'] for r in manifest['files'])}

def compile_cpp(source, binary, output, compiler):
    command = [compiler, '-O2', '-std=c++17', '-fsanitize=undefined',
               '-fno-sanitize-recover=all', str(source), '-o', str(binary)]
    cp = subprocess.run(command, capture_output=True, text=True, timeout=180)
    output.write_text(cp.stdout+cp.stderr)
    require(cp.returncode == 0, 'Compiler failed; see '+str(output))

def run_binary(binary, output, args=(), stdin=None, timeout=1200):
    err = output.with_suffix(output.suffix+'.stderr')
    with output.open('wb') as so, err.open('wb') as se:
        if stdin is not None:
            with stdin.open('rb') as si:
                cp = subprocess.run([str(binary), *map(str,args)], stdin=si, stdout=so, stderr=se, timeout=timeout)
        else:
            cp = subprocess.run([str(binary), *map(str,args)], stdin=subprocess.DEVNULL, stdout=so, stderr=se, timeout=timeout)
    require(cp.returncode == 0, 'Replay failed: '+str(output))
    require(not err.read_bytes(), 'Nonempty replay stderr: '+str(err))

def quick(work, output):
    source = work/R2_NAME/'root_audit/global274/verify.py'
    frozen = read(source.parent/'VERIFICATION.json')
    with (output/'global.stdout').open('w') as f, contextlib.redirect_stdout(f):
        runpy.run_path(str(source), run_name='__main__')
    fresh = read(source.parent/'VERIFICATION.json')
    require(fresh == frozen, 'Global integration differs from frozen result')
    shutil.copyfile(source.parent/'VERIFICATION.json', output/'global_result.json')
    return {'status':'PASS_EXACT_GLOBAL_INTEGRATION', 'global_upper':fresh['global_upper'],
            'remaining_minimum_states':fresh['remaining_minimum_states'],
            'inherited_r1_raw_rows_not_rerun':fresh['inherited_r1_raw_rows_not_rerun'],
            'scope':'Exact profile/state coverage and integer bridges; earlier large-domain audits inherited'}

def final(work, output, compiler):
    root = work/R2_NAME
    low = root/'root_audit/three40_complete42'
    nc = root/'root_potential/three40_complete42_nc106_verify'
    domains = root/'root_potential/complete41_domain_audit'
    print('Rebuilding and replaying final lower/outer C++ kernel...', flush=True)
    binary = output/'lower_outer.bin'
    compile_cpp(low/'verify.cpp', binary, output/'lower_outer.compile.log', compiler)
    stdout = output/'lower_outer.stdout'
    run_binary(binary, stdout, stdin=low/'input.txt')
    fresh, frozen = stdout.read_text().splitlines(), (low/'verify.log').read_text().splitlines()
    cases = [s for s in fresh if s.startswith('CASE ')]
    require(len(cases)==133 and cases==[s for s in frozen if s.startswith('CASE ')], 'Lower/outer CASE mismatch')
    require(fresh[-1].split(' seconds ')[0]==frozen[-1].split(' seconds ')[0], 'Lower/outer total mismatch')
    print('Rebuilding the 14 fully ordered NC106 domains...', flush=True)
    fresh_domains = output/'fresh_nc_domains'; fresh_domains.mkdir()
    binary = output/'domains.bin'
    compile_cpp(domains/'enumerate_domains.cpp', binary, output/'domains.compile.log', compiler)
    run_binary(binary, output/'domains.stdout', args=[domains/'INPUTS.txt',fresh_domains])
    counts=[]
    for i in range(14):
        name=f'case{i:02d}_new_raw.u8'; a=fresh_domains/name; b=domains/name
        require(sha(a)==sha(b), 'NC106 regenerated domain mismatch: '+name)
        require(a.stat().st_size%9==0, 'Malformed NC106 domain')
        counts.append(a.stat().st_size//9)
    require(sum(counts)==1106094, 'NC106 domain row count mismatch')
    print('Rebuilding and replaying the independent NC106 C++ kernel...', flush=True)
    binary=output/'nc106.bin'
    compile_cpp(nc/'replay_raw.cpp', binary, output/'nc106.compile.log', compiler)
    stdout=output/'nc106.stdout'
    run_binary(binary, stdout, args=[nc/'REPLAY_INPUT.txt',fresh_domains])
    a,b=read(stdout),read(nc/'RAW_VERIFICATION.json')
    require(a['cases']==b['cases'] and len(a['cases'])==14, 'NC106 case records mismatch')
    require(a['all_raw_count']==b['all_raw_count']==1106094, 'NC106 raw total mismatch')
    print('Recomputing finite-support arithmetic with the independent Python audit...', flush=True)
    source=work/'audit_2026-09-06_upper274/evidence/support_audit.py'
    code=source.read_text()
    # Three narrowly scoped portability substitutions: input root, output root,
    # and resolution of historical absolute paths embedded in hash inventories.
    old="R = Path('/Users/hengshao/Desktop/math/research_2026-09-05-upper274-continuation-r2')"
    require(code.count(old)==1, 'Unexpected support-audit input binding')
    code=code.replace(old,'R = RELEASE_ROOT')
    old='OUT = Path(__file__).resolve().parent'
    require(code.count(old)==1, 'Unexpected support-audit output binding')
    code=code.replace(old,'OUT = RELEASE_OUTPUT')
    old="p=Path(name) if name.startswith('/') else root/name"
    require(code.count(old)==1, 'Unexpected support-audit hash path binding')
    code=code.replace(old,'p=resolve_historical_path(name, root)')
    def resolve_historical_path(name, base):
        if name.startswith(ORIGINAL_ROOT): return work/name[len(ORIGINAL_ROOT):]
        require(not name.startswith('/'), 'Unmapped historical absolute path: '+name)
        return base/name
    with (output/'support.stdout').open('w') as f, contextlib.redirect_stdout(f):
        exec(compile(code,str(source),'exec'),{'__file__':str(source),'__name__':'__main__',
             'RELEASE_ROOT':root,'RELEASE_OUTPUT':output,'resolve_historical_path':resolve_historical_path})
    s=read(output/'support_audit.json')
    require(s['local_support_and_conditional_evaluations']==15885 and s['positive_gap']==148616699075,
            'Finite-support audit result mismatch')
    return {'status':'PASS_FINAL_RAW_DOMAINS_AND_SUPPORT', 'lower_outer_cases':133,
            'lower_outer_raw_rows':7701024, 'nc106_cases':14,'nc106_raw_rows':1106094,
            'total_final_raw_rows':8807118,'nc106_domains_rebuilt_byte_identically':True,
            'finite_support_evaluations':15885,'positive_gap':148616699075,
            'scope':'Fresh replay of previously independent kernels; shared frozen coefficients/classification data'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['quick','final'], default='quick')
    parser.add_argument('--output', type=Path, help='New directory for generated reports; default creates a temporary directory')
    parser.add_argument('--compiler', default=os.environ.get('CXX','c++'))
    args=parser.parse_args()
    require(__debug__, 'Run without Python -O: the frozen checkers contain assertions')
    started=time.monotonic()
    if args.output:
        output=args.output.expanduser().resolve()
        require(not output.exists(), '--output must be a new directory')
        require(not output.is_relative_to(HERE), '--output must be outside the frozen release package')
        output.mkdir(parents=True)
    else:
        output=Path(tempfile.mkdtemp(prefix='cap7-upper274-results-'))
    result={'mode':args.mode, 'frozen_source_hashes':check_hashes(),
            'claim':'f(7,3) <= 274, conditional on explicitly recorded low-dimensional premises',
            'not_a_complete_from_scratch_reproof':True}
    print('Frozen source hashes passed. Output: '+str(output), flush=True)
    with tempfile.TemporaryDirectory(prefix='cap7-upper274-work-') as temporary:
        work=Path(temporary).resolve()/'workspace'
        shutil.copytree(HERE/'workspace',work)
        result['global']=quick(work,output)
        print('Exact global profile/state integration passed.', flush=True)
        if args.mode=='final': result['final']=final(work,output,args.compiler)
    result['elapsed_seconds']=time.monotonic()-started
    result['status']='PASS'
    (output/'RELEASE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('Reports: '+str(output/'RELEASE_VERIFICATION.json'))

if __name__=='__main__':
    main()
