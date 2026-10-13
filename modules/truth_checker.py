"""AI Truth & Consistency Checker - Detect vague claims and verify evidence"""

import re
from datetime import datetime
from utils.helpers import extract_dates, tokenize_text


class TruthChecker:
    """Check resume for vague claims and consistency issues."""
    
    VAGUE_CLAIMS = {
        'expert': 'needs evidence',
        'expert in': 'needs evidence',
        'excellent': 'needs evidence',
        'excellent at': 'needs evidence',
        'very good': 'needs evidence',
        'great': 'needs evidence',
        'passionate about': 'needs evidence',
        'proficient in': 'may need evidence',
        'familiar with': 'may need evidence',
        'knowledge of': 'may need evidence',
        'worked on': 'needs evidence',
        'responsible for': 'needs evidence',
        'involved in': 'needs evidence',
        'helped with': 'needs evidence',
        'contributed to': 'may need evidence',
    }
    
    EVIDENCE_KEYWORDS = {
        'projects': ['developed', 'built', 'created', 'implemented', 'designed'],
        'results': ['increased', 'improved', 'reduced', 'achieved', 'delivered', '%', 'by', '$'],
        'certifications': ['certified', 'certification', 'credential', 'award', 'trained'],
        'measurable': ['%', 'x', '$', 'number', 'count', 'achieved']
    }
    
    def __init__(self, resume_text):
        self.resume_text = resume_text
        self.text_lower = resume_text.lower()
        self.sentences = re.split(r'[.!?]', resume_text)
    
    def analyze(self):
        """Run comprehensive truth and consistency analysis."""
        return {
            'truth_score': self.calculate_truth_score(),
            'vague_claims': self.detect_vague_claims(),
            'evidence_strength': self.analyze_evidence_strength(),
            'consistency_issues': self.check_consistency(),
            'recommendations': self.get_recommendations()
        }
    
    def calculate_truth_score(self):
        """Calculate truth/evidence score (0-100)."""
        score = 100
        
        vague_issues = self.detect_vague_claims()
        score -= len(vague_issues) * 5
        
        consistency_issues = self.check_consistency()
        score -= len(consistency_issues) * 3
        
        evidence = self.analyze_evidence_strength()
        if evidence['total_evidence_score'] < 60:
            score -= 20
        
        return max(0, min(100, score))
    
    def detect_vague_claims(self):
        """Detect vague or unsupported claims."""
        issues = []
        
        for claim, severity in self.VAGUE_CLAIMS.items():
            pattern = rf'\b{re.escape(claim)}\b'
            matches = re.finditer(pattern, self.text_lower)
            
            for match in matches:
                # Find the sentence containing this claim
                char_pos = match.start()
                sentence_start = self.resume_text.rfind('.', 0, char_pos)
                sentence_end = self.resume_text.find('.', char_pos)
                
                if sentence_start == -1:
                    sentence_start = 0
                else:
                    sentence_start += 1
                
                if sentence_end == -1:
                    sentence_end = len(self.resume_text)
                
                sentence = self.resume_text[sentence_start:sentence_end].strip()
                
                issues.append({
                    'claim': claim,
                    'sentence': sentence[:100],
                    'severity': severity,
                    'suggestion': self._get_evidence_suggestion(claim)
                })
        
        return issues[:10]  # Return top 10 issues
    
    def _get_evidence_suggestion(self, claim):
        """Get suggestion for providing evidence."""
        suggestions = {
            'expert': 'Provide projects or results demonstrating expertise',
            'excellent': 'Add specific achievements or certifications',
            'very good': 'Include measurable results or examples',
            'great': 'Quantify the impact with metrics',
            'passionate': 'Show through specific projects or achievements',
            'proficient': 'Demonstrate with projects or years of experience',
            'familiar': 'Increase to "proficient" if you have real experience',
            'worked on': 'Specify your role and measurable impact',
            'responsible for': 'Add metrics showing results achieved',
            'involved in': 'Clarify your specific contributions',
            'helped': 'Upgrade to active role if possible'
        }
        
        for key, suggestion in suggestions.items():
            if key in claim:
                return suggestion
        
        return 'Add specific results or certifications to support this claim'
    
    def analyze_evidence_strength(self):
        """Analyze strength of evidence in resume."""
        scores = {
            'project_evidence': 0,
            'result_evidence': 0,
            'certification_evidence': 0,
            'measurable_evidence': 0,
            'total_evidence_score': 0
        }
        
        # Check for project mentions
        project_keywords = self.EVIDENCE_KEYWORDS['projects']
        project_count = sum(
            len(re.findall(rf'\b{keyword}\b', self.text_lower))
            for keyword in project_keywords
        )
        scores['project_evidence'] = min(25, project_count * 3)
        
        # Check for results/impact
        result_keywords = ['increased', 'improved', 'reduced', 'achieved', 'delivered']
        result_count = sum(
            len(re.findall(rf'\b{keyword}\b', self.text_lower))
            for keyword in result_keywords
        )
        scores['result_evidence'] = min(25, result_count * 3)
        
        # Check for certifications
        cert_keywords = ['certified', 'certification', 'certificate', 'award', 'credential']
        cert_count = sum(
            len(re.findall(rf'\b{keyword}\b', self.text_lower))
            for keyword in cert_keywords
        )
        scores['certification_evidence'] = min(20, cert_count * 4)
        
        # Check for measurable metrics
        measurable_count = len(re.findall(r'(\d+%|\d+x|\$\d+)', self.resume_text))
        scores['measurable_evidence'] = min(30, measurable_count * 3)
        
        # Calculate total
        scores['total_evidence_score'] = min(
            100,
            sum([
                scores['project_evidence'],
                scores['result_evidence'],
                scores['certification_evidence'],
                scores['measurable_evidence']
            ]) // 4
        )
        
        return scores
    
    def check_consistency(self):
        """Check for timeline and consistency issues."""
        issues = []
        
        # Extract dates
        dates = re.findall(r'\b(19|20)\d{2}\b', self.resume_text)
        
        if len(dates) < 2:
            issues.append({
                'type': 'Missing dates',
                'description': 'Resume lacks clear dates for timeline verification',
                'suggestion': 'Include years for all positions and education'
            })
            return issues
        
        # Extract year numbers
        years = sorted([int(date) for date in dates if date.isdigit()])
        
        # Check for impossible timeline
        current_year = datetime.now().year
        
        if max(years) > current_year:
            issues.append({
                'type': 'Future date',
                'description': f'Resume contains future dates (after {current_year})',
                'suggestion': 'Review and correct dates to ensure accuracy'
            })
        
        if min(years) < 1950:
            issues.append({
                'type': 'Unrealistic date',
                'description': 'Resume contains very old dates (before 1950)',
                'suggestion': 'Verify all dates are accurate'
            })
        
        # Check for unrealistic experience duration
        year_range = max(years) - min(years)
        if year_range > 50:
            issues.append({
                'type': 'Unrealistic experience',
                'description': f'Experience spans {year_range}+ years',
                'suggestion': 'Verify career timeline is accurate'
            })
        
        # Check for overlapping dates (if pattern detected)
        date_pairs = re.findall(
            r'(\d{4})\s*(?:[-–]|to|–)\s*(\d{4})',
            self.resume_text
        )
        
        if date_pairs:
            prev_end = None
            for start, end in date_pairs:
                if prev_end and int(start) < int(prev_end):
                    issues.append({
                        'type': 'Possible overlapping positions',
                        'description': 'Timeline suggests overlapping employment',
                        'suggestion': 'Clarify job timing if positions overlapped or adjust dates'
                    })
                    break
                prev_end = int(end)
        
        return issues
    
    def get_recommendations(self):
        """Get recommendations for improving evidence and truthfulness."""
        recommendations = []
        
        vague_claims = self.detect_vague_claims()
        if vague_claims:
            recommendations.append(
                f'Address {len(vague_claims)} vague claims with specific evidence'
            )
        
        evidence = self.analyze_evidence_strength()
        if evidence['project_evidence'] < 15:
            recommendations.append('Add more projects with specific technologies and results')
        
        if evidence['result_evidence'] < 15:
            recommendations.append('Include quantifiable results (% improvement, cost saved, etc.)')
        
        if evidence['certification_evidence'] < 10 and 'certificate' not in self.text_lower:
            recommendations.append('List any certifications or professional credentials')
        
        consistency = self.check_consistency()
        if consistency:
            recommendations.append(f'Review timeline - {len(consistency)} consistency issue(s) found')
        
        if evidence['measurable_evidence'] < 5:
            recommendations.append('Add metrics and numbers to quantify your impact')
        
        return recommendations[:5]
