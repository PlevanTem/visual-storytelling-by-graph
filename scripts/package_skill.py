"""Export the complete local source delivery, excluding Git and Python caches."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT.parent/'visual-storytelling-by-graph-v0.2.0.zip');args=parser.parse_args()
    files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and not any(x in p.parts for x in ['.git','__pycache__','node_modules']) and p.suffix!='.pyc' and p.name!='MANIFEST.sha256']
    require_inside=lambda p:p.resolve().is_relative_to(ROOT.resolve())
    if args.output.resolve().is_relative_to(ROOT.resolve()):parser.error('Write the archive outside the source directory to avoid recursion.')
    if not all(require_inside(p) for p in files):raise ValueError('Source paths escaped root.')
    (ROOT/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files),encoding='utf-8');files.append(ROOT/'MANIFEST.sha256')
    with zipfile.ZipFile(args.output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(args.output) as z:assert z.testzip() is None
    digest=hashlib.sha256(args.output.read_bytes()).hexdigest();args.output.with_suffix(args.output.suffix+'.sha256').write_text(digest+'  '+args.output.name+'\n',encoding='utf-8')
    print(json.dumps({'archive':str(args.output),'files':len(files),'bytes':args.output.stat().st_size,'sha256':digest,'CRC':'pass'},indent=2))
if __name__=='__main__':main()
