# Resume Screening Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced AI-powered agent designed to streamline the recruitment process. It compares a candidate's resume against a job description, scores the fit out of 100, extracts matched and missing skills, and provides concrete gap-closing advice. 

Built with Python and Streamlit, this tool is fully flexible and supports multiple top-tier LLMs including **Anthropic Claude**, **OpenAI GPT-4o**, and **Google Gemini**.

![screenshot placeholder — add a screenshot of the app here]

## Features

- **Multi-Model Support**: Seamlessly switch between Anthropic (Claude), OpenAI (GPT), and Google (Gemini) APIs.
- **Smart File Parsing**: Directly upload resumes and job descriptions as PDF, DOCX, or TXT files.
- **Structured JSON Output**: Guarantees highly structured, deterministic gap analysis results.
- **Exportable Reports**: Generate and download comprehensive Markdown reports of the screening analysis.
- **Dynamic Error Handling**: Gracefully handles missing inputs and massive file uploads.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3
- **LLM Integrations**: Anthropic SDK, OpenAI SDK, Google GenAI SDK
- **Document Parsers**: `pypdf`, `python-docx`

## Installation and Setup Guide

### 1. Clone the repository
```bash
git clone https://github.com/the-mom-who-codes/resume-screening-agent.git
cd resume-screening-agent
```

### 2. Create a virtual environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```
Open `.env` and insert your preferred API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```
*(Note: You only need to provide the key for the provider you intend to use. You can also paste the key directly in the web app UI).*

### 5. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
Navigate to the provided Local URL (typically `http://localhost:8501`) in your browser to start screening!

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
