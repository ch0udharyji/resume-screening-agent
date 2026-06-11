"""
Resume Screening Agent
----------------------
Paste a candidate's resume and a job description. The agent compares them,
scores the fit, lists matched and missing skills, and suggests how to close
the gaps. Built with Streamlit + the Anthropic API.

Run locally with:  streamlit run app.py
"""

import os
import json
import streamlit as st
import anthropic
from dotenv import load_dotenv

load_dotenv()

# The model the agent uses. You can swap this for any Claude model string.
MODEL = "claude-3-5-sonnet-latest"

# ---- Page setup -------------------------------------------------------------
st.set_page_config(page_title="Resume Screening Agent", page_icon="📄", layout="centered")
st.title("📄 Resume Screening Agent")
st.caption("Compares a resume against a job description — scores the fit and flags the gaps.")

# ---- API key ----------------------------------------------------------------
# Reads the key from an environment variable if set, otherwise asks for it.
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    api_key = st.text_input("Your Anthropic API key", type="password",
                            help="Get one at console.anthropic.com. It is not stored anywhere.")

# ---- Inputs -----------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    resume = st.text_area("Paste the resume / CV", height=320, placeholder="Candidate's resume text...")
with col2:
    job_desc = st.text_area("Paste the job description", height=320, placeholder="The role's requirements...")

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

# ---- Run --------------------------------------------------------------------
if st.button("Screen the candidate", type="primary"):
    if not api_key or not resume.strip() or not job_desc.strip():
        st.warning("Please add your API key, a resume, and a job description first.")
    else:
        try:
            with st.spinner("The agent is reading both documents..."):
                client = anthropic.Anthropic(api_key=api_key)
                message = client.messages.create(
                    model=MODEL,
                    max_tokens=1500,
                    messages=[{
                        "role": "user",
                        "content": PROMPT.format(resume=resume, job_desc=job_desc),
                    }],
                )
                raw = message.content[0].text.strip()

                # Safety net: strip code fences if the model adds them.
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                    raw = raw.strip()

                result = json.loads(raw)

            # ---- Display the result -----------------------------------------
            score = result.get("fit_score", 0)
            st.metric("Fit score", f"{score} / 100")
            st.progress(score / 100)
            st.subheader(result.get("verdict", ""))

            left, right = st.columns(2)
            with left:
                st.markdown("**✅ Matched skills**")
                for s in result.get("matched_skills", []):
                    st.markdown(f"- {s}")
            with right:
                st.markdown("**⚠️ Missing skills**")
                for s in result.get("missing_skills", []):
                    st.markdown(f"- {s}")

            st.markdown("**🔧 Gaps and how to close them**")
            for g in result.get("gaps", []):
                st.markdown(f"- {g}")

            st.markdown("**📝 Summary**")
            st.info(result.get("summary", ""))

        except json.JSONDecodeError:
            st.error("The model did not return clean JSON. Try clicking the button again.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
