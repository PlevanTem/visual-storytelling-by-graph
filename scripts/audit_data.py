"""Non-destructive CSV inspection. Standard library only; no semantic inference."""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

MISSING={'','na','n/a','null','none','nan'}

def audit(path,encoding='utf-8-sig'):
    with Path(path).open(encoding=encoding,newline='') as f:
        reader=csv.reader(f)
        try: headers=next(reader)
        except StopIteration: raise ValueError('CSV is empty: no header.')
        if not headers or any(not h.strip() for h in headers):raise ValueError('Header contains an empty column name.')
        if len(set(headers))!=len(headers):raise ValueError('Duplicate column names make the schema ambiguous.')
        rows=list(reader)
    ragged=[i+2 for i,r in enumerate(rows) if len(r)!=len(headers)]
    cols={}
    for j,h in enumerate(headers):
        vals=[r[j].strip() if j<len(r) else '' for r in rows]
        present=[v for v in vals if v.lower() not in MISSING]
        nums=[]; nonfinite=0; nonnumeric=0
        for v in present:
            try:
                n=float(v)
                if math.isfinite(n):nums.append(n)
                else:nonfinite+=1
            except ValueError:nonnumeric+=1
        cols[h]={'missing':len(vals)-len(present),'distinct_non_missing':len(set(present)),
                 'finite_numeric':len(nums),'non_finite_numeric':nonfinite,'non_numeric':nonnumeric,
                 'candidate_type':'empty' if not present else 'numeric_like' if len(nums)==len(present) else 'mixed_or_text',
                 'minimum':min(nums) if nums else None,'maximum':max(nums) if nums else None}
    return {'file':Path(path).name,'rows':len(rows),'columns':cols,
            'duplicate_rows':sum(n-1 for n in Counter(tuple(r) for r in rows).values()),
            'ragged_row_lines':ragged,'semantics':'Not inferred: identifiers, units, denominator, pairing, causal structure.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('--encoding',default='utf-8-sig');parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.output and args.input.resolve()==args.output.resolve():parser.error('Output must not overwrite the input.')
    try:result=audit(args.input,args.encoding)
    except (OSError,ValueError,UnicodeError,csv.Error) as e:parser.exit(1,f'Audit failed: {e}\n')
    content=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(content,encoding='utf-8')
    else:print(content,end='')

if __name__=='__main__':main()
