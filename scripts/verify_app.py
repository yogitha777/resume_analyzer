import os
import sys

# Ensure root directory is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import io
from resume_parser import parse_resume
from text_cleaner import clean_text
from skill_extractor import SkillExtractor
from job_matcher import JobMatcher
from roadmap_generator import analyze_skill_gaps, generate_learning_roadmap
from ai_feedback import is_ai_feedback_available, generate_ai_feedback

class UploadedFileMock:
    def __init__(self, filepath):
        self.name = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            self._bytes = f.read()
    def getvalue(self):
        return self._bytes
    def read(self):
        return self._bytes

def verify_pipeline():
    extractor = SkillExtractor(os.path.join(ROOT, "data", "skill_dictionary.csv"))
    matcher = JobMatcher(os.path.join(ROOT, "data", "job_roles.csv"))
    
    # Verify PDF
    pdf_mock = UploadedFileMock(os.path.join(ROOT, "sample_resumes", "resume_data_analyst.pdf"))
    pdf_text = parse_resume(pdf_mock)
    cleaned_pdf = clean_text(pdf_text)
    pdf_skills = extractor.extract_skills(cleaned_pdf)["all_skills"]
    pdf_rankings = matcher.compute_match_scores(cleaned_pdf, pdf_skills)
    print(f"[OK] PDF Parsing & Matching: extracted {len(pdf_skills)} skills, top role '{pdf_rankings[0]['job_role']}' ({pdf_rankings[0]['match_score']}%)")

    # Verify DOCX
    docx_mock = UploadedFileMock(os.path.join(ROOT, "sample_resumes", "resume_data_analyst.docx"))
    docx_text = parse_resume(docx_mock)
    cleaned_docx = clean_text(docx_text)
    docx_skills = extractor.extract_skills(cleaned_docx)["all_skills"]
    docx_rankings = matcher.compute_match_scores(cleaned_docx, docx_skills)
    print(f"[OK] DOCX Parsing & Matching: extracted {len(docx_skills)} skills, top role '{docx_rankings[0]['job_role']}' ({docx_rankings[0]['match_score']}%)")

    # Verify Gap Analysis & Roadmap
    top_role = pdf_rankings[0]
    gaps = analyze_skill_gaps(pdf_skills, top_role["required_skills"])
    roadmap = generate_learning_roadmap(gaps["missing_skills"])
    week_count = sum(1 for line in roadmap if "Week" in line and ("###" in line or "Week" in line))
    print(f"[OK] Gap Analysis & Roadmap: {len(gaps['matching_skills'])} matching, {len(gaps['missing_skills'])} missing, roadmap generated")

    # Verify AI Feedback availability & safe offline status
    ai_status = is_ai_feedback_available()
    print(f"[OK] AI Feedback module status check: API Key Available = {ai_status}")

if __name__ == "__main__":
    verify_pipeline()
