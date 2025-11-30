# backend/llm_prompts.py
TESTCASE_PROMPT = """
You are an expert QA engineer. Given the user query and the following context snippets (each labelled with its source), generate structured test cases (JSON array).
Constraints:
- All reasoning MUST be grounded in the provided snippets. Do not invent features.
- For each test case output: Test_ID, Feature, Test_Scenario, Steps (ordered), Inputs, Expected_Result, Grounded_In (source file).
User query: {query}
Context snippets:
{context}
Return only valid JSON.
"""

SELENIUM_PROMPT = """
You are a Selenium (Python) expert. Generate a runnable Python Selenium script for this selected test case.
Constraints:
- Use the provided checkout.html DOM (attached below) to choose selectors (IDs, names, or CSS selectors). Prefer IDs.
- Use standard Selenium imports and include comments.
- Do not invent new UI elements.
- Keep the script runnable against a local file path: e.g., driver.get("file:///absolute/path/to/checkout.html")
Provide only the Python code block (no extra text).
Selected Test Case (JSON):
{testcase}
checkout.html content:
{html}
Additional context snippets:
{context}
"""
