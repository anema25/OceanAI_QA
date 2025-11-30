# backend/app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os, tempfile, json
from .ingest import chunk_and_index
from .retrieval import retrieve
from .llm_prompts import TESTCASE_PROMPT, SELENIUM_PROMPT

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/ingest")
async def ingest(files: list[UploadFile] = File(...)):
    count = 0
    for f in files:
        path = os.path.join(UPLOAD_DIR, f.filename)
        with open(path, "wb") as out:
            out.write(await f.read())
        count += chunk_and_index(path)
    return {"status":"ok","chunks_indexed":count}

@app.post("/generate_testcases")
async def generate_testcases(query: str = Form(...)):
    # retrieve context
    docs = retrieve(query, k=6)
    context = "\n\n".join([f"Source: {d['meta']['source_document']}\n{d['text']}" for d in docs])
    prompt = TESTCASE_PROMPT.format(query=query, context=context)
    # CALL LLM: replace with your LLM call. Must return a JSON array.
    llm_result = call_llm(prompt)   # implement call_llm
    # validate JSON
    try:
        parsed = json.loads(llm_result)
    except Exception as e:
        return {"error":"LLM did not return valid JSON","raw":llm_result}
    return {"testcases": parsed}

@app.post("/generate_script")
async def generate_script(testcase_json: str = Form(...)):
    testcase = json.loads(testcase_json)
    # retrieve html file content from uploaded directory
    html_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.html')]
    if not html_files:
        return {"error":"No checkout.html uploaded"}
    html_path = os.path.join(UPLOAD_DIR, html_files[0])
    with open(html_path,'r',encoding='utf-8') as fh: html = fh.read()
    # retrieve context for grounding
    docs = retrieve(testcase.get('Test_Scenario',''), k=6)
    context = "\n\n".join([f"Source: {d['meta']['source_document']}\n{d['text']}" for d in docs])
    prompt = SELENIUM_PROMPT.format(testcase=json.dumps(testcase,indent=2), html=html, context=context)
    script = call_llm(prompt)   # implement call_llm to return the Python script
    return {"script": script}
