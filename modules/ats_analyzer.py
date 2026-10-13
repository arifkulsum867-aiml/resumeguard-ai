"""ATS (Applicant Tracking System) compatibility analyzer"""

import re
from collections import Counter
from utils.helpers import tokenize_text, extract_keywords, extract_skills
from utils.constants import STANDARD_SECTIONS, ATS_WEIGHTS


class ATSAnalyzer:
    """Analyze resume compatibility with ATS systems."""
    
    def __init__(self, resume_text):
        self.resume_text = resume_text
        self.text_lower = resume_text.lower()
        self.tokens = tokenize_text(self.resume_text)
    
    def analyze(self):
        """Run comprehensive ATS analysis."""
        return {
            'ats_score': self.calculate_ats_score(),
            'section_names_score': self.check_section_names(),
            'keyword_density_score': self.analyze_keyword_density(),
            'structure_score': self.check_structure(),
            'formatting_score': self.check_formatting(),
            'issues': self.identify_ats_issues(),
            'recommendations': self.get_ats_recommendations()
        }
    
    def calculate_ats_score(self):
        """Calculate overall ATS compatibility score (0-100)."""
        scores = {
            'section_names': self.check_section_names(),
            'keyword_density': self.analyze_keyword_density(),
            'structure': self.check_structure(),
            'formatting': self.check_formatting()
        }
        
        weighted_score = sum(
            scores[key] * ATS_WEIGHTS[key]
            for key in scores.keys()
        )
        return min(100, max(0, int(weighted_score)))
    
    def check_section_names(self):
        """Check for standard section names (0-100)."""
        score = 0
        sections = STANDARD_SECTIONS
        
        found_sections = 0
        for section in sections:
            if re.search(rf'\b{section}\b', self.text_lower):
                found_sections += 1
        
        score = (found_sections / len(sections)) * 100
        
        # Bonus for having clear section headers
        if re.search(r'[A-Z]{2,}', self.resume_text):  # All caps headers
            score += 10
        
        return min(100, int(score))
    
    def analyze_keyword_density(self):
        """Analyze keyword density and relevance (0-100)."""
        keywords = extract_keywords(self.resume_text, top_n=20)
        skills = extract_skills(self.resume_text)
        
        score = 0
        
        # Check keyword diversity
        if len(keywords) >= 15:
            score += 35
        else:
            score += len(keywords) * 2
        
        # Check for technical skills
        tech_keywords = ['python', 'java', 'sql', 'machine learning', 'cloud', 'api',
                        'react', 'node', 'docker', 'kubernetes', 'aws', 'azure']
        tech_count = sum(1 for keyword in tech_keywords if keyword in self.text_lower)
        score += min(30, tech_count * 3)
        
        # Check for skill variations
        if len(skills) >= 5:
            score += 20
        
        # Check keyword frequency (should be moderate)
        keyword_counts = Counter([kw[0] for kw in keywords])
        max_frequency = max([count for _, count in keyword_counts.most_common(1)], default=0)
        
        if 2 <= max_frequency <= 5:
            score += 15
        
        return min(100, max(0, score))
    
    def check_structure(self):
        """Check resume structure and formatting (0-100)."""
        score = 50
        
        # Check for consistent bullet points
        bullet_count = self.resume_text.count('•') + self.resume_text.count('-')
        if bullet_count >= 10:
            score += 20
        
        # Check for line breaks (good spacing)
        line_breaks = self.resume_text.count('\n')
        if line_breaks >= 15:
            score += 15
        
        # Check for no tables or complex formatting
        if '<table>' not in self.text_lower and '|' not in self.resume_text:
            score += 15
        
        # Check for consistent formatting
        if self.resume_text.count('\n\n') >= 3:
            score += 10
        
        # Check for no images or graphics descriptions
        if 'image' not in self.text_lower and 'chart' not in self.text_lower:
            score += 10
        
        return min(100, max(0, score))
    
    def check_formatting(self):
        """Check file format and ATS-friendly formatting (0-100)."""
        score = 80
        
        # Check for problematic characters
        problematic_chars = ['©', '®', '™', '•', '→', '←']
        char_count = sum(1 for char in problematic_chars if char in self.resume_text)
        score -= min(30, char_count * 5)
        
        # Check for excessive special characters
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s\n\-\.]', self.resume_text))
        if special_char_count > 50:
            score -= min(20, special_char_count // 10)
        
        # Check for columns or complex layouts (not ATS friendly)
        if re.search(r'column|layout|table', self.text_lower):
            score -= 15
        
        # Check for standard fonts
        if 'calibri' in self.text_lower or 'arial' in self.text_lower or 'times' in self.text_lower:
            score += 5
        
        # Check for no PDFs with images
        # (We assume text extraction worked, so no heavy image usage)
        
        return min(100, max(0, score))
    
    def identify_ats_issues(self):
        """Identify ATS compatibility issues."""
        issues = []
        
        # Check for missing standard sections
        for section in STANDARD_SECTIONS:
            if not re.search(rf'\b{section}\b', self.text_lower):
                issues.append({
                    'issue': f'Missing standard section: {section.title()}',
                    'impact': 'Medium',
                    'solution': f'Add a clearly labeled {section.title()} section'
                })
        
        # Check for limited keywords
        keywords = extract_keywords(self.resume_text, top_n=20)
        if len(keywords) < 10:
            issues.append({
                'issue': 'Limited keyword diversity',
                'impact': 'High',
                'solution': 'Add more relevant technical terms and industry keywords'
            })
        
        # Check for problematic formatting
        if '<' in self.resume_text or '>' in self.resume_text:
            issues.append({
                'issue': 'Possible HTML or formatting tags',
                'impact': 'High',
                'solution': 'Ensure resume is plain text without HTML formatting'
            })
        
        # Check for no clear dates
        if not re.search(r'(19|20)\d{2}', self.resume_text):
            issues.append({
                'issue': 'No clear dates found',
                'impact': 'Medium',
                'solution': 'Include years for education and work experience'
            })
        
        # Check for unusual characters
        unusual_chars = re.findall(r'[^a-zA-Z0-9\s\n\-\.\,\:\;\(\)\/]', self.resume_text)
        if len(unusual_chars) > 20:
            issues.append({
                'issue': f'Many unusual characters ({len(unusual_chars)} found)',
                'impact': 'Medium',
                'solution': 'Replace special characters with standard ASCII alternatives'
            })
        
        return issues[:5]
    
    def get_ats_recommendations(self):
        """Get ATS optimization recommendations."""
        recommendations = []
        
        # Recommendation 1: Keywords
        if self.analyze_keyword_density() < 70:
            recommendations.append('Add more industry-relevant keywords and technical terms')
        
        # Recommendation 2: Section headers
        if self.check_section_names() < 70:
            recommendations.append('Use standard section headers like EDUCATION, EXPERIENCE, SKILLS')
        
        # Recommendation 3: Formatting
        if self.check_formatting() < 70:
            recommendations.append('Use simple formatting (bullet points, standard fonts)')
        
        # Recommendation 4: Structure
        if self.check_structure() < 70:
            recommendations.append('Improve structure with clear sections and bullet points')
        
        # Recommendation 5: Contact info
        if '@' not in self.resume_text and 'email' not in self.text_lower:
            recommendations.append('Ensure email address and phone number are clearly visible')
        
        # Recommendation 6: Dates
        if not re.search(r'(19|20)\d{2}', self.resume_text):
            recommendations.append('Include years for all positions and education')
        
        # Recommendation 7: Avoid images
        if 'photo' in self.text_lower or 'picture' in self.text_lower:
            recommendations.append('Remove photos or images (ATS cannot read them)')
        
        return recommendations[:5]
    
    def get_ats_score_explanation(self):
        """Get explanation of ATS score."""
        score = self.calculate_ats_score()
        
        if score >= 80:
            return "Excellent ATS compatibility. Your resume should parse well in most systems."
        elif score >= 60:
            return "Good ATS compatibility with some optimization opportunities."
        elif score >= 40:
            return "Fair ATS compatibility. Consider improvements for better parsing."
        else:
            return "Poor ATS compatibility. Significant improvements recommended."
