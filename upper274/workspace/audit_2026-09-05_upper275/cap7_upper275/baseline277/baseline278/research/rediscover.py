#!/usr/bin/env python3
"""Propose an integer local or root certificate using the proved lower-dimensional
inputs. Discovery uses NumPy/SciPy/Numba; the complete verifiers do not.

Examples:
  python3 research/rediscover.py --case 108 108 63 --status 1 1
  python3 research/rediscover.py --case 108 108 63 --status 0 0
  python3 research/rediscover.py --dimension 6 --case 44 43 22
  python3 research/rediscover.py --root 279

Output is a proposal with an exhaustive integer check on the discovery feature
family. Acceptance as a proof requires the corresponding geometric reduction
and independent complete verification. No further bound improvement is promised.
"""
from __future__ import annotations
import argparse,json,itertools
from pathlib import Path
import numpy as np
from engine import CERT,F6,old,enum,separate,separate_spectral,force,root
D=Path(__file__).resolve().parents[1]

def sub112(rows):
    return (rows[:,2]<=22)|((rows[:,0]<=40)&(rows[:,1]<=36))

def jsonable(x):
    if isinstance(x,np.integer):return int(x)
    if isinstance(x,np.floating):return float(x)
    if isinstance(x,np.ndarray):return x.tolist()
    raise TypeError(type(x).__name__)

def prior(stages,key):
    """A known case uses only its earlier stages. An unlisted case may use all
    completed stages, which are established results, never speculative cuts."""
    out=[];k=','.join(map(str,key))
    for stage in stages:
        if k in stage:break
        out.extend(old.parse_key(t) for t in stage)
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--case',nargs=3,type=int,metavar=('A','B','C'))
    group.add_argument('--root',type=int,metavar='SIZE')
    parser.add_argument('--dimension',type=int,choices=(6,7),default=7)
    parser.add_argument('--status',nargs='*',type=int,choices=(0,1),help='Statuses in order for the columns of sizes 103 through 108')
    parser.add_argument('--output',type=Path,help='Optional JSON output path')
    args=parser.parse_args();cert=json.loads((D/'certificate.json').read_text())
    seeds=[tuple(t) for t in cert['completion_seeds']]
    comp=seeds+[old.parse_key(t) for st in cert['completion_stages'] for t in st]
    univ=[t for t in comp if not sub112(np.asarray([t]))[0]]
    if args.root is not None:
        if args.dimension!=7:parser.error('--root currently handles dimension seven only')
        banned=[tuple(t) for t in cert['seven_seed_exclusions']]+[old.parse_key(t) for st in cert['seven_stages'] for t in st]
        rec,types,mix=root(args.root,banned)
        result={'target':args.root,'certificate':rec,'remaining_types':len(types),'feasible_relaxation_mixture':mix}
    else:
        key=tuple(args.case)
        if not key[0]>=key[1]>=key[2]>=0:parser.error('Require A >= B >= C >= 0')
        n=args.dimension
        if n==6:
            if args.status is not None:parser.error('--status is only supported in dimension seven')
            banned=F6+seeds+prior(cert['completion_stages'],key)
            arr,count=enum(key,n=6,top_forbidden=banned)
            rec=separate(arr[:,:7],force(key,6),121)
            if rec is None:rec=separate_spectral(arr,key,n=6)
            result={'dimension':6,'conditional_on':'cap not contained in a 112-cap','type':key,'raw_matrices':count,'feature_rows':len(arr),'certificate':rec}
        else:
            banned=[tuple(t) for t in cert['seven_seed_exclusions']]+prior(cert['seven_stages'],key)
            arr,count=enum(key,n=7,f6=F6+univ,top_forbidden=banned)
            mask=np.ones(len(arr),dtype=bool);features=[];totals=list(force(key));status=None
            if args.status is not None:
                eligible=[j for j,N in enumerate(key) if 103<=N<109]
                if len(args.status)!=len(eligible):parser.error(f'Expected {len(eligible)} status values for this type')
                status=[-1,-1,-1]
                for j,s in zip(eligible,args.status):
                    status[j]=s;types=arr[:,7+3*j:10+3*j]
                    if s:
                        mask &= sub112(types);fam=types[:,2]<=22;defect=112-key[j]
                        features.extend([fam.astype(np.int64),np.where(fam,22-types[:,2],0)])
                        totals.extend([56,11*defect])
                        if key[j]>=108:
                            features.append(np.where(~fam,40-types[:,0],0));totals.append(110*defect)
                    else:
                        for t in comp:mask &= ~np.all(types>=t,axis=1)
            rows=np.c_[arr[mask,:7],np.asarray(features).T[mask]] if features else arr[mask,:7]
            rec=separate(rows,np.asarray(totals),364)
            result={'dimension':7,'type':key,'status':status,'unrestricted_raw_matrices':count,'retained_feature_rows':len(rows),'certificate':rec}
    text=json.dumps(result,indent=2,default=jsonable)+'\n';print(text,end='')
    if args.output:args.output.write_text(text)
if __name__=='__main__':main()
