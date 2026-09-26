import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(filename, title, content_paragraphs):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor='#1e293b',
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor='#334155',
        spaceAfter=8
    )
    
    story = [Paragraph(title, title_style), Spacer(1, 10)]
    for para in content_paragraphs:
        story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 4))
        
    doc.build(story)
    print(f"Generated PDF: {filename}")

if __name__ == "__main__":
    out_dir = "sample_resumes"
    
    # 1. Data Analyst PDF
    da_text = [
        "<b>Candidate Profile:</b> PII-Free Synthetic Data Analyst Resume",
        "<b>Summary:</b> Detail-oriented Data Analyst with expertise in data visualization, SQL queries, statistical analysis, and dashboard generation.",
        "<b>Technical Skills:</b> Python, SQL, Pandas, NumPy, Statistics, Power BI, Tableau, Excel, Data Cleaning, Data Visualization.",
        "<b>Experience:</b> Senior Data Analyst at Analytics Corp. Developed interactive dashboards in Power BI and automated ETL pipelines with Python and SQL.",
        "<b>Education:</b> B.S. in Computer Science & Applied Statistics.",
        "<b>Projects:</b> Customer Churn Analysis using Pandas and Scikit-Learn; Sales Performance Tracking Dashboard in Tableau."
    ]
    create_pdf(os.path.join(out_dir, "resume_data_analyst.pdf"), "Sample Data Analyst Resume", da_text)
    
    # 2. ML Engineer PDF
    ml_text = [
        "<b>Candidate Profile:</b> PII-Free Synthetic Machine Learning Engineer Resume",
        "<b>Summary:</b> Experienced Machine Learning Engineer specializing in deep learning, model deployment, and predictive modeling.",
        "<b>Technical Skills:</b> Python, PyTorch, Scikit-Learn, Deep Learning, MLflow, Docker, FastAPI, NumPy, Pandas, Git, Linux.",
        "<b>Experience:</b> AI Engineer at Tech Solutions. Built deep learning recommendation models in PyTorch and deployed microservices using Docker and FastAPI.",
        "<b>Education:</b> M.S. in Artificial Intelligence & Data Science.",
        "<b>Projects:</b> Real-time Object Detection with PyTorch; Automated MLOps Pipeline using MLflow and Docker."
    ]
    create_pdf(os.path.join(out_dir, "resume_ml_engineer.pdf"), "Sample Machine Learning Engineer Resume", ml_text)
    
    # 3. Software Engineer PDF
    se_text = [
        "<b>Candidate Profile:</b> PII-Free Synthetic Software Engineer Resume",
        "<b>Summary:</b> Full-stack software developer with robust experience in C++, C#, .NET, Python, SQL, Docker, and REST APIs.",
        "<b>Technical Skills:</b> C++, C#, .NET, Python, SQL, Docker, Git, REST APIs, Microservices, Linux, Unit Testing.",
        "<b>Experience:</b> Software Engineer at Enterprise Systems. Designed high-throughput microservices using C# and .NET Core.",
        "<b>Education:</b> B.Tech in Software Engineering.",
        "<b>Projects:</b> Distributed Cache Engine in C++; Enterprise API Gateway using .NET Core and Docker."
    ]
    create_pdf(os.path.join(out_dir, "resume_software_engineer.pdf"), "Sample Software Engineer Resume", se_text)
