"""ResumeGuard AI - Main Streamlit Application"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Import modules
from modules.resume_processor import ResumeProcessor
from modules.quality_analyzer import QualityAnalyzer
from modules.ats_analyzer import ATSAnalyzer
from modules.truth_checker import TruthChecker
from modules.job_analyzer import JobAnalyzer
from modules.matching_engine import MatchingEngine
from modules.project_analyzer import ProjectAnalyzer
from modules.ml_model import MatchingClassifier

from utils.demo_data import (
    list_sample_resumes, list_sample_jobs,
    get_sample_resume, get_sample_job_description
)
from utils.constants import (
    COLOR_EXCELLENT, COLOR_GOOD, COLOR_FAIR, COLOR_POOR,
    COLOR_MATCHED, COLOR_MISSING, COLOR_PARTIAL,
    COLOR_HIGH_PRIORITY, COLOR_MEDIUM_PRIORITY, COLOR_LOW_PRIORITY
)

# Page config
st.set_page_config(
    page_title="ResumeGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .score-excellent { color: #00cc44; font-weight: bold; }
    .score-good { color: #4499ff; font-weight: bold; }
    .score-fair { color: #ffaa00; font-weight: bold; }
    .score-poor { color: #ff3333; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'job_description' not in st.session_state:
        st.session_state.job_description = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False

def create_score_chart(score, label, color_range='full'):
    """Create a gauge chart for scores."""
    if score >= 80:
        color = COLOR_EXCELLENT
    elif score >= 60:
        color = COLOR_GOOD
    elif score >= 40:
        color = COLOR_FAIR
    else:
        color = COLOR_POOR
    
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': label},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 20], 'color': COLOR_POOR},
                {'range': [20, 40], 'color': '#ff8800'},
                {'range': [40, 60], 'color': COLOR_FAIR},
                {'range': [60, 80], 'color': COLOR_GOOD},
                {'range': [80, 100], 'color': COLOR_EXCELLENT}
            ],
            'threshold': {
                'line': {'color': 'white', 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    )])
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def upload_resume_section():
    """Handle resume upload."""
    st.header("📄 Resume Upload & Processing")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt']
        )
    
    with col2:
        demo_toggle = st.checkbox("📚 Demo Mode", value=st.session_state.demo_mode)
        st.session_state.demo_mode = demo_toggle
    
    if st.session_state.demo_mode:
        st.info("🎯 Demo Mode Enabled - Select sample data below")
        sample_resume = st.selectbox(
            "Select Sample Resume",
            list_sample_resumes(),
            key="demo_resume_select"
        )
        st.session_state.resume_text = get_sample_resume(sample_resume)
        st.success(f"✅ Loaded: {sample_resume}")
    
    elif uploaded_file:
        processor = ResumeProcessor()
        result = processor.process_file(uploaded_file)
        
        if result['success']:
            st.session_state.resume_text = result['text']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 File", result['file_name'])
            with col2:
                st.metric("📊 Words", processor.get_word_count())
            with col3:
                st.metric("📧 Contact", result['email'])
            
            st.success("✅ Resume processed successfully!")
        else:
            st.error(f"❌ Error: {result['error']}")
    
    # Display resume text if available
    if st.session_state.resume_text:
        with st.expander("👁️ View Extracted Resume Text"):
            st.text_area("Resume Content:", st.session_state.resume_text, height=300, disabled=True)
        return True
    
    return False

def quality_analysis_section():
    """Resume quality analysis."""
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume first")
        return
    
    st.header("⭐ Resume Quality Analysis")
    
    analyzer = QualityAnalyzer(st.session_state.resume_text)
    analysis = analyzer.analyze()
    
    # Main scores
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.plotly_chart(
            create_score_chart(analysis['overall_score'], 'Overall'),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            create_score_chart(analysis['completeness_score'], 'Completeness'),
            use_container_width=True
        )
    with col3:
        st.plotly_chart(
            create_score_chart(analysis['content_score'], 'Content'),
            use_container_width=True
        )
    with col4:
        st.plotly_chart(
            create_score_chart(analysis['keyword_score'], 'Keywords'),
            use_container_width=True
        )
    with col5:
        st.plotly_chart(
            create_score_chart(analysis['grammar_score'], 'Grammar'),
            use_container_width=True
        )
    
    # Sections analysis
    st.subheader("📋 Section Analysis")
    sections_df = pd.DataFrame([
        {
            'Section': sec,
            'Status': info['quality'],
            'Word Count': info['length']
        }
        for sec, info in analysis['sections_analysis'].items()
    ])
    st.dataframe(sections_df, use_container_width=True)
    
    # Issues
    if analysis['issues']:
        st.subheader("⚠️ Issues Found")
        for issue in analysis['issues'][:5]:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    severity_color = '#ff3333' if issue['severity'] == 'High' else '#ffaa00'
                    st.markdown(f"**{issue['type']}** ({issue['severity']})")
                with col2:
                    st.write(issue['suggestion'])
    
    # Recommendations
    st.subheader("💡 Recommendations")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.write(f"{i}. {rec}")
    
    return analysis

def ats_analysis_section():
    """ATS compatibility analysis."""
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume first")
        return
    
    st.header("🤖 ATS Compatibility Analyzer")
    st.info("⚠️ **Note**: This ATS score is an estimate for guidance only")
    
    analyzer = ATSAnalyzer(st.session_state.resume_text)
    analysis = analyzer.analyze()
    
    # Main score
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(
            create_score_chart(analysis['ats_score'], 'ATS Score'),
            use_container_width=True
        )
    
    with col2:
        st.markdown("### 📊 Component Scores")
        st.metric("Section Names", analysis['section_names_score'])
        st.metric("Keyword Density", analysis['keyword_density_score'])
        st.metric("Structure", analysis['structure_score'])
        st.metric("Formatting", analysis['formatting_score'])
    
    # Explanation
    st.markdown("### 📝 Analysis")
    st.write(analyzer.get_ats_score_explanation())
    
    # Issues
    if analysis['issues']:
        st.subheader("⚠️ ATS Issues")
        for issue in analysis['issues']:
            with st.container():
                st.markdown(f"**{issue['issue']}**")
                st.write(f"*Impact: {issue['impact']}*")
                st.write(f"💡 {issue['solution']}")
    
    # Recommendations
    st.subheader("✨ Optimization Tips")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.write(f"{i}. {rec}")
    
    return analysis

def truth_checker_section():
    """Truth and consistency checker."""
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume first")
        return
    
    st.header("✅ AI Truth & Consistency Checker")
    
    checker = TruthChecker(st.session_state.resume_text)
    analysis = checker.analyze()
    
    # Main score
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(
            create_score_chart(analysis['truth_score'], 'Evidence Strength'),
            use_container_width=True
        )
    
    with col2:
        evidence = analysis['evidence_strength']
        st.markdown("### 📊 Evidence Breakdown")
        st.metric("Projects", f"{evidence['project_evidence']}/25")
        st.metric("Results", f"{evidence['result_evidence']}/25")
        st.metric("Certs", f"{evidence['certification_evidence']}/20")
        st.metric("Metrics", f"{evidence['measurable_evidence']}/30")
    
    # Vague claims
    if analysis['vague_claims']:
        st.subheader("🤔 Vague Claims Needing Evidence")
        for claim_issue in analysis['vague_claims'][:5]:
            with st.container():
                st.markdown(f"**Claim**: {claim_issue['claim']}")
                st.write(f"*From*: {claim_issue['sentence']}")
                st.write(f"**Suggestion**: {claim_issue['suggestion']}")
                st.divider()
    
    # Consistency issues
    if analysis['consistency_issues']:
        st.subheader("⏱️ Timeline Consistency Issues")
        for consistency_issue in analysis['consistency_issues']:
            st.warning(f"**{consistency_issue['type']}**: {consistency_issue['description']}")
            st.write(f"💡 {consistency_issue['suggestion']}")
    
    # Recommendations
    st.subheader("💡 How to Strengthen Your Evidence")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.write(f"{i}. {rec}")
    
    return analysis

def job_analysis_section():
    """Analyze job description."""
    st.header("📋 Job Description Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_input = st.text_area(
            "Paste or upload a job description",
            height=300,
            placeholder="Paste the job description here..."
        )
    
    with col2:
        if st.session_state.demo_mode:
            sample_job = st.selectbox(
                "Or select a sample job",
                list_sample_jobs(),
                key="demo_job_select"
            )
            job_input = get_sample_job_description(sample_job)
            st.success(f"✅ Loaded: {sample_job}")
    
    if job_input:
        st.session_state.job_description = job_input
        
        analyzer = JobAnalyzer(job_input)
        analysis = analyzer.analyze()
        
        # Job info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📌 Category", analysis['job_category'])
        with col2:
            st.metric("📍 Level", analysis['experience_level']['level'])
        with col3:
            years = analysis['experience_level']['years_required']
            st.metric("📅 Years", f"{years}+" if years else "Not Specified")
        with col4:
            st.metric("🎯 Skills", len(analysis['extracted_skills']))
        
        # Required vs Nice to have
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Required Skills")
            for skill in analysis['required_skills'][:10]:
                st.write(f"• {skill}")
        
        with col2:
            st.subheader("⭐ Nice to Have")
            for skill in analysis['nice_to_have_skills'][:10]:
                st.write(f"• {skill}")
        
        # Technologies
        st.subheader("🔧 Technologies Mentioned")
        techs = analysis['technologies']
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.write("**Languages**")
            for lang in techs['languages'][:3]:
                st.write(f"• {lang}")
        
        with col2:
            st.write("**Web Frameworks**")
            for fw in techs['web_frameworks'][:3]:
                st.write(f"• {fw}")
        
        with col3:
            st.write("**Databases**")
            for db in techs['databases'][:3]:
                st.write(f"• {db}")
        
        with col4:
            st.write("**Cloud**")
            for cloud in techs['cloud_services'][:3]:
                st.write(f"• {cloud}")
        
        with col5:
            st.write("**DevOps**")
            for devops in techs['devops'][:3]:
                st.write(f"• {devops}")
        
        return analysis
    
    return None

def matching_section(quality_analysis, ats_analysis, truth_analysis):
    """Resume vs Job Matching."""
    if not st.session_state.resume_text or not st.session_state.job_description:
        st.warning("⚠️ Please upload a resume and job description first")
        return
    
    st.header("🎯 Resume vs Job Matching")
    
    matcher = MatchingEngine(st.session_state.resume_text, st.session_state.job_description)
    matching = matcher.analyze()
    
    # Main match score
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(
            create_score_chart(matching['match_score'], 'Job Match Score'),
            use_container_width=True
        )
    
    with col2:
        summary = matching['match_summary']
        st.markdown(f"### {summary['summary']}")
        st.write(summary['description'])
        st.metric("Score", f"{matching['match_score']}/100")
    
    # Skills breakdown
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("✅ Matched Skills")
        matched = matching['matched_skills']
        if matched:
            for skill in matched[:5]:
                st.write(f"• {skill}")
            if len(matched) > 5:
                st.write(f"... +{len(matched)-5} more")
        else:
            st.write("No direct matches found")
    
    with col2:
        st.subheader("❌ Missing Skills")
        missing = matching['missing_skills']
        if missing:
            for skill in missing[:5]:
                st.write(f"• {skill}")
            if len(missing) > 5:
                st.write(f"... +{len(missing)-5} more")
        else:
            st.write("All skills matched!")
    
    with col3:
        st.subheader("🟡 Partial Matches")
        partial = matching['partial_skills']
        if partial:
            for skill in partial[:5]:
                st.write(f"• {skill}")
        else:
            st.write("No partial matches")
    
    # Skill gap analysis
    st.subheader("📊 Skill Gap Analysis")
    
    gaps = matching['skill_gap_analysis']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔴 High Priority")
        if gaps['high_priority']:
            for skill in gaps['high_priority'][:5]:
                st.write(f"• {skill}")
        else:
            st.write("None!")
    
    with col2:
        st.markdown("### 🟡 Medium Priority")
        if gaps['medium_priority']:
            for skill in gaps['medium_priority'][:5]:
                st.write(f"• {skill}")
        else:
            st.write("None!")
    
    with col3:
        st.markdown("### 🟢 Low Priority")
        if gaps['low_priority']:
            for skill in gaps['low_priority'][:5]:
                st.write(f"• {skill}")
        else:
            st.write("None!")
    
    # Keyword matching
    keyword_match = matching['keyword_match']
    st.subheader("🔑 Keyword Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Matched Keywords", keyword_match['matched_keywords'], keyword_match['total_job_keywords'])
        st.metric("Match %", f"{keyword_match['match_percentage']}%")
    
    with col2:
        st.write("**Top Matched Keywords**")
        for kw in keyword_match['matched_list'][:8]:
            st.write(f"• {kw}")
    
    return matching

def project_analysis_section():
    """Analyze projects in resume."""
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume first")
        return
    
    st.header("🚀 Project Analysis")
    
    analyzer = ProjectAnalyzer(st.session_state.resume_text)
    analysis = analyzer.analyze()
    
    # Overall project strength
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(
            create_score_chart(analysis['project_strength_score'], 'Project Strength'),
            use_container_width=True
        )
    
    with col2:
        st.metric("Total Projects Found", analysis['total_projects'])
    
    # Projects list
    if analysis['projects']:
        st.subheader("📌 Projects Detected")
        for i, project in enumerate(analysis['projects'], 1):
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"### {i}. {project['title']}")
                
                with col2:
                    tech_status = "✅" if project['has_technologies'] else "❌"
                    st.write(f"{tech_status} Technologies")
                
                with col3:
                    results_status = "✅" if project['has_results'] else "❌"
                    st.write(f"{results_status} Results")
                
                with col4:
                    desc_status = "✅" if project['has_description'] else "❌"
                    st.write(f"{desc_status} Description")
                
                st.write(project['description'][:200] + "...")
                st.metric("Strength Score", project['strength_score'])
    
    # Recommendations
    st.subheader("💡 Improvement Suggestions")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.write(f"{i}. {rec}")
    
    return analysis

def ml_prediction_section():
    """ML-based match prediction."""
    if not st.session_state.resume_text or not st.session_state.job_description:
        st.warning("⚠️ Please upload a resume and job description first")
        return
    
    st.header("🤖 ML-Based Match Prediction")
    
    classifier = MatchingClassifier()
    prediction = classifier.classify(
        st.session_state.resume_text,
        st.session_state.job_description
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(
            create_score_chart(prediction['match_score'], 'ML Predicted Score'),
            use_container_width=True
        )
    
    with col2:
        st.markdown(f"### {prediction['match_class']}")
        st.metric("Confidence", f"{prediction['confidence']}%")
        st.write(prediction['explanation'])
    
    return prediction

def ai_advisor_section(quality_analysis, ats_analysis, matching):
    """AI advisor with recommendations."""
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume first")
        return
    
    st.header("🧠 AI Advisor - Top 5 Improvements")
    
    recommendations = []
    
    # From quality analysis
    if quality_analysis:
        recommendations.extend(quality_analysis.get('recommendations', []))
    
    # From ATS analysis
    if ats_analysis:
        recommendations.extend(ats_analysis.get('recommendations', []))
    
    # From matching (if job provided)
    if matching:
        gaps = matching.get('skill_gap_analysis', {})
        if gaps.get('high_priority'):
            recommendations.append(f"Learn these high-priority skills: {', '.join(gaps['high_priority'][:3])}")
    
    # Remove duplicates and get top 5
    recommendations = list(dict.fromkeys(recommendations))[:5]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"### {i}. {rec}")
    
    # Job-specific suggestions
    if matching:
        st.subheader("💼 Job-Specific Suggestions")
        
        matched = matching.get('matched_skills', [])
        missing = matching.get('missing_skills', [])
        
        if matched:
            st.write(f"✅ **Leverage your strengths**: Highlight your experience with {', '.join(matched[:3])}")
        
        if missing:
            st.write(f"📚 **Focus on learning**: Priority is gaining skills in {', '.join(missing[:3])}")
        
        match_score = matching.get('match_score', 0)
        if match_score < 50:
            st.warning("This role may not be the best fit currently. Consider roles that align better with your experience.")

def report_generation_section():
    """Generate downloadable report."""
    st.header("📋 Generate Report")
    
    if not st.session_state.resume_text:
        st.warning("⚠️ Please upload a resume first")
        return
    
    if st.button("📥 Generate Summary Report"):
        report_text = f"""
