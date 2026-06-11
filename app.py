"""
Resume Screening Agent
----------------------
Paste a candidate's resume and a job description. The agent compares them,
scores the fit, lists matched and missing skills, and suggests how to close
the gaps. Built with Streamlit + the Anthropic API.

Run locally with:  streamlit run app.py
"""

import os
import sys
import time
import json
import streamlit as st
import streamlit.runtime
import anthropic
from dotenv import load_dotenv

if not streamlit.runtime.exists():
    print("[Error]: Streamlit apps cannot be run directly with python.")
    print("[Info]: Please run this app using: streamlit run app.py")
    sys.exit(1)

load_dotenv()

# ---- Page setup -------------------------------------------------------------
st.set_page_config(page_title="Resume Screening Agent", layout="centered")

@st.dialog("Candidate Fit Analysis", width="large")
def show_analysis_modal(result):
    score = result.get("fit_score", 0)
    st.metric("Fit score", f"{score} / 100")
    st.progress(score / 100)
    st.subheader(result.get("verdict", ""))

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Matched Skills", "Missing Skills", "Gap Analysis"])
    
    with tab1:
        st.info(result.get("summary", ""))
    
    with tab2:
        for s in result.get("matched_skills", []):
            st.markdown(f"- {s}")
            
    with tab3:
        for s in result.get("missing_skills", []):
            st.markdown(f"- {s}")
            
    with tab4:
        for g in result.get("gaps", []):
            st.markdown(f"- {g}")

    st.divider()

    # ---- Download Report --------------------------------------------
    report_md = f"# Resume Screening Report\n\n**Fit Score**: {score} / 100\n**Verdict**: {result.get('verdict', '')}\n\n## Summary\n{result.get('summary', '')}\n\n## Matched Skills\n"
    for s in result.get("matched_skills", []):
        report_md += f"- {s}\n"
    report_md += "\n## Missing Skills\n"
    for s in result.get("missing_skills", []):
        report_md += f"- {s}\n"
    report_md += "\n## Gap Analysis\n"
    for g in result.get("gaps", []):
        report_md += f"- {g}\n"

    st.download_button(
        label="Download Report (Markdown)",
        data=report_md,
        file_name="screening_report.md",
        mime="text/markdown",
        use_container_width=True
    )


# ---- Helper Function --------------------------------------------------------
def extract_text_from_file(uploaded_file):
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("File is too large. Please upload a file smaller than 5MB.")
        return ""
    
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except ImportError:
            st.error("Please install pypdf to read PDF files.")
    elif uploaded_file.name.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            st.error("Please install python-docx to read DOCX files.")
    else:
        text = uploaded_file.getvalue().decode("utf-8")
    return text

# ---- The agent's instructions -----------------------------------------------
PROMPT = """You are an expert technical recruiter. Compare the candidate's resume \
against the job description and assess how well they fit.

Return ONLY valid JSON (no markdown fences, no preamble) in exactly this shape:
{{
  "fit_score": <integer from 0 to 100>,
  "verdict": "<one short sentence summarizing the fit>",
  "matched_skills": ["skills the candidate clearly has that the job wants"],
  "missing_skills": ["important skills the job wants that are absent or weak"],
  "gaps": ["each item: a specific gap AND a concrete way the candidate could close it"],
  "summary": "<2-3 sentence overall assessment for the hiring manager>"
}}

RESUME:
{resume}

JOB DESCRIPTION:
{job_desc}
"""

st.title("Resume Screening Agent")
st.caption("Compares a resume against a job description — scores the fit and flags the gaps.")
st.markdown("---")

# ---- AI Provider & API key --------------------------------------------------
col_prov, col_key = st.columns([1, 2])
with col_prov:
    provider = st.selectbox("AI Provider", ["Anthropic (Claude)", "OpenAI (GPT-4o)", "Google (Gemini)"])

if provider == "Anthropic (Claude)":
    env_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    key_label = "Your Anthropic API key"
    help_text = "Get one at console.anthropic.com."
elif provider == "OpenAI (GPT-4o)":
    env_api_key = os.environ.get("OPENAI_API_KEY", "")
    key_label = "Your OpenAI API key"
    help_text = "Get one at platform.openai.com."
else:
    env_api_key = os.environ.get("GEMINI_API_KEY", "")
    key_label = "Your Google Gemini API key"
    help_text = "Get one at aistudio.google.com."

with col_key:
    api_key = st.text_input(key_label, value=env_api_key, type="password",
                            help=f"{help_text} It is not stored anywhere.")

# ---- Inputs -----------------------------------------------------------------
tab_resume, tab_job = st.tabs(["Candidate Resume", "Job Description"])

