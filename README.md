<div align="center">

# Resume Screening Agent

**An AI-powered agent that scores resumes against job descriptions, highlights skill gaps, and generates actionable reports.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Anthropic](https://img.shields.io/badge/Claude-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![OpenAI](https://img.shields.io/badge/GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Gemini](https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)

[![GitHub stars](https://img.shields.io/github/stars/the-mom-who-codes/resume-screening-agent?style=for-the-badge&logo=github&color=blue)](https://github.com/the-mom-who-codes/resume-screening-agent/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/the-mom-who-codes/resume-screening-agent?style=for-the-badge&logo=github&color=blue)](https://github.com/the-mom-who-codes/resume-screening-agent/network/members)
[![GitHub issues](https://img.shields.io/github/issues/the-mom-who-codes/resume-screening-agent?style=for-the-badge&logo=github&color=blue)](https://github.com/the-mom-who-codes/resume-screening-agent/issues)

</div>

---

## Overview

Resume Screening Agent streamlines recruitment by comparing a candidate's resume against a job description. It scores the overall fit out of 100, extracts matched and missing skills, and provides concrete, actionable advice on how to close the gap.

Built with **Python** and **Streamlit**, the tool is provider-agnostic and supports multiple top-tier LLMs, including **Anthropic Claude**, **OpenAI GPT-4o**, and **Google Gemini** — switch between them at any time.

<br>

<div align="center">

<img width="800" alt="Home page screenshot" src="" />

*Add a screenshot of the home/upload page here*

</div>

---

## Features

| | |
|---|---|
| **Multi-Model Support** | Seamlessly switch between Anthropic (Claude), OpenAI (GPT), and Google (Gemini) APIs. |
| **Smart File Parsing** | Directly upload resumes and job descriptions as PDF, DOCX, or TXT files. |
| **Structured JSON Output** | Guarantees highly structured, deterministic gap-analysis results. |
| **Exportable Reports** | Generate and download comprehensive Markdown reports of the screening analysis. |
| **Dynamic Error Handling** | Gracefully handles missing inputs and oversized file uploads. |

---

## Technology Stack

<table>
  <tr>
    <td><b>Frontend</b></td>
    <td>Streamlit</td>
  </tr>
  <tr>
    <td><b>Backend</b></td>
    <td>Python 3</td>
  </tr>
  <tr>
    <td><b>LLM Integrations</b></td>
    <td>Anthropic SDK · OpenAI SDK · Google GenAI SDK</td>
  </tr>
  <tr>
    <td><b>Document Parsers</b></td>
    <td><code>pypdf</code> · <code>python-docx</code></td>
  </tr>
</table>

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/the-mom-who-codes/resume-screening-agent.git
cd resume-screening-agent
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Open `.env` and insert your preferred API key(s):

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

> **Note:** You only need to provide the key for the provider you intend to use. Alternatively, you can paste the key directly into the web app UI.

### 5. Run the application

```bash
streamlit run app.py
```

Navigate to the local URL printed in your terminal (typically `http://localhost:8501`) to start screening.

---

## License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details.