RESUMEGUARD AI - ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESUME ANALYSIS COMPLETE
This is your comprehensive resume analysis report.

To view detailed analysis:
1. Use the Resume Quality Analysis tool for content improvement
2. Check the ATS Compatibility score for system parsing
3. Review the Evidence & Consistency checks
4. If you have a job description, run the Job Matching analysis

All scores are provided for guidance. Recommendations are rule-based.

Thank you for using ResumeGuard AI!
"""
        
        st.download_button(
            label="📥 Download Text Report",
            data=report_text,
            file_name=f"resumeguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        st.success("✅ Report generated!")

def main():
    """Main application."""
    init_session_state()
    
    # Header
    st.markdown("""
    # 🛡️ ResumeGuard AI
    *Professional Resume Analysis & Optimization Platform*
    
    ---
    """)
    
    # Sidebar
    with st.sidebar:
        st.title("📊 Navigation")
        page = st.radio(
            "Select Analysis",
            [
                "📄 Resume Upload",
                "⭐ Quality Analysis",
                "🤖 ATS Analyzer",
                "✅ Truth Checker",
                "📋 Job Analysis",
                "🎯 Job Matching",
                "🚀 Project Analysis",
                "🤖 ML Prediction",
                "🧠 AI Advisor",
                "📋 Reports"
            ]
        )
        
        st.divider()
        st.info("💡 **Tip**: Start by uploading your resume, then explore each analysis!")
    
    # Routes
    quality_results = None
    ats_results = None
    truth_results = None
    matching_results = None
    prediction_results = None
    
    if page == "📄 Resume Upload":
        upload_resume_section()
    
    elif page == "⭐ Quality Analysis":
        quality_results = quality_analysis_section()
    
    elif page == "🤖 ATS Analyzer":
        ats_results = ats_analysis_section()
    
    elif page == "✅ Truth Checker":
        truth_results = truth_checker_section()
    
    elif page == "📋 Job Analysis":
        job_analysis_section()
    
    elif page == "🎯 Job Matching":
        quality_results = quality_analysis_section() if not quality_results else quality_results
        ats_results = ats_analysis_section() if not ats_results else ats_results
        truth_results = truth_checker_section() if not truth_results else truth_results
        matching_results = matching_section(quality_results, ats_results, truth_results)
    
    elif page == "🚀 Project Analysis":
        project_analysis_section()
    
    elif page == "🤖 ML Prediction":
        job_analysis_section()
        prediction_results = ml_prediction_section()
    
    elif page == "🧠 AI Advisor":
        quality_results = quality_analysis_section() if not quality_results else quality_results
        ats_results = ats_analysis_section() if not ats_results else ats_results
        job_analysis_section()
        matching_results = matching_section(quality_results, ats_results, truth_results) if not matching_results else matching_results
        ai_advisor_section(quality_results, ats_results, matching_results)
    
    elif page == "📋 Reports":
        report_generation_section()
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    **ResumeGuard AI v1.0** | Made with ❤️ for Data Science Students
    
    *Disclaimer*: All scores are estimates and provided for guidance only. 
    Not a substitute for professional resume review.
    """)

if __name__ == "__main__":
    main()
