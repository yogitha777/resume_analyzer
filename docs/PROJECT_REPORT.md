# 📘 Comprehensive Project Report: ResumeIQ

**Project Name:** ResumeIQ — AI Resume Analyzer & Career Recommendation System  
**Author:** Yogitha  
**Repository:** [https://github.com/yogitha777/resume_analyzer](https://github.com/yogitha777/resume_analyzer)  

---

## 1. Executive Summary & Problem Statement

### 1.1 Context
In today's modern job market, candidates face significant challenges in understanding how well their technical profiles match specific career paths. Traditional Applicant Tracking Systems (ATS) reject candidates without explaining skill deficiencies, while manual career counseling is expensive and unavailable to many students.

### 1.2 Proposed Solution
**ResumeIQ** is an interactive, privacy-aware AI platform designed to analyze resume documents (PDF and DOCX), extract domain-specific technical skills, score role compatibility against 8 industry benchmarks, perform gap analysis, and construct actionable 4-week learning roadmaps.

---

## 2. System Architecture & Workflow

### 2.1 Technical Architecture
ResumeIQ adopts a modular, 5-layer software architecture:
1. **Presentation Layer**: Streamlit Web UI (`app.py`) featuring responsive CSS, interactive metrics, and 4 dedicated navigation tabs.
2. **Ingestion & Parsing Layer**: In-memory text extraction (`resume_parser.py`) supporting PDF (`pypdf`) and DOCX (`python-docx`).
3. **Normalization & Extraction Layer**: Text standardization (`text_cleaner.py`) with C++/C#/.NET preservation and dictionary keyword matching (`skill_extractor.py`).
4. **Matching & Analytics Engine**: Blended scoring engine (`job_matcher.py`) combining 70% direct skill overlap with 30% TF-IDF vector similarity (`scikit-learn`).
5. **Guidance & Advisory Layer**: 4-week roadmap generation (`roadmap_generator.py`) and optional LLM career feedback (`ai_feedback.py` using `google-genai`).

---

## 3. Key Modules & Technical Implementation

### 3.1 Text Cleaner & Token Protection
Standard text cleaners strip symbols like `+`, `#`, and `.`, destroying critical technical keywords (`C++`, `C#`, `.NET`). `text_cleaner.py` uses temporary placeholder substitution during regex cleaning to ensure 100% token preservation.

### 3.2 Matching Algorithm
Compatibility scores are generated via a blended mathematical formula:

$$\text{Match Score} = \min\left(100.0, \max\left(0.0, 0.70 \times \text{Overlap} + 0.30 \times \text{TF-IDF}\right)\right)$$

- **Skill Overlap Percentage**: Ratio of matched resume skills to target role requirements.
- **TF-IDF Cosine Similarity**: Unigram/bigram vector comparison against role descriptions in `job_roles.csv`.

### 3.3 Skill-Gap Analysis & Roadmap Generation
Missing skills are derived by set subtraction: $\text{Missing} = \text{Required} \setminus \text{Extracted}$. `roadmap_generator.py` divides missing skills evenly across a 4-week timeline, assigning weekly goals, practice topics, and mini-project milestones.

### 3.4 Optional Gemini AI Advisor
`ai_feedback.py` implements safe-by-default integration with Google's Gemini LLM. It features dynamic model discovery (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) and controlled prompt engineering that passes only anonymized skill sets to prevent PII leaks.

---

## 4. Responsible AI & Data Security

1. **Demographic Neutrality**: ResumeIQ never evaluates, requests, or stores personal attributes (age, gender, ethnicity, religion, marital status, disability).
2. **In-Memory File Processing**: Resumes are parsed dynamically in RAM and discarded immediately after processing.
3. **API Key Security**: The app operates 100% offline when no `GEMINI_API_KEY` is present. Keys are loaded strictly from `.env` and excluded from Git commits.

---

## 5. Verification & Testing Results

- **Automated Unit Tests**: 37/37 Pytest assertions passed cleanly (`tests/test_pipeline.py`).
- **File Validation Testing**: Successfully validated file uploads up to 5 MB with proper error handling for invalid formats.
- **End-to-End Pipeline Verification**: Verified PDF/DOCX parsing, skill matching, score ranking, gap analysis, roadmap generation, and report downloading.

---

## 6. Limitations & Future Roadmap

### 6.1 Current Limitations
- Skills dictionary relies on predefined CSV mappings.
- TF-IDF requires sufficient text density for optimal vector scoring.

### 6.2 Future Scope
- Integration with live job market APIs (LinkedIn, Indeed).
- Support for multilingual resume analysis.
- Interactive skill self-assessment quizzes.
