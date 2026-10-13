# ResumeGuard AI

A professional AI + Data Science web application that analyzes and improves your resume. ResumeGuard AI provides comprehensive insights on resume quality, ATS compatibility, job matching, and personalized improvement recommendations.

## Features

### 1. **Resume Upload & Processing**
- Support for PDF, DOCX, and TXT file formats
- Automatic text extraction and display
- Secure file handling

### 2. **Resume Quality Analysis**
- Overall Resume Quality Score (0-100)
- Section-wise analysis (Education, Skills, Projects, Experience, Certifications, Summary)
- Detection of:
  - Missing critical sections
  - Weak or vague descriptions
  - Repeated words and phrases
  - Poor wording suggestions

### 3. **ATS Analyzer**
- Estimated ATS Compatibility Score (0-100)
- Keyword optimization analysis
- Standard sections validation
- Resume structure assessment
- *Note: Score is estimated and for guidance only*

### 4. **AI Truth & Consistency Checker**
- Identifies vague claims needing evidence
- Suggests supporting materials (projects, certifications, results)
- Basic timeline and date consistency validation
- Non-accusatory feedback approach

### 5. **Job Description Analyzer**
- Extract skills, technologies, and keywords from job descriptions
- Identify key requirements and responsibilities
- Automatic skill categorization

### 6. **Resume vs Job Matching**
- Comprehensive job match score (0-100)
- Matched skills visualization
- Missing skills identification
- Skill Gap Analysis with priority levels (High/Medium/Low)

### 7. **Project Analyzer**
- Automatic project detection
- Project strength scoring based on:
  - Technology mentions
  - Impact/Results clarity
  - Description completeness
- Actionable feedback for improvement

### 8. **ML-Based Matching Model**
- Scikit-learn classification model for resume-job matching
- Features: skill overlap, keyword overlap, requirement coverage
- Predictions: Low Match, Moderate Match, Strong Match
- Model evaluation metrics included

### 9. **Interactive Dashboard**
- Resume Quality Score visualization
- ATS Score progress
- Job Match Score
- Evidence Strength indicator
- Project Strength tracker
- Skill gap charts
- Personalized recommendations

### 10. **AI Advisor**
- Top 5 resume improvement suggestions
- Job-specific recommendations
- Rule-based system (fallback when API unavailable)

### 11. **Demo Mode**
- Pre-loaded sample resumes
- Sample job descriptions
- Perfect for demonstrations without real data

### 12. **Report Generation**
- Download comprehensive PDF/text reports
- Includes all scores, gaps, and recommendations
- Professional formatting

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (run once):
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository. A private repository is a good
   choice if you do not want the source code to be public.
2. In Streamlit Community Cloud, create a new app and select the repository,
   branch, and `app.py` as the entry point.
3. Deploy the app. Streamlit Community Cloud installs the packages listed in
   `requirements.txt`.

The deployed app is available to people who can access its URL. Do not upload
real resumes unless you are comfortable processing them on the hosting service.

## Usage

1. **Upload Resume**: Start by uploading your resume (PDF, DOCX, or TXT)
2. **View Analysis**: Explore the Resume Quality Score and section analysis
3. **Check ATS**: See your estimated ATS compatibility score
4. **Add Job Description**: Paste a job description to match against
5. **View Matching**: See job match scores, skill gaps, and recommendations
6. **Review Improvements**: Read personalized suggestions
7. **Download Report**: Generate a comprehensive report with all findings

## Demo Mode

To test without uploading a resume:
1. Click the "Demo Mode" toggle in the sidebar
2. Select a sample resume and job description
3. Explore all features with pre-loaded data

## Technologies Used

- **Streamlit**: Interactive web framework
- **Pandas & NumPy**: Data processing
- **Scikit-learn**: Machine learning model
- **Plotly**: Interactive visualizations
- **python-docx**: DOCX file handling
- **PyPDF2/pdfplumber**: PDF file handling
- **NLTK**: Natural language processing

## Architecture

```
resumeguard_ai/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── modules/
│   ├── resume_processor.py        # File upload & parsing
│   ├── quality_analyzer.py        # Resume quality scoring
│   ├── ats_analyzer.py            # ATS compatibility
│   ├── truth_checker.py           # Evidence & consistency
│   ├── job_analyzer.py            # Job description parsing
│   ├── matching_engine.py         # Resume-job matching
│   ├── project_analyzer.py        # Project analysis
│   └── ml_model.py                # ML classification
├── utils/
│   ├── helpers.py                 # Utility functions
│   ├── demo_data.py               # Sample data
│   └── constants.py               # Constants
└── README.md
```

## Key Features Explained

### Resume Quality Score
Combines analysis of:
- Section completeness (20%)
- Content quality and descriptions (30%)
- Keyword relevance (20%)
- Grammar and language (15%)
- Formatting and structure (15%)

### ATS Score
Evaluates:
- Standard section names
- Keyword density
- Resume structure
- File format compatibility
- Spacing and formatting

### Job Match Score
Based on:
- Skill overlap with job requirements
- Keyword relevance
- Experience level matching
- Technology stack overlap
- Requirement coverage

### ML Model
Uses features like:
- Cosine similarity for text matching
- Skill overlap ratio
- Keyword frequency analysis
- Requirement satisfaction ratio

## Privacy & Data

- Resume uploads and extracted text are processed by the Python server running
  the app, not solely in the browser.
- The app code does not intentionally save uploaded resumes to persistent
  storage; extracted text is held in Streamlit session state while the session
  is active.
- When deployed, uploads are handled by the hosting service. Review that
  service's privacy and retention policies before uploading sensitive resumes.
- Demo mode uses only sample data

## Limitations & Disclaimers

- ATS scores are estimates and provided for guidance only
- ML predictions indicate likelihood based on feature matching
- Not a substitute for professional resume review
- AI suggestions are rule-based, not trained on external APIs
- Always verify information in your resume

## Version

Version 1.0.0 - August 2026

## Support

For issues or feature requests, please provide feedback directly in the application.

---

**Made with ❤️ for Data Science Students**
