import requests
from fastapi import FastAPI, HTTPException
import os
from fuzzywuzzy import fuzz_ratio 
from functions import *
import subprocess
with open('.env') as f:
    try:
        for line in f:
            l=line.split('=') 
            key,value = l[0],l[1]
            AIPROXY_TOKEN = value
            print(AIPROXY_TOKEN)
    except:
        print('Setup the enviroment variables')
app = FastAPI()
@app.get('/read')
async def read_file(path : str):
    if not path.startswith('/data'):
        raise HTTPException(status_code=403, detail='Access to file is not allowed')
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='File not found')
    file = open(path , 'r')
    content = file.read()
    return {'content':content}

@app.post('/run')
async def run_task(task :str):
    task_output = get_task_output(AIPROXY_TOKEN,task)
    task=task.lower()
    if "count" in task:
        day = extract_dayname(task)
        count_days(day)
    elif 'install' in task:
        pkgname = extract_package(task)
        correct_pkg = get_correct_pkgname(pkgname)
        if pkgname:
            subprocess.run(['pip','install',pkgname])
        else :
            return {"status":"Task is recognised but not implemented yet"}
        return {"status":"success","task_output":task_output}
