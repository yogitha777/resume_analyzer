# 🧠 ResumeIQ — AI Resume Analyzer & Career Recommendation System

**ResumeIQ** is an intelligent, privacy-preserving resume analysis and career guidance platform. It evaluates technical skills, projects, and domain experience from uploaded resume documents (PDF & DOCX) to compute role compatibility scores, highlight missing skill gaps, and generate structured 4-week learning roadmaps.

---

## 🎯 Problem Statement & Objectives

### Problem Statement
Job seekers and students often struggle to assess how well their resumes align with target industry roles. Traditional automated screening tools (ATS) are opaque, while manual resume reviews can be costly and subjective. Furthermore, generic feedback rarely provides actionable steps to bridge technical skill gaps.

### Objectives
1. **Intelligent Text & Skill Extraction**: Accurately parse PDF and DOCX resume documents in-memory and extract domain-specific technical skills.
2. **Transparent Role Benchmarking**: Score compatibility against 8 key job roles using a transparent, multi-component matching model (70% Skill Overlap + 30% TF-IDF Cosine Similarity).
3. **Actionable Skill-Gap Analysis**: Identify exact matching vs. missing competencies for any selected target role.
4. **Structured Learning Roadmaps**: Generate customized 4-week action plans to guide skill acquisition and mini-project development.
5. **Responsible AI & Privacy**: Guarantee 100% demographic neutrality (no scoring on age, gender, ethnicity, etc.) and in-memory data safety.

---

## ✨ Key Features

- **📄 Dual Format Support**: Native parsing for PDF and DOCX resume files up to 5 MB.
- **🔒 In-Memory & Demographically Neutral**: Resumes are processed strictly in RAM and discarded after analysis. Personal demographic attributes are never evaluated.
- **📊 Blended Compatibility Engine**: Combines direct skill dictionary overlap with contextual TF-IDF vector similarity.
- **🏆 Top 3 Role Recommendations**: Automatically ranks and surfaces the top 3 best-fit roles.
- **🧠 Categorized Skill Extraction**: Groups detected skills into Programming Languages, Frameworks, Data Science, Cloud/DevOps, and Databases.
- **🗺️ 4-Week Actionable Roadmaps**: Provides step-by-step weekly goals, resource suggestions, and practical mini-projects to bridge missing skill gaps.
- **🤖 Optional Gemini AI Advisor**: Generates personalized, constructive feedback when a `GEMINI_API_KEY` is configured (safe-by-default offline fallback when unconfigured).
- **📥 Exportable Analysis Reports**: Download comprehensive summary reports in `.txt` format.

---

## 🏗️ System Architecture & Workflow

```
[ Upload PDF / DOCX ] ➔ [ In-Memory Parsing ] ➔ [ Text Normalization ]
                                                      │
[ Category Visuals ] ◄── [ Skill Dictionary ] ◄──────┤
                                                      │
[ Compatibility Charts] ◄─ [ TF-IDF + Cosine ] ◄──────┘
         │
         ├──> [ Top 3 Recommendations ]
         ├──> [ Skill-Gap Analysis (Found vs. Missing) ]
         ├──> [ 4-Week Learning Roadmap ]
         └──> [ Optional Gemini AI Advisor ] ➔ [ Downloadable Report ]
```

---

## 💻 Technologies Used

- **Language**: Python 3.10+
- **User Interface**: Streamlit
- **Data & Analytics**: Pandas, NumPy, Scikit-Learn (TF-IDF Vectorizer & Cosine Similarity)
- **Data Visualization**: Plotly Express & Plotly Graph Objects
- **Document Parsing**: PyPDF, Python-Docx
- **LLM Integration**: Google GenAI SDK (`google-genai`)
- **Testing & Quality**: Pytest, Standard Logging
- **Environment Management**: Python-Dotenv

---

## 📁 Project Structure

```
yogitha_resume_analyzer/
├── app.py                      # Main Streamlit web application
├── resume_parser.py            # PDF & DOCX in-memory text extractor
├── text_cleaner.py             # Text cleaner with C++/C#/.NET preservation
├── skill_extractor.py          # Dictionary-based technical skill extractor
├── job_matcher.py              # TF-IDF & Cosine Similarity match engine
├── roadmap_generator.py        # Skill gap analysis & 4-week roadmap generator
├── ai_feedback.py              # Optional Gemini AI feedback module
├── requirements.txt            # Project dependencies
├── .env.example                # API key configuration template
├── .gitignore                  # Git exclusion rules (.env, venv, caches)
├── data/
│   ├── job_roles.csv           # Benchmark job role definitions & required skills
│   └── skill_dictionary.csv    # Categorized skill dictionary
├── docs/
│   ├── PROJECT_REPORT.md       # Comprehensive technical project report
│   ├── architecture.mermaid    # System workflow & architecture diagram
│   └── testing_sheet.csv       # Test execution log & verification sheet
├── sample_resumes/             # Synthetic PII-free sample resumes (.docx, .pdf)
├── scripts/
│   └── create_sample_pdfs.py   # Synthetic sample PDF generator script
└── tests/
    ├── test_pipeline.py        # Pytest test suite (37 unit tests)
    └── test_cases.csv          # Pipeline benchmark test cases
```

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yogitha777/resume_analyzer.git
cd resume_analyzer
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure Gemini API Key
Create a `.env` file in the root directory based on `.env.example`:
```env
GEMINI_API_KEY=your_actual_api_key_here
```
> *Note: If no API key is set, ResumeIQ operates in offline mode with complete rule-based functionality.*

---

## 🚀 Running the Application

Launch the Streamlit web interface:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧮 Matching Methodology

ResumeIQ calculates compatibility using a two-tier weighted scoring model:

$$\text{Match Score} = (0.70 \times \text{Skill Overlap Score}) + (0.30 \times \text{TF-IDF Cosine Similarity})$$

1. **Skill Overlap Score (70%)**: Direct match percentage between skills extracted from the resume and the core required skills specified for the target role.
2. **TF-IDF Similarity Score (30%)**: Contextual vector similarity using term frequency-inverse document frequency over technical corpus descriptions.

---

## 🧪 Testing & Verification

Run the automated Pytest test suite to verify pipeline functionality:
```bash
python -m pytest tests/test_pipeline.py -v
```

All 37 test cases cover text cleaning, special token preservation (`C++`, `C#`, `.NET`), TF-IDF bounds $[0, 100]$, DOCX/PDF parsing, gap analysis, and 4-week roadmap section generation.

---

## 🔒 Responsible AI & Ethical Principles

- **Zero Demographic Bias**: ResumeIQ strictly ignores personal identifiers, demographics, photographs, gender, age, and marital status.
- **In-Memory Security**: Uploaded files are parsed dynamically in RAM and never stored on server storage.
- **Controlled Prompt Engineering**: When Gemini AI is enabled, only anonymized skill lists and role names are sent to the LLM — never raw resume text.

---

## 👤 Author & Maintainer

Developed by **Yogitha**  
GitHub Repository: [https://github.com/yogitha777/resume_analyzer](https://github.com/yogitha777/resume_analyzer)
