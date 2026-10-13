"""Resume vs Job Matching Engine"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.helpers import extract_skills, similarity_score
from utils.constants import COLOR_HIGH_PRIORITY, COLOR_MEDIUM_PRIORITY, COLOR_LOW_PRIORITY


class MatchingEngine:
    """Match resume against job description."""
    
    def __init__(self, resume_text, job_description):
        self.resume_text = resume_text
        self.job_description = job_description
        self.resume_lower = resume_text.lower()
        self.job_lower = job_description.lower()
    
    def analyze(self):
        """Run comprehensive job matching analysis."""
        return {
            'match_score': self.calculate_match_score(),
            'matched_skills': self.get_matched_skills(),
            'missing_skills': self.get_missing_skills(),
            'partial_skills': self.get_partial_matches(),
            'skill_gap_analysis': self.analyze_skill_gaps(),
            'keyword_match': self.analyze_keyword_match(),
            'match_summary': self.generate_match_summary()
        }
    
    def calculate_match_score(self):
        """Calculate overall job match score (0-100)."""
        scores = {
            'skill_match': self._calculate_skill_match(),
            'keyword_match': self._calculate_keyword_match(),
            'experience_match': self._calculate_experience_match(),
            'requirement_coverage': self._calculate_requirement_coverage()
        }
        
        # Weighted average
        weighted_score = (
            scores['skill_match'] * 0.35 +
            scores['keyword_match'] * 0.25 +
            scores['experience_match'] * 0.25 +
            scores['requirement_coverage'] * 0.15
        )
        
        return int(min(100, max(0, weighted_score)))
    
    def _calculate_skill_match(self):
        """Calculate skill match percentage."""
        resume_skills = extract_skills(self.resume_text)
        job_skills = extract_skills(self.job_description)
        
        if not job_skills:
            return 50
        
        matched = 0
        for skill in job_skills:
            if skill.lower() in [s.lower() for s in resume_skills]:
                matched += 1
        
        return (matched / len(job_skills)) * 100 if job_skills else 0
    
    def _calculate_keyword_match(self):
        """Calculate keyword overlap using TF-IDF cosine similarity."""
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform([self.resume_text, self.job_description])
            similarity = cosine_similarity(vectors)[0][1]
            return similarity * 100
        except:
            return 50
    
    def _calculate_experience_match(self):
        """Calculate experience level match."""
        score = 50
        
        # Extract experience from job
        job_exp_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        job_exp_match = re.search(job_exp_pattern, self.job_lower)
        job_years = int(job_exp_match.group(1)) if job_exp_match else 0
        
        # Extract experience from resume
        resume_years = self._extract_years_from_resume()
        
        if job_years == 0:
            score = 100
        elif resume_years >= job_years:
            score = 100
        elif resume_years >= job_years * 0.7:
            score = 80
        elif resume_years >= job_years * 0.4:
            score = 60
        else:
            score = 30
        
        return score
    
    def _extract_years_from_resume(self):
        """Extract years of experience from resume."""
        # Count years mentioned
        years_pattern = r'(201|202)\d\s*[-–]\s*(201|202)\d'
        periods = re.findall(years_pattern, self.resume_text)
        
        total_years = 0
        for period in periods:
            # Simple calculation
            total_years += 1
        
        return total_years if total_years > 0 else 3  # Default to 3
    
    def _calculate_requirement_coverage(self):
        """Calculate how many job requirements are covered."""
        # Extract education keywords
        education_keywords = ['bachelor', 'master', 'degree', 'university', 'college']
        education_count = sum(1 for keyword in education_keywords if keyword in self.resume_lower)
        
        certification_keywords = ['certified', 'certification', 'credential']
        certification_count = sum(1 for keyword in certification_keywords if keyword in self.resume_lower)
        
        score = 0
        if education_count > 0:
            score += 40
        if certification_count > 0:
            score += 30
        
        # Check for relevant projects
        project_keywords = ['project', 'developed', 'built', 'created']
        if sum(1 for keyword in project_keywords if keyword in self.resume_lower) > 0:
            score += 30
        
        return min(100, score)
    
    def get_matched_skills(self):
        """Get skills that are both in resume and job description."""
        resume_skills = extract_skills(self.resume_text)
        job_skills = extract_skills(self.job_description)
        
        matched = []
        for skill in job_skills:
            for resume_skill in resume_skills:
                if skill.lower() == resume_skill.lower():
                    matched.append(skill)
                    break
        
        return matched
    
    def get_missing_skills(self):
        """Get skills required in job but missing in resume."""
        resume_skills = extract_skills(self.resume_text)
        job_skills = extract_skills(self.job_description)
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        
        missing = []
        for skill in job_skills:
            if skill.lower() not in resume_skills_lower:
                missing.append(skill)
        
        return missing
    
    def get_partial_matches(self):
        """Get skills with partial matches (related technologies)."""
        resume_skills = extract_skills(self.resume_text)
        job_skills = extract_skills(self.job_description)
        
        partial = []
        
        # Define skill relationships
        related_skills = {
            'React': ['Angular', 'Vue', 'Frontend'],
            'Python': ['Django', 'Flask', 'Data Science'],
            'Java': ['Spring', 'Backend'],
            'SQL': ['Database', 'PostgreSQL', 'MySQL'],
            'AWS': ['Cloud', 'Azure', 'GCP'],
            'Machine Learning': ['AI', 'Deep Learning', 'TensorFlow'],
        }
        
        for skill in job_skills:
            if skill not in resume_skills and skill not in partial:
                for resume_skill in resume_skills:
                    for base_skill, related in related_skills.items():
                        if base_skill.lower() == resume_skill.lower() and skill in related:
                            partial.append(skill)
                            break
        
        return partial
    
    def analyze_skill_gaps(self):
        """Analyze skill gaps with priority levels."""
        missing = self.get_missing_skills()
        
        gaps = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': []
        }
        
        # Categorize by frequency and importance
        technical_keywords = ['python', 'java', 'machine learning', 'aws', 'kubernetes']
        soft_keywords = ['communication', 'leadership', 'teamwork']
        
        for skill in missing:
            skill_lower = skill.lower()
            
            if any(tech in skill_lower for tech in technical_keywords):
                gaps['high_priority'].append(skill)
            elif any(soft in skill_lower for soft in soft_keywords):
                gaps['low_priority'].append(skill)
            else:
                gaps['medium_priority'].append(skill)
        
        return gaps
    
    def analyze_keyword_match(self):
        """Analyze keyword overlap between resume and job."""
        # Extract important keywords
        job_keywords = self._extract_important_keywords(self.job_description)
        resume_keywords = self._extract_important_keywords(self.resume_text)
        
        matched_keywords = []
        for keyword in job_keywords:
            if keyword in resume_keywords:
                matched_keywords.append(keyword)
        
        match_percentage = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        
        return {
            'total_job_keywords': len(job_keywords),
            'matched_keywords': len(matched_keywords),
            'match_percentage': int(match_percentage),
            'matched_list': matched_keywords[:10],
            'missing_keywords': [kw for kw in job_keywords if kw not in matched_keywords][:10]
        }
    
    def _extract_important_keywords(self, text):
        """Extract important keywords from text."""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'in', 'to', 'is', 'of', 'with'}
        
        words = text.lower().split()
        important = [
            word.strip('.,!?;:') for word in words
            if len(word) > 3 and word.lower().strip('.,!?;:') not in stop_words
        ]
        
        return list(set(important))
    
    def generate_match_summary(self):
        """Generate a summary of the match."""
        score = self.calculate_match_score()
        
        if score >= 75:
            summary = 'Strong Match'
            description = 'You meet most of the job requirements'
        elif score >= 50:
            summary = 'Moderate Match'
            description = 'You meet some requirements, but skill gaps exist'
        else:
            summary = 'Low Match'
            description = 'Consider gaining additional skills for this role'
        
        return {
            'summary': summary,
            'description': description,
            'score': score
        }


def compare_resume_job(resume_text, job_description):
    """Compare resume against job description."""
    matcher = MatchingEngine(resume_text, job_description)
    return matcher.analyze()
