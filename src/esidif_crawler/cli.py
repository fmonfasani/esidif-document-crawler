import argparse
import asyncio
from .config import load_config
from .crawler import Crawler
from .storage import Storage, export_manifest

def main():
    parser=argparse.ArgumentParser(prog="esidif-crawler"); sub=parser.add_subparsers(dest="command",required=True)
    for name in ("audit","crawl"):
        p=sub.add_parser(name); p.add_argument("--config",default="config.yaml")
        if name=="crawl": p.add_argument("--download",action="store_true")
    p=sub.add_parser("export"); p.add_argument("--config",default="config.yaml"); p.add_argument("--output",default="data/manifests/documents.json")
    args=parser.parse_args(); config=load_config(args.config)
    if args.command in {"audit","crawl"}: print(asyncio.run(Crawler(config,getattr(args,"download",False)).run()))
    else:
        s=Storage(config.storage.database)
        try: print({"documents":export_manifest(s,args.output)})
        finally: s.close()

if __name__=="__main__": main()
