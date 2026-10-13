"""Job Description Analyzer - Extract skills and requirements"""

import re
from collections import Counter
from utils.helpers import tokenize_text, extract_keywords, extract_skills


class JobAnalyzer:
    """Analyze job descriptions to extract requirements and skills."""
    
    SKILL_CATEGORIES = {
        'programming_languages': [
            'python', 'java', 'javascript', 'typescript', 'cpp', 'c#', 'csharp',
            'php', 'ruby', 'go', 'rust', 'kotlin', 'swift', 'objective-c'
        ],
        'web_technologies': [
            'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'node.js',
            'express', 'django', 'flask', 'asp.net', 'spring', 'fastapi'
        ],
        'databases': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'cassandra', 'redis',
            'dynamodb', 'elasticsearch', 'oracle', 'sqlite'
        ],
        'cloud_platforms': [
            'aws', 'amazon web services', 'gcp', 'google cloud', 'azure',
            'microsoft azure', 'heroku', 'digital ocean'
        ],
        'devops_tools': [
            'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'git',
            'terraform', 'ansible', 'ci/cd', 'ci cd'
        ],
        'data_science': [
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy'
        ],
        'tools_platforms': [
            'jira', 'confluence', 'slack', 'asana', 'trello', 'figma',
            'postman', 'swagger', 'linux', 'unix'
        ]
    }
    
    REQUIREMENT_INDICATORS = [
        'required', 'must have', 'essential', 'mandatory',
        'min', 'minimum', 'years of experience'
    ]
    
    NICE_TO_HAVE_INDICATORS = [
        'preferred', 'nice to have', 'bonus', 'additional',
        'familiarity', 'knowledge of'
    ]
    
    def __init__(self, job_description):
        self.job_description = job_description
        self.text_lower = job_description.lower()
        self.tokens = tokenize_text(job_description)
    
    def analyze(self):
        """Run comprehensive job analysis."""
        return {
            'extracted_skills': self.extract_skills(),
            'required_skills': self.extract_required_skills(),
            'nice_to_have_skills': self.extract_nice_to_have_skills(),
            'keywords': self.extract_keywords(),
            'experience_level': self.determine_experience_level(),
            'job_category': self.categorize_job(),
            'key_requirements': self.extract_key_requirements(),
            'technologies': self.identify_technologies()
        }
    
    def extract_skills(self):
        """Extract all skills mentioned in job description."""
        skills = extract_skills(self.job_description)
        
        # Add more granular skill extraction
        for category, skill_list in self.SKILL_CATEGORIES.items():
            for skill in skill_list:
                if skill in self.text_lower:
                    skill_title = skill.replace('-', ' ').title()
                    if skill_title not in skills:
                        skills.append(skill_title)
        
        return list(set(skills))
    
    def extract_required_skills(self):
        """Extract skills that are marked as required."""
        required = []
        
        # Look for required/must have indicators
        for indicator in self.REQUIREMENT_INDICATORS:
            pattern = rf'{indicator}.*?(?=[.!?]|\n|required|preferred)'
            matches = re.finditer(pattern, self.text_lower, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                text_chunk = match.group(0)
                # Extract skills from this chunk
                for category, skill_list in self.SKILL_CATEGORIES.items():
                    for skill in skill_list:
                        if skill in text_chunk.lower():
                            if skill.title() not in required:
                                required.append(skill.replace('-', ' ').title())
        
        return required if required else self.extract_skills()[:10]
    
    def extract_nice_to_have_skills(self):
        """Extract skills that are marked as nice to have."""
        nice_to_have = []
        
        for indicator in self.NICE_TO_HAVE_INDICATORS:
            pattern = rf'{indicator}.*?(?=[.!?]|\n|required|must have)'
            matches = re.finditer(pattern, self.text_lower, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                text_chunk = match.group(0)
                for category, skill_list in self.SKILL_CATEGORIES.items():
                    for skill in skill_list:
                        if skill in text_chunk.lower():
                            if skill.title() not in nice_to_have:
                                nice_to_have.append(skill.replace('-', ' ').title())
        
        return nice_to_have
    
    def extract_keywords(self):
        """Extract important keywords from job description."""
        keywords = extract_keywords(self.job_description, top_n=20)
        keyword_list = [word for word, _ in keywords]
        return keyword_list
    
    def determine_experience_level(self):
        """Determine required experience level."""
        text = self.text_lower
        
        # Check for experience indicators
        if 'senior' in text or 'lead' in text or '7+' in text or '10+' in text:
            level = 'Senior'
            years = self._extract_years_experience()
        elif 'mid-level' in text or 'mid level' in text or '3+' in text or '5+' in text:
            level = 'Mid-Level'
            years = self._extract_years_experience()
        elif 'junior' in text or 'entry' in text or '0-2' in text or '1+' in text:
            level = 'Junior'
            years = self._extract_years_experience()
        else:
            level = 'Not Specified'
            years = self._extract_years_experience()
        
        return {
            'level': level,
            'years_required': years
        }
    
    def _extract_years_experience(self):
        """Extract years of experience requirement."""
        pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        matches = re.findall(pattern, self.text_lower)
        if matches:
            return int(matches[0])
        return None
    
    def categorize_job(self):
        """Categorize the job based on keywords."""
        text = self.text_lower
        
        categories = {
            'Data Science': ['data scientist', 'machine learning', 'ml engineer', 'deep learning'],
            'Web Development': ['web developer', 'frontend', 'backend', 'full stack', 'react', 'angular'],
            'DevOps': ['devops', 'site reliability', 'sre', 'infrastructure', 'kubernetes', 'docker'],
            'Cloud Engineering': ['cloud architect', 'cloud engineer', 'aws', 'azure', 'gcp'],
            'Software Engineering': ['software engineer', 'backend engineer', 'senior engineer'],
            'Product Management': ['product manager', 'product lead', 'product owner'],
            'Data Engineering': ['data engineer', 'etl', 'data pipeline']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'General Software/Engineering Role'
    
    def extract_key_requirements(self):
        """Extract key job requirements."""
        requirements = []
        
        # Look for requirement sections
        requirement_patterns = [
            r'requirements?:?(.*?)(?=preferred|nice to have|compensation)',
            r'(?:key\s+)?responsibilities?:?(.*?)(?=requirements?|qualifications?)',
            r'qualifications?:?(.*?)(?=responsibilities?|requirements?)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.finditer(pattern, self.text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                chunk = match.group(1)
                # Split by bullet points or lines
                lines = re.split(r'[\n•-]', chunk)
                for line in lines:
                    line = line.strip()
                    if len(line) > 10 and len(line) < 200:
                        requirements.append(line[:150])
        
        return requirements[:10]
    
    def identify_technologies(self):
        """Identify all mentioned technologies."""
        technologies = {
            'languages': [],
            'web_frameworks': [],
            'databases': [],
            'cloud_services': [],
            'devops': []
        }
        
        for lang in self.SKILL_CATEGORIES['programming_languages']:
            if lang in self.text_lower:
                technologies['languages'].append(lang.title())
        
        for framework in self.SKILL_CATEGORIES['web_technologies']:
            if framework in self.text_lower:
                technologies['web_frameworks'].append(framework.title())
        
        for db in self.SKILL_CATEGORIES['databases']:
            if db in self.text_lower:
                technologies['databases'].append(db.title())
        
        for cloud in self.SKILL_CATEGORIES['cloud_platforms']:
            if cloud in self.text_lower:
                technologies['cloud_services'].append(cloud.title())
        
        for tool in self.SKILL_CATEGORIES['devops_tools']:
            if tool in self.text_lower:
                technologies['devops'].append(tool.title())
        
        return technologies


def parse_job_description(job_text):
    """Parse a job description and return structured data."""
    analyzer = JobAnalyzer(job_text)
    return analyzer.analyze()
