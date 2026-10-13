"""Project Analyzer - Analyze projects mentioned in resume"""

import re
from utils.helpers import extract_skills, tokenize_text


class ProjectAnalyzer:
    """Analyze projects mentioned in resume."""
    
    PROJECT_INDICATORS = [
        'project', 'developed', 'built', 'created', 'implemented',
        'designed', 'engineered', 'application', 'system', 'software'
    ]
    
    RESULT_KEYWORDS = [
        'improved', 'increased', 'decreased', 'reduced', 'optimized',
        'achieved', 'delivered', 'accelerated', 'enhanced', 'strengthened'
    ]
    
    def __init__(self, resume_text):
        self.resume_text = resume_text
        self.text_lower = resume_text.lower()
    
    def analyze(self):
        """Run comprehensive project analysis."""
        projects = self.detect_projects()
        
        return {
            'total_projects': len(projects),
            'projects': [self.evaluate_project(p) for p in projects],
            'project_strength_score': self.calculate_project_strength_score(),
            'recommendations': self.get_project_recommendations()
        }
    
    def detect_projects(self):
        """Detect projects mentioned in resume."""
        projects = []
        
        # Split by common project separators
        sections = re.split(r'\n(?=[A-Z])', self.resume_text)
        
        for section in sections:
            section_lower = section.lower()
            
            # Check if this section mentions projects
            if any(indicator in section_lower for indicator in self.PROJECT_INDICATORS):
                # If it's a project section, split by bullet points
                if 'project' in section_lower:
                    items = re.split(r'[\n•-]\s*', section)
                    for item in items:
                        if len(item) > 20 and len(item) < 500:
                            projects.append(item.strip())
                else:
                    # Could be a single project
                    if len(section.strip()) > 50:
                        projects.append(section.strip())
        
        return projects[:10]  # Return top 10 projects
    
    def evaluate_project(self, project_text):
        """Evaluate a single project."""
        text_lower = project_text.lower()
        
        return {
            'title': self._extract_project_title(project_text),
            'description': project_text[:150],
            'has_technologies': self._check_technologies(text_lower),
            'has_results': self._check_results(text_lower),
            'has_description': self._check_description(project_text),
            'strength_score': self._calculate_project_score(project_text)
        }
    
    def _extract_project_title(self, project_text):
        """Extract project title from text."""
        # Usually first line or before first colon
        lines = project_text.split('\n')
        title = lines[0].strip()
        
        # Clean up
        title = re.sub(r'^[-•]\s*', '', title)
        if ':' in title:
            title = title.split(':')[0]
        
        return title[:50]
    
    def _check_technologies(self, text_lower):
        """Check if project mentions technologies."""
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql',
            'tensorflow', 'mongodb', 'aws', 'docker', 'api', 'rest'
        ]
        
        return any(tech in text_lower for tech in tech_keywords)
    
    def _check_results(self, text_lower):
        """Check if project mentions results/impact."""
        has_results = any(keyword in text_lower for keyword in self.RESULT_KEYWORDS)
        has_numbers = bool(re.search(r'\d+%|\d+x|\$\d+|increased by', text_lower))
        
        return has_results or has_numbers
    
    def _check_description(self, project_text):
        """Check if project has adequate description."""
        word_count = len(tokenize_text(project_text))
        return word_count >= 15  # Minimum 15 words
    
    def _calculate_project_score(self, project_text):
        """Calculate individual project strength score (0-100)."""
        score = 0
        text_lower = project_text.lower()
        
        # Has technologies (25 points)
        if self._check_technologies(text_lower):
            score += 25
        
        # Has results/metrics (35 points)
        if self._check_results(text_lower):
            score += 35
        
        # Has adequate description (20 points)
        if self._check_description(project_text):
            score += 20
        
        # Has multiple action verbs (20 points)
        action_verbs = ['developed', 'designed', 'implemented', 'created', 'built',
                       'optimized', 'improved', 'enhanced', 'deployed']
        verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        score += min(20, verb_count * 5)
        
        return min(100, score)
    
    def calculate_project_strength_score(self):
        """Calculate overall project strength score."""
        projects = self.detect_projects()
        
        if not projects:
            return 0
        
        total_score = sum(
            self._calculate_project_score(p) for p in projects
        )
        
        return int(total_score / len(projects))
    
    def get_project_recommendations(self):
        """Generate recommendations for improving projects."""
        recommendations = []
        
        projects = self.detect_projects()
        
        if not projects:
            recommendations.append('Add a Projects section with specific examples')
            return recommendations
        
        avg_score = self.calculate_project_strength_score()
        
        # Check for missing technologies
        tech_found = False
        for project in projects:
            if self._check_technologies(project.lower()):
                tech_found = True
                break
        
        if not tech_found:
            recommendations.append('Specify technologies used in each project')
        
        # Check for missing results
        results_found = False
        for project in projects:
            if self._check_results(project.lower()):
                results_found = True
                break
        
        if not results_found:
            recommendations.append('Include measurable results or impact for each project')
        
        # Check for descriptions
        desc_found = False
        for project in projects:
            if self._check_description(project):
                desc_found = True
                break
        
        if not desc_found:
            recommendations.append('Add more detailed descriptions of what each project does')
        
        if avg_score < 50:
            recommendations.append('Enhance project descriptions with impact and outcomes')
        
        if len(projects) < 2:
            recommendations.append('Add more projects to showcase diverse skills')
        
        return recommendations[:5]


def analyze_projects(resume_text):
    """Analyze projects in resume."""
    analyzer = ProjectAnalyzer(resume_text)
    return analyzer.analyze()
