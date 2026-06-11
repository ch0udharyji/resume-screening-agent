# Resume Screening Agent
An AI agent that compares a candidate's resume against a job description, scores
the fit out of 100, lists matched and missing skills, and suggests how to close
the gaps. Built with Python, Streamlit, and the Anthropic API.
![screenshot placeholder — add a screenshot of the app here]
What it does

Takes a resume and a job description as input
Uses an LLM with structured (JSON) output to score the match
Returns: fit score, matched skills, missing skills, concrete gap-closing advice, and a summary
Runs as a simple web app in the browser

Skills demonstrated

LLM prompting with structured output
Building an agent workflow (input → reasoning → structured result → UI)
Streamlit app development

Run it locally

Install the dependencies:

   pip install -r requirements.txt

Get an API key from console.anthropic.com.
Run the app:

   streamlit run app.py

Paste your API key into the app, add a resume and a job description, and click Screen the candidate.

Tech stack
Python · Streamlit · Anthropic API