with tab_resume:
    resume_input_method = st.radio("How would you like to provide the resume?", ("Upload File", "Manual Paste"), key="resume_method", horizontal=True)
    resume = ""
    if resume_input_method == "Upload File":
        if "resume_file_error" in st.session_state:
            st.error(st.session_state.resume_file_error)
            del st.session_state.resume_file_error
            
        if "resume_text" not in st.session_state:
            st.session_state.resume_text = ""
        if "resume_name" not in st.session_state:
            st.session_state.resume_name = ""
            
        if not st.session_state.resume_text:
            st.info("Supported formats: PDF, DOCX, TXT. Max file size: 5MB.")
            resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"], accept_multiple_files=False, key="resume_uploader")
            if resume_file is not None:
                if resume_file.size > 5 * 1024 * 1024:
                    st.session_state.resume_file_error = "File cannot be imported because it is above 5MB."
                    del st.session_state["resume_uploader"]
                    st.rerun()
                else:
                    st.session_state.resume_text = extract_text_from_file(resume_file)
                    st.session_state.resume_name = resume_file.name
                    st.rerun()
        else:
            st.success(f"Uploaded: {st.session_state.resume_name}")
            resume = st.session_state.resume_text
            if st.button("Remove Resume"):
                st.session_state.resume_text = ""
                st.session_state.resume_name = ""
                st.rerun()
    else:
        resume = st.text_area("Paste the resume / CV here", height=150, placeholder="Candidate's resume text...", label_visibility="collapsed")

with tab_job:
    job_input_method = st.radio("How would you like to provide the job description?", ("Manual Paste", "Upload File"), key="job_method", horizontal=True)
    job_desc = ""
    if job_input_method == "Upload File":
        if "job_file_error" in st.session_state:
            st.error(st.session_state.job_file_error)
            del st.session_state.job_file_error
            
        if "job_text" not in st.session_state:
            st.session_state.job_text = ""
        if "job_name" not in st.session_state:
            st.session_state.job_name = ""
            
        if not st.session_state.job_text:
            st.info("Supported formats: PDF, DOCX, TXT. Max file size: 5MB.")
            job_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"], accept_multiple_files=False, key="job_uploader")
            if job_file is not None:
                if job_file.size > 5 * 1024 * 1024:
                    st.session_state.job_file_error = "File cannot be imported because it is above 5MB."
                    del st.session_state["job_uploader"]
                    st.rerun()
                else:
                    st.session_state.job_text = extract_text_from_file(job_file)
                    st.session_state.job_name = job_file.name
                    st.rerun()
        else:
            st.success(f"Uploaded: {st.session_state.job_name}")
            job_desc = st.session_state.job_text
            if st.button("Remove Job Description"):
                st.session_state.job_text = ""
                st.session_state.job_name = ""
                st.rerun()
    else:
        job_desc = st.text_area("Paste the job description here", height=150, placeholder="The role's requirements...", label_visibility="collapsed")

st.markdown("---")

# ---- Execution --------------------------------------------------------------
if st.button("Screen the Candidate", type="primary", use_container_width=True):
    if not api_key or not resume.strip() or not job_desc.strip():
        missing = []
        if not api_key:
            missing.append("API key")
        if not resume.strip():
            missing.append("resume")
        if not job_desc.strip():
            missing.append("job description")
            
        if len(missing) == 1:
            msg = f"Please add your {missing[0]} first."
        elif len(missing) == 2:
            msg = f"Please add your {missing[0]} and {missing[1]} first."
        else:
            msg = "Please add your API key, resume, and job description first."
        st.warning(msg)
    else:
        # We clear the previous analysis result to avoid confusion
        if "analysis_result" in st.session_state:
            del st.session_state["analysis_result"]
            
        with st.status("Analyzing candidate fit...", expanded=True) as status:
            st.write("Extracting context from resume and job description...")
            time.sleep(0.5)
            st.write(f"Connecting to {provider.split(' ')[0]} API...")
            
            try:
                prompt_text = PROMPT.format(resume=resume, job_desc=job_desc)
                
                if provider == "Anthropic (Claude)":
                    client = anthropic.Anthropic(api_key=api_key)
                    message = client.messages.create(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=1500,
                        messages=[{"role": "user", "content": prompt_text}],
                    )
                    raw = message.content[0].text.strip()
                    
                elif provider == "OpenAI (GPT-4o)":
                    import openai
                    client = openai.OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt_text}],
                        response_format={"type": "json_object"}
                    )
                    raw = response.choices[0].message.content.strip()
                    
                else: # Google Gemini
                    from google import genai
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model='gemini-2.5-pro',
                        contents=prompt_text,
                    )
                    raw = response.text.strip()
                    
                st.write("Processing and formatting results...")

                # Safety net: strip code fences if the model adds them.
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                    raw = raw.strip()

                result = json.loads(raw)
                st.session_state["analysis_result"] = result
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
            except json.JSONDecodeError:
                status.update(label="Failed", state="error", expanded=True)
                st.error("The model did not return clean JSON. Try clicking the button again.")
            except Exception as e:
                status.update(label="Failed", state="error", expanded=True)
                st.error(f"Something went wrong: {e}")

# If we have a successful result in session_state, show the View Analysis button
if "analysis_result" in st.session_state:
    st.success("The agent has finished reviewing the candidate.")
    if st.button("View Analysis", use_container_width=True):
        show_analysis_modal(st.session_state["analysis_result"])
