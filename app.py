import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

from text_cleaner import clean_text
from resume_parser import parse_resume
from skill_extractor import SkillExtractor
from job_matcher import JobMatcher
from roadmap_generator import analyze_skill_gaps, generate_learning_roadmap
from ai_feedback import is_ai_feedback_available, generate_ai_feedback

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="ResumeIQ — AI Resume Analyzer & Career Recommendation System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS Styling for ResumeIQ ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Global Container Adjustments */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }
    
    /* Header Container */
    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .header-card h1 {
        color: #ffffff !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .header-card p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    
    /* Responsible AI Banner */
    .rai-banner {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 14px 18px;
        border-radius: 6px;
        font-size: 0.92rem;
        color: #334155;
        margin-bottom: 24px;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        text-align: center;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    
    /* Skill Badge Styling */
    .skill-badge {
        display: inline-block;
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 500;
        margin: 3px 4px;
    }
    .skill-badge-missing {
        display: inline-block;
        background-color: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 500;
        margin: 3px 4px;
    }
    
    /* Section Cards */
    .content-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    /* Status Badges */
    .status-online {
        color: #15803d;
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-offline {
        color: #b45309;
        background-color: #fffbeb;
        border: 1px solid #fef3c7;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <h1>🧠 ResumeIQ</h1>
    <p>AI Resume Analyzer & Career Recommendation System</p>
</div>
""", unsafe_allow_html=True)

# ── Responsible AI Statement ───────────────────────────────────────────────────
st.markdown("""
<div class="rai-banner">
    🔒 <strong>Responsible AI Guarantee:</strong> ResumeIQ evaluates strictly job-relevant technical skills, 
    projects, education, and domain competencies. Demographic factors (gender, age, ethnicity, nationality, 
    religion, marital status, or disability) are <strong>never</strong> evaluated, requested, or stored. 
    Resumes are processed entirely <strong>in-memory</strong> and discarded after analysis.
</div>
""", unsafe_allow_html=True)

# ── Sidebar Setup ──────────────────────────────────────────────────────────────
st.sidebar.markdown("### 📁 Upload Resume")
uploaded_file = st.sidebar.file_uploader(
    "Select your PDF or DOCX resume:",
    type=["pdf", "docx"],
    help="Upload your latest resume file (Max 5MB)."
)


# ── Cached Resource Loaders ────────────────────────────────────────────────────
@st.cache_resource
def load_components():
    extractor = SkillExtractor("data/skill_dictionary.csv")
    matcher = JobMatcher("data/job_roles.csv")
    return extractor, matcher


skill_extractor, job_matcher = load_components()

# ── Main Application Workflow ──────────────────────────────────────────────────
if uploaded_file is not None:
    # ── File Validation ────────────────────────────────────────────────────────
    MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
    allowed_extensions = {".pdf", ".docx"}
    file_ext = "." + uploaded_file.name.rsplit(".", 1)[-1].lower() if "." in uploaded_file.name else ""

    if file_ext not in allowed_extensions:
        st.error(f"❌ **Unsupported File Format:** `{file_ext or 'Unknown'}`. Please upload a valid `.pdf` or `.docx` document.")
        st.stop()

    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        st.error(f"❌ **File Exceeds Limit:** `{uploaded_file.size / (1024*1024):.2f} MB`. Maximum allowed size is 5 MB.")
        st.stop()

    st.sidebar.success(f"✅ Loaded: `{uploaded_file.name}`")
    with st.sidebar.expander("ℹ️ File Properties", expanded=False):
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Format:** {file_ext.upper()[1:]}")
        st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")

    # ── Extraction & Matching Core Pipeline ────────────────────────────────────
    raw_text = parse_resume(uploaded_file)
    cleaned_resume = clean_text(raw_text)

    skill_data = skill_extractor.extract_skills(cleaned_resume)
    extracted_skills = skill_data["all_skills"]
    categorized = skill_data["categorized_skills"]

    rankings = job_matcher.compute_match_scores(cleaned_resume, extracted_skills)
    job_roles_list = [r["job_role"] for r in rankings]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Target Job Role")
    selected_role_name = st.sidebar.selectbox("Choose role for gap analysis:", job_roles_list)

    target_info = next(r for r in rankings if r["job_role"] == selected_role_name)
    gap_analysis = analyze_skill_gaps(extracted_skills, target_info["required_skills"])
    roadmap = generate_learning_roadmap(gap_analysis["missing_skills"])

    # ── Main Content Area with 4 Custom Tabs ──────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Resume Overview",
        "🧠 Skills Analysis",
        "🗺️ Career Roadmap",
        "🤖 AI Career Advisor"
    ])

    # ═══════════════════════════════════════════════════════════════════════════
    # TAB 1: 📊 Resume Overview
    # ═══════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown("### 🎯 Target Role Compatibility")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Target Role</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(selected_role_name), unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Overall Match Score</div>
                <div class="metric-value" style="color: #2563eb;">{:.1f}%</div>
            </div>
            """.format(target_info['match_score']), unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Extracted Skills Count</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(len(extracted_skills)), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_gauge, col_top3 = st.columns([1, 1])

        with col_gauge:
            st.markdown("#### ⏱️ Match Score Gauge")
            gauge_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=target_info["match_score"],
                number={"suffix": "%", "font": {"size": 34, "color": "#1e293b"}},
                title={"text": f"Compatibility — {selected_role_name}", "font": {"size": 14, "color": "#64748b"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": "#2563eb"},
                    "steps": [
                        {"range": [0, 40], "color": "#fee2e2"},
                        {"range": [40, 70], "color": "#fef3c7"},
                        {"range": [70, 100], "color": "#dcfce7"},
                    ],
                    "threshold": {
                        "line": {"color": "#dc2626", "width": 4},
                        "thickness": 0.75,
                        "value": target_info["match_score"],
                    },
                },
            ))
            gauge_fig.update_layout(height=260, margin=dict(t=40, b=10, l=20, r=20))
            st.plotly_chart(gauge_fig, use_container_width=True)

            st.info(
                f"💡 **Scoring Formula:** Blended blend of **Skill Overlap (70%)** = `{target_info['skill_overlap_score']:.1f}%` "
                f"and **TF-IDF Contextual Similarity (30%)** = `{target_info['tfidf_score']:.1f}%`."
            )

        with col_top3:
            st.markdown("#### 🏆 Top Recommended Roles")
            top3 = rankings[:3]
            badges = ["🥇 1st Rank", "🥈 2nd Rank", "🥉 3rd Rank"]
            for badge, role in zip(badges, top3):
                st.markdown(f"""
                <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 12px 18px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #0f172a; font-size: 1.05rem;">{badge}: {role['job_role']}</strong>
                        <div style="color: #64748b; font-size: 0.85rem;">Overlap: {role['skill_overlap_score']:.1f}% | TF-IDF: {role['tfidf_score']:.1f}%</div>
                    </div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #2563eb;">{role['match_score']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📊 All Job Role Compatibility Benchmarks")
        df_rankings = pd.DataFrame(rankings)
        fig_bar = px.bar(
            df_rankings,
            x="match_score",
            y="job_role",
            orientation="h",
            title="Role Match Percentage Comparison (%)",
            labels={"match_score": "Score (%)", "job_role": "Job Role"},
            color="match_score",
            color_continuous_scale="Blues",
            text="match_score",
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, height=360, margin=dict(l=20, r=40, t=40, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # TAB 2: 🧠 Skills Analysis
    # ═══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("### 🧠 Technical Skill Extraction & Gap Analysis")

        col_skills_cat, col_skills_chart = st.columns([1.1, 0.9])

        with col_skills_cat:
            st.markdown("#### 📌 Extracted Skills by Domain")
            if categorized:
                for cat, s_list in categorized.items():
                    cat_name = cat.replace('_', ' ').title()
                    badges_html = " ".join([f'<span class="skill-badge">{s}</span>' for s in s_list])
                    st.markdown(f"**{cat_name}** ({len(s_list)}):<br>{badges_html}", unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            else:
                st.warning("No technical skills detected from dictionary matching.")

        with col_skills_chart:
            st.markdown("#### 📈 Skill Distribution across Domains")
            if categorized:
                cat_counts = {cat.replace('_', ' ').title(): len(s_list) for cat, s_list in categorized.items() if s_list}
                df_cat = pd.DataFrame(list(cat_counts.items()), columns=["Category", "Skill Count"])
                
                fig_donut = px.pie(
                    df_cat,
                    names="Category",
                    values="Skill Count",
                    hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    title="Skill Breakdown by Category"
                )
                fig_donut.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown("---")
        st.markdown(f"#### 🔍 Target Skill Comparison: **{selected_role_name}**")
        
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("##### ✅ Matching Competencies Found")
            if gap_analysis["matching_skills"]:
                found_badges = " ".join([f'<span class="skill-badge">{s.title()}</span>' for s in sorted(gap_analysis["matching_skills"])])
                st.markdown(found_badges, unsafe_allow_html=True)
            else:
                st.write("_No required skills detected for this target role._")

        with g2:
            st.markdown("##### ❌ Missing / Priority Growth Areas")
            if gap_analysis["missing_skills"]:
                missing_badges = " ".join([f'<span class="skill-badge-missing">{s.title()}</span>' for s in sorted(gap_analysis["missing_skills"])])
                st.markdown(missing_badges, unsafe_allow_html=True)
            else:
                st.success("🎉 Outstanding! You possess all primary baseline skills for this role.")

    # ═══════════════════════════════════════════════════════════════════════════
    # TAB 3: 🗺️ Career Roadmap
    # ═══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown(f"### 🗺️ Structured 4-Week Action Plan: **{selected_role_name}**")
        st.caption("Customized learning trajectory designed to bridge missing skill gaps efficiently.")

        for line in roadmap:
            if line.startswith("### 📅"):
                st.markdown(f"#### {line.replace('### ', '')}")
            elif line.startswith("- **"):
                st.markdown(f"• {line[2:]}")
            elif line.strip():
                st.markdown(line)

    # ═══════════════════════════════════════════════════════════════════════════
    # TAB 4: 🤖 AI Career Advisor
    # ═══════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown("### 🤖 Personalized AI Career Feedback & Export")

        ai_available = is_ai_feedback_available()
        if ai_available:
            st.markdown('Status: <span class="status-online">🟢 Gemini API Configured (Online)</span>', unsafe_allow_html=True)
        else:
            st.markdown('Status: <span class="status-offline">🟡 Offline Mode (Rule-based output active — GEMINI_API_KEY unconfigured)</span>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        ai_feedback_text = None
        if ai_available:
            st.markdown("#### 💡 Request Gemini AI Custom Analysis")
            st.write("Generates an encouraging, privacy-preserving feedback summary tailored exclusively to your skill profile.")
            if st.button("✨ Generate AI Career Guidance", type="primary"):
                with st.spinner("Connecting securely to Gemini LLM..."):
                    ai_feedback_text = generate_ai_feedback(
                        target_role=selected_role_name,
                        matching_skills=gap_analysis["matching_skills"],
                        missing_skills=gap_analysis["missing_skills"],
                        match_score=target_info["match_score"],
                    )
                if ai_feedback_text:
                    st.info(ai_feedback_text)
        else:
            st.info(
                "ℹ️ **Optional Feature Note:** Gemini AI feedback is currently offline because no `GEMINI_API_KEY` was detected in the environment. "
                "All core rule-based matching, gap analysis, and 4-week roadmaps remain 100% functional."
            )

        st.markdown("---")
        st.markdown("#### 📥 Export Full Resume Analysis Report")
        
        top3_lines = "\n".join(
            f"  {i+1}. {r['job_role']} — Match Score: {r['match_score']:.1f}%"
            for i, r in enumerate(top3)
        )

        report_content = f"""RESUMEIQ — COMPREHENSIVE CAREER ANALYSIS REPORT
======================================================================
Generated System : ResumeIQ AI Resume Analyzer
Responsible AI   : Evaluates technical skills, experience, and domain knowledge.
                   Demographics are never evaluated or stored.
======================================================================

TARGET ROLE         : {selected_role_name}
OVERALL MATCH SCORE : {target_info['match_score']:.1f}%
  • Skill Overlap Score     : {target_info['skill_overlap_score']:.1f}%
  • TF-IDF Context Score   : {target_info['tfidf_score']:.1f}%

----------------------------------------------------------------------
TOP 3 RECOMMENDED ROLES
----------------------------------------------------------------------
{top3_lines}

----------------------------------------------------------------------
EXTRACTED TECHNICAL SKILLS ({len(extracted_skills)} total)
----------------------------------------------------------------------
{', '.join(sorted(extracted_skills)) if extracted_skills else 'None detected'}

----------------------------------------------------------------------
SKILL-GAP ANALYSIS FOR {selected_role_name.upper()}
----------------------------------------------------------------------
Matching Skills Found : {', '.join(sorted(gap_analysis['matching_skills'])) if gap_analysis['matching_skills'] else 'None'}
Missing Growth Skills  : {', '.join(sorted(gap_analysis['missing_skills'])) if gap_analysis['missing_skills'] else 'None'}

----------------------------------------------------------------------
4-WEEK LEARNING ROADMAP
----------------------------------------------------------------------
""" + "\n".join(
            line.replace("**", "").replace("*", "").replace("###", ">>")
            for line in roadmap
        )

        if ai_feedback_text:
            report_content += f"\n\n----------------------------------------------------------------------\nGEMINI AI CAREER ADVISOR FEEDBACK\n----------------------------------------------------------------------\n{ai_feedback_text}"

        st.download_button(
            label="📄 Download Analysis Summary Report (.txt)",
            data=report_content,
            file_name=f"ResumeIQ_Analysis_{selected_role_name.replace(' ', '_').lower()}.txt",
            mime="text/plain",
        )

else:
    # ── Landing / Welcome View ──────────────────────────────────────────────────
    st.markdown("""
    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); text-align: center;">
        <h2 style="color: #0f172a; margin-bottom: 12px;">👋 Welcome to ResumeIQ!</h2>
        <p style="color: #475569; font-size: 1.05rem; max-width: 650px; margin: 0 auto 24px auto;">
            Upload your resume PDF or DOCX file using the sidebar on the left to unlock intelligent role compatibility matching, technical skill extraction, and personalized 4-week learning roadmaps.
        </p>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px 20px; text-align: left; width: 280px;">
                <strong style="color: #2563eb;">📄 In-Memory Parsing</strong><br>
                <span style="font-size: 0.88rem; color: #64748b;">Supports PDF and DOCX formats without disk storage.</span>
            </div>
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px 20px; text-align: left; width: 280px;">
                <strong style="color: #2563eb;">📊 Blended Match Engine</strong><br>
                <span style="font-size: 0.88rem; color: #64748b;">Combines 70% skill overlap with 30% TF-IDF similarity.</span>
            </div>
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px 20px; text-align: left; width: 280px;">
                <strong style="color: #2563eb;">🗺️ 4-Week Roadmaps</strong><br>
                <span style="font-size: 0.88rem; color: #64748b;">Actionable weekly plans tailored to bridge identified skill gaps.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)