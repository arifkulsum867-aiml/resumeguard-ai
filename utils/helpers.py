import re
import string
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


COMMON_SKILLS = [
    'python', 'java', 'javascript', 'typescript', 'cpp', 'c#', 'csharp', 'php', 'ruby', 'go',
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra',
    'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask',
    'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'jenkins', 'git',
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'keras',
    'data analysis', 'data visualization', 'pandas', 'numpy', 'scikit-learn', 'matplotlib', 'plotly',
    'excel', 'tableau', 'power bi', 'looker',
    'agile', 'scrum', 'waterfall', 'jira', 'confluence',
    'leadership', 'communication', 'problem solving', 'project management', 'teamwork'
]

STOP_WORDS = set(stopwords.words('english'))

RESUME_SECTIONS = ['education', 'skills', 'experience', 'projects', 'certifications', 'summary']

VAGUE_CLAIMS = [
    'expert', 'excellent', 'very good', 'great', 'amazing', 'responsible for',
    'worked on', 'involved in', 'helped', 'collaborated', 'proficient', 'familiar with'
]


def extract_text(file_path):
    """Extract text from various file formats."""
    if file_path.endswith('.pdf'):
        return extract_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_txt(file_path)
    return None


def extract_pdf(file_path):
    """Extract text from PDF."""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None


def extract_docx(file_path):
    """Extract text from DOCX."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return None


def extract_txt(file_path):
    """Extract text from TXT."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return None


def clean_text(text):
    """Clean and normalize text."""
    text = text.lower()
    text = re.sub(r'[^\w\s\-\.]', '', text)
    return text.strip()


def tokenize_text(text):
    """Tokenize text into words."""
    try:
        return word_tokenize(text.lower())
    except:
        return text.lower().split()


def extract_keywords(text, top_n=20):
    """Extract top keywords from text."""
    tokens = tokenize_text(text)
    filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
    counter = Counter(filtered)
    return counter.most_common(top_n)


def extract_skills(text):
    """Extract skills from text."""
    text_lower = text.lower()
    found_skills = []
    for skill in COMMON_SKILLS:
        if skill in text_lower:
            found_skills.append(skill.title())
    return list(set(found_skills))


def find_section_content(text, section_name):
    """Find content of a specific section."""
    section_pattern = rf'{section_name}.*?(?=\n[A-Z]|\Z)'
    match = re.search(section_pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else ""


def find_repeated_words(text, min_count=3):
    """Find repeated words in text."""
    tokens = tokenize_text(text)
    filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 3]
    counter = Counter(filtered)
    return {word: count for word, count in counter.most_common() if count >= min_count}


def extract_dates(text):
    """Extract dates from text for consistency checking."""
    date_pattern = r'\b(19|20)\d{2}\b|\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(20|19)?\d{2}\b'
    dates = re.findall(date_pattern, text, re.IGNORECASE)
    return dates


def calculate_text_density(text):
    """Calculate keyword density."""
    if not text:
        return 0
    tokens = tokenize_text(text)
    return len(tokens)


def extract_emails(text):
    """Extract email addresses."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


def extract_phone_numbers(text):
    """Extract phone numbers."""
    phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
    return re.findall(phone_pattern, text)


def similarity_score(text1, text2):
    """Calculate text similarity score (0-1)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors)[0][1]
        return float(similarity)
    except:
        return 0.0


def word_frequency_analysis(text):
    """Analyze word frequency."""
    tokens = tokenize_text(text)
    filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
    return Counter(filtered).most_common(10)
