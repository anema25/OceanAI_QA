# streamlit_app/app.py
import streamlit as st
import requests, json, os

API_BASE = st.secrets.get("API_BASE","http://localhost:8000")

st.title("Autonomous QA Agent — Test Case & Script Generation")

with st.sidebar:
    st.header("Upload Assets")
    uploaded = st.file_uploader("Upload support documents and checkout.html (md,txt,json,html)", accept_multiple_files=True)
    if st.button("Upload and Ingest"):
        files = uploaded
        if not files: st.warning("Add files first"); st.stop()
        files_payload = []
        for f in files:
            files_payload.append(("files", (f.name, f.getvalue(), f.type)))
        resp = requests.post(API_BASE + "/ingest", files=files_payload)
        st.write(resp.json())

st.header("Agent")
query = st.text_area("Enter request (e.g., Generate all positive and negative test cases for the discount code feature.)")
if st.button("Generate Test Cases"):
    resp = requests.post(API_BASE + "/generate_testcases", data={"query": query})
    if resp.status_code==200:
        out = resp.json()
        if "testcases" in out:
            st.success("Test cases generated")
            st.write(out["testcases"])
            st.session_state['testcases']=out['testcases']
        else:
            st.error(out)
    else:
        st.error(resp.text)

if 'testcases' in st.session_state:
    st.header("Select Test Case to Generate Script")
    tc = st.selectbox("Select", options=st.session_state['testcases'], format_func=lambda t: t.get("Test_ID")+": "+t.get("Feature"))
    if st.button("Generate Selenium Script for selected TC"):
        resp = requests.post(API_BASE + "/generate_script", data={"testcase_json": json.dumps(tc)})
        if resp.status_code==200:
            st.code(resp.json().get("script",""), language="python")
