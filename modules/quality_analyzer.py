"""Resume quality analysis module"""

import re
from utils.helpers import (
    tokenize_text, extract_keywords, find_section_content,
    find_repeated_words, extract_skills, calculate_text_density
)
from utils.constants import STANDARD_SECTIONS, QUALITY_WEIGHTS, VAGUE_PHRASES


class QualityAnalyzer:
    """Analyze resume quality and provide improvement suggestions."""
    
    def __init__(self, resume_text):
        self.resume_text = resume_text
        self.text_lower = resume_text.lower()
        self.sections_found = {}
        self._identify_sections()
    
    def _identify_sections(self):
        """Identify which sections are present in resume."""
        for section in STANDARD_SECTIONS:
            pattern = rf'\b{section}\b'
            self.sections_found[section] = bool(re.search(pattern, self.text_lower))
    
    def analyze(self):
        """Run comprehensive quality analysis."""
        return {
            'overall_score': self.calculate_overall_score(),
            'completeness_score': self.analyze_completeness(),
            'content_score': self.analyze_content_quality(),
            'keyword_score': self.analyze_keywords(),
            'grammar_score': self.analyze_grammar(),
            'formatting_score': self.analyze_formatting(),
            'sections_analysis': self.analyze_sections(),
            'issues': self.identify_issues(),
            'recommendations': self.get_recommendations()
        }
    
    def calculate_overall_score(self):
        """Calculate overall resume quality score (0-100)."""
        scores = {
            'completeness': self.analyze_completeness(),
            'content_quality': self.analyze_content_quality(),
            'keyword_relevance': self.analyze_keywords(),
            'grammar': self.analyze_grammar(),
            'formatting': self.analyze_formatting()
        }
        
        weighted_score = sum(
            scores[key] * QUALITY_WEIGHTS[key]
            for key in scores.keys()
        )
        return min(100, max(0, int(weighted_score)))
    
    def analyze_completeness(self):
        """Analyze section completeness (0-100)."""
        present_sections = sum(1 for found in self.sections_found.values() if found)
        score = (present_sections / len(STANDARD_SECTIONS)) * 100
        return int(score)
    
    def analyze_content_quality(self):
        """Analyze content quality based on descriptions (0-100)."""
        score = 0
        word_count = len(tokenize_text(self.resume_text))
        
        # Check word count (ideal 400-800)
        if 400 <= word_count <= 800:
            score += 30
        elif 200 <= word_count <= 1200:
            score += 15
        
        # Check for bullet points/structured format
        bullet_count = self.resume_text.count('•') + self.resume_text.count('-')
        if bullet_count >= 5:
            score += 30
        
        # Check for action verbs
        action_verbs = ['developed', 'designed', 'implemented', 'managed', 'led', 
                       'created', 'built', 'improved', 'optimized', 'increased']
        verb_count = sum(1 for verb in action_verbs if verb in self.text_lower)
        if verb_count >= 5:
            score += 20
        
        # Check for vague language
        vague_count = sum(1 for phrase in VAGUE_PHRASES if phrase in self.text_lower)
        if vague_count > 0:
            score -= min(20, vague_count * 2)
        
        # Check for quantifiable achievements
        if re.search(r'(\d+%|\d+x|\$\d+|increased.*\d+)', self.resume_text):
            score += 20
        
        return min(100, max(0, score))
    
    def analyze_keywords(self):
        """Analyze keyword relevance and diversity (0-100)."""
        keywords = extract_keywords(self.resume_text, top_n=10)
        skills = extract_skills(self.resume_text)
        
        score = 0
        
        # Diverse keywords
        if len(keywords) >= 8:
            score += 40
        else:
            score += len(keywords) * 5
        
        # Skills mentioned
        if len(skills) >= 10:
            score += 40
        elif len(skills) >= 5:
            score += 20
        else:
            score += len(skills) * 4
        
        # Common technical terms
        tech_terms = ['python', 'java', 'sql', 'machine learning', 'cloud', 'api']
        tech_count = sum(1 for term in tech_terms if term in self.text_lower)
        score += tech_count * 5
        
        return min(100, max(0, score))
    
    def analyze_grammar(self):
        """Analyze grammar and language quality (0-100)."""
        score = 85  # Start with good score
        
        # Check for common grammar issues
        issues = [
            (r'\bi\s', 'capitalization'),
            (r'  ', 'double spaces'),
            (r',\s{2,}', 'formatting'),
        ]
        
        issue_count = 0
        for pattern, _ in issues:
            issue_count += len(re.findall(pattern, self.resume_text, re.IGNORECASE))
        
        score -= min(30, issue_count * 2)
        return max(0, score)
    
    def analyze_formatting(self):
        """Analyze formatting and structure (0-100)."""
        score = 0
        
        # Check for consistent formatting
        if self.resume_text.count('\n') > 10:
            score += 20
        
        # Check for section headers
        headers = sum(1 for section in STANDARD_SECTIONS if section in self.text_lower)
        score += headers * 10
        
        # Check line breaks and spacing
        if '\n\n' in self.resume_text:
            score += 20
        
        # Check for consistent capitalization of headers
        if re.search(r'[A-Z]{2,}', self.resume_text):
            score += 20
        
        # Check for consistent bullet points
        if (self.resume_text.count('•') > 3 or self.resume_text.count('-') > 3):
            score += 20
        
        return min(100, max(0, score))
    
    def analyze_sections(self):
        """Analyze individual sections."""
        analysis = {}
        
        for section in STANDARD_SECTIONS:
            section_text = find_section_content(self.resume_text, section)
            analysis[section.title()] = {
                'present': self.sections_found.get(section, False),
                'length': len(tokenize_text(section_text)) if section_text else 0,
                'quality': self._evaluate_section_quality(section, section_text)
            }
        
        return analysis
    
    def _evaluate_section_quality(self, section, content):
        """Evaluate quality of a specific section."""
        if not content:
            return 'Missing'
        
        word_count = len(tokenize_text(content))
        
        if section == 'summary':
            if 50 <= word_count <= 150:
                return 'Good'
            else:
                return 'Needs Revision'
        
        elif section == 'skills':
            if word_count >= 10:
                return 'Good'
            else:
                return 'Needs Expansion'
        
        elif section in ['experience', 'projects']:
            if word_count >= 100:
                return 'Good'
            else:
                return 'Needs Detail'
        
        elif section == 'education':
            if word_count >= 20:
                return 'Good'
            else:
                return 'Needs Detail'
        
        return 'Fair'
    
    def identify_issues(self):
        """Identify specific issues in resume."""
        issues = []
        
        # Check for missing sections
        for section in STANDARD_SECTIONS:
            if not self.sections_found[section]:
                issues.append({
                    'type': 'Missing Section',
                    'section': section.title(),
                    'severity': 'High',
                    'suggestion': f'Add {section} section to improve completeness'
                })
        
        # Check for weak descriptions
        repeated = find_repeated_words(self.resume_text, min_count=3)
        if repeated:
            issues.append({
                'type': 'Repeated Words',
                'words': list(repeated.keys())[:5],
                'severity': 'Medium',
                'suggestion': 'Vary vocabulary to avoid repetitive language'
            })
        
        # Check for vague claims
        vague_phrases = [phrase for phrase in VAGUE_PHRASES if phrase in self.text_lower]
        if vague_phrases:
            issues.append({
                'type': 'Vague Language',
                'phrases': vague_phrases[:5],
                'severity': 'Medium',
                'suggestion': 'Use specific, measurable descriptions instead'
            })
        
        # Check word count
        word_count = len(tokenize_text(self.resume_text))
        if word_count < 200:
            issues.append({
                'type': 'Too Short',
                'word_count': word_count,
                'severity': 'High',
                'suggestion': 'Expand resume to include more details'
            })
        elif word_count > 1500:
            issues.append({
                'type': 'Too Long',
                'word_count': word_count,
                'severity': 'Medium',
                'suggestion': 'Condense resume to highlight most relevant information'
            })
        
        return issues
    
    def get_recommendations(self):
        """Generate improvement recommendations."""
        recommendations = []
        
        score = self.calculate_overall_score()
        
        if not self.sections_found.get('summary'):
            recommendations.append('Add a professional summary at the top')
        
        if self.analyze_content_quality() < 60:
            recommendations.append('Add more action verbs and quantifiable results')
        
        if self.analyze_keywords() < 60:
            recommendations.append('Include more relevant technical skills and keywords')
        
        if not any('github' in self.text_lower or 'portfolio' in self.text_lower for _ in [1]):
            if 'developer' in self.text_lower or 'engineer' in self.text_lower:
                recommendations.append('Add GitHub or portfolio link for technical roles')
        
        repeated = find_repeated_words(self.resume_text, min_count=3)
        if len(repeated) > 3:
            recommendations.append('Reduce repeated words and phrases')
        
        word_count = len(tokenize_text(self.resume_text))
        if word_count < 300:
            recommendations.append('Expand descriptions with more specific achievements')
        
        if self.analyze_formatting() < 60:
            recommendations.append('Improve formatting with consistent bullet points and spacing')
        
        return recommendations[:5]  # Return top 5 recommendations
