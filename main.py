from pathlib import Path
from typing import Dict, List, Literal
import csv, io, json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from engine import PIS, ASSESSMENTS, calculate

app = FastAPI(title='ABET Initial CO–SO Mapper', version='1.0.0', description='Curriculum-based PI mapping, distinct from attainment.')
BASE = Path(__file__).parent
app.mount('/static', StaticFiles(directory=BASE/'static'), name='static')

class CO(BaseModel):
    id: str
    description: str

class Selection(BaseModel):
    pis: List[str] = Field(default_factory=list)
    basis: Literal['syllabus','planned_activity',''] = ''
    rationale: str = ''
    assessments: List[str] = Field(default_factory=list)

class MappingRequest(BaseModel):
    course: str = ''
    syllabus: str = ''
    framework: Literal['CAC','EAC']
    cos: List[CO]
    selections: Dict[str,Selection] = Field(default_factory=dict)

@app.get('/health')
def health(): return {'status': 'ok'}

@app.get('/')
def home(): return FileResponse(BASE/'static'/'index.html')

@app.get('/api/frameworks')
def frameworks():
    return {'frameworks':{framework:{so:[{'id':f'{so}.{i}', 'description':d} for i,d in enumerate(items,1)] for so,items in outcomes.items()} for framework,outcomes in PIS.items()},'assessments':ASSESSMENTS,'thresholds':{'high':60,'moderate':50},'note':'Initial curriculum mapping only; not attainment.'}

@app.post('/api/map')
def map_course(payload: MappingRequest):
    if len({c.id for c in payload.cos}) != len(payload.cos): raise HTTPException(422,'Duplicate CO identifiers')
    try: return calculate(payload.framework,[c.model_dump() for c in payload.cos],{k:v.model_dump() for k,v in payload.selections.items()})
    except ValueError as e: raise HTTPException(422,str(e))

@app.post('/api/export/csv')
def export_csv(payload: MappingRequest):
    try: result=calculate(payload.framework,[c.model_dump() for c in payload.cos],{k:v.model_dump() for k,v in payload.selections.items()})
    except ValueError as e: raise HTTPException(422,str(e))
    output=io.StringIO(); writer=csv.writer(output)
    sos=list(PIS[payload.framework]); writer.writerow(['CO','Course Outcome']+sos)
    for row in result['rows']: writer.writerow([row['co'],row['description']]+[row['outcomes'][so]['correlation'] for so in sos])
    writer.writerow(['Average (nonzero)','']+[result['averages'][so] if result['averages'][so] is not None else '—' for so in sos]); writer.writerow([])
    writer.writerow(['CO','SO','Selected PIs','PI coverage %','Correlation','Basis','Justification','Assessment opportunities'])
    for row in result['rows']:
        for so,entry in row['outcomes'].items():
            writer.writerow([row['co'],so,', '.join(entry['pis']),entry['coverage'],entry['correlation'],entry['basis'],entry['rationale'],', '.join(entry['assessments'])])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]),media_type='text/csv; charset=utf-8',headers={'Content-Disposition':f'attachment; filename="{payload.framework.lower()}_co_so_mapping.csv"'})
