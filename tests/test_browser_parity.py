import copy
import json
import subprocess
import unittest
from test_validation import ROOT, validate

class BrowserParity(unittest.TestCase):
    def test_browser_matches_python_and_preserves_sources(self):
        base=json.loads((ROOT/'data/fictional_study.json').read_text())
        cases=[base]
        duplicate=copy.deepcopy(base)
        duplicate['subjects'].append(copy.deepcopy(duplicate['subjects'][0]))
        cases.append(duplicate)
        for value in ['1970-01-01','0000-01-01','2026-02-30']:
            sample=copy.deepcopy(base)
            sample['subjects'][0]['consent']=value
            sample['subjects'][0]['visits'][0]['date']=value
            cases.append(sample)
        script="const m=require('./model.js');let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{const x=JSON.parse(s),before=JSON.stringify(x);const out=x.map(m.validate);if(before!==JSON.stringify(x))throw Error('Source mutated');process.stdout.write(JSON.stringify(out));});"
        result=subprocess.run(['node','-e',script],cwd=ROOT,input=json.dumps(cases),capture_output=True,text=True,encoding='utf-8',check=True)
        self.assertEqual(json.loads(result.stdout),[validate(x) for x in cases])
