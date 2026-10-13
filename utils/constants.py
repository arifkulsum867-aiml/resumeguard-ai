"""Constants for ResumeGuard AI"""

# Score ranges and thresholds
QUALITY_SCORE_EXCELLENT = 80
QUALITY_SCORE_GOOD = 60
QUALITY_SCORE_FAIR = 40

ATS_SCORE_EXCELLENT = 80
ATS_SCORE_GOOD = 60
ATS_SCORE_FAIR = 40

MATCH_SCORE_STRONG = 75
MATCH_SCORE_MODERATE = 50
MATCH_SCORE_LOW = 25

# Weights for quality score calculation
QUALITY_WEIGHTS = {
    'completeness': 0.20,
    'content_quality': 0.30,
    'keyword_relevance': 0.20,
    'grammar': 0.15,
    'formatting': 0.15
}

# ATS score components
ATS_WEIGHTS = {
    'section_names': 0.25,
    'keyword_density': 0.25,
    'structure': 0.25,
    'formatting': 0.25
}

# Colors for visualizations
COLOR_EXCELLENT = '#00cc44'  # Green
COLOR_GOOD = '#4499ff'       # Blue
COLOR_FAIR = '#ffaa00'       # Orange
COLOR_POOR = '#ff3333'       # Red

COLOR_MATCHED = '#00cc44'
COLOR_MISSING = '#ff3333'
COLOR_PARTIAL = '#ffaa00'

# Priority colors
COLOR_HIGH_PRIORITY = '#ff3333'
COLOR_MEDIUM_PRIORITY = '#ffaa00'
COLOR_LOW_PRIORITY = '#4499ff'

# Standard resume sections
STANDARD_SECTIONS = [
    'summary',
    'education',
    'experience',
    'skills',
    'projects',
    'certifications'
]

# Skills categories
SKILLS_CATEGORIES = {
    'technical': ['python', 'java', 'javascript', 'sql', 'c++', 'typescript'],
    'web_development': ['react', 'angular', 'vue', 'nodejs', 'html', 'css', 'javascript'],
    'data_science': ['machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'],
    'cloud': ['aws', 'gcp', 'azure', 'docker', 'kubernetes'],
    'databases': ['sql', 'mongodb', 'postgresql', 'mysql', 'redis'],
    'tools': ['git', 'jira', 'jenkins', 'docker', 'kubernetes'],
    'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving']
}

# Common keywords by industry
INDUSTRY_KEYWORDS = {
    'data_science': ['analysis', 'machine learning', 'prediction', 'model', 'data', 'insights'],
    'web_development': ['frontend', 'backend', 'api', 'database', 'responsive', 'deployment'],
    'devops': ['deployment', 'infrastructure', 'automation', 'monitoring', 'scaling', 'ci/cd']
}

# Vague language patterns
VAGUE_PHRASES = [
    'responsible for',
    'worked on',
    'involved in',
    'helped with',
    'contributed to',
    'participated in',
    'collaborated with'
]

# Maximum length for descriptions
MAX_DESCRIPTION_LENGTH = 500
MIN_DESCRIPTION_LENGTH = 20

# Minimum project requirements
MIN_PROJECT_ELEMENTS = {
    'technologies': 1,
    'description': 1,
    'results': 1
}

# File upload limits (in bytes)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'txt']
