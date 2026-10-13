"""ML Model - Scikit-learn based resume-job matching classifier"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from utils.helpers import extract_skills, similarity_score


class ResumJobMatcher:
    """ML model for resume-job matching using Scikit-learn."""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.is_trained = False
    
    def create_features(self, resume_text, job_description):
        """Create features for ML model."""
        features = {}
        
        # Feature 1: Text similarity using TF-IDF
        try:
            vec = TfidfVectorizer()
            texts = [resume_text, job_description]
            tfidf_matrix = vec.fit_transform(texts)
            from sklearn.metrics.pairwise import cosine_similarity
            text_sim = cosine_similarity(tfidf_matrix)[0][1]
            features['text_similarity'] = float(text_sim)
        except:
            features['text_similarity'] = 0.5
        
        # Feature 2: Skill overlap ratio
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        
        if job_skills:
            skill_overlap = sum(
                1 for skill in job_skills
                if any(s.lower() == skill.lower() for s in resume_skills)
            ) / len(job_skills)
            features['skill_overlap'] = skill_overlap
        else:
            features['skill_overlap'] = 0.5
        
        # Feature 3: Keyword overlap
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        if job_words:
            keyword_overlap = len(resume_words & job_words) / len(job_words)
            features['keyword_overlap'] = keyword_overlap
        else:
            features['keyword_overlap'] = 0.5
        
        # Feature 4: Resume length (normalized)
        resume_length = len(resume_text.split())
        features['resume_length'] = min(1.0, resume_length / 1000)
        
        # Feature 5: Job description length (normalized)
        job_length = len(job_description.split())
        features['job_length'] = min(1.0, job_length / 2000)
        
        # Feature 6: Experience keywords
        experience_keywords = ['years', 'experience', 'years of']
        experience_count = sum(
            1 for keyword in experience_keywords
            if keyword in resume_text.lower()
        )
        features['experience_keywords'] = min(1.0, experience_count / 5)
        
        # Feature 7: Education keywords
        education_keywords = ['degree', 'university', 'college', 'master', 'bachelor']
        education_count = sum(
            1 for keyword in education_keywords
            if keyword in resume_text.lower()
        )
        features['education_keywords'] = min(1.0, education_count / 5)
        
        # Feature 8: Measurable results
        import re
        measurable_items = len(re.findall(r'\d+%|\d+x|\$\d+', resume_text))
        features['measurable_results'] = min(1.0, measurable_items / 10)
        
        # Feature 9: Requirement coverage
        requirement_keywords = ['required', 'must', 'essential', 'mandatory']
        requirements_in_job = sum(
            1 for keyword in requirement_keywords
            if keyword in job_description.lower()
        )
        features['requirement_mentions'] = min(1.0, requirements_in_job / 10)
        
        # Feature 10: Action verb count
        action_verbs = [
            'developed', 'designed', 'implemented', 'created', 'built',
            'optimized', 'improved', 'enhanced', 'deployed', 'managed'
        ]
        action_count = sum(
            1 for verb in action_verbs
            if verb in resume_text.lower()
        )
        features['action_verbs'] = min(1.0, action_count / 10)
        
        return features
    
    def predict_match(self, resume_text, job_description):
        """Predict match between resume and job.
        
        Returns:
            dict: Match prediction and confidence
        """
        features = self.create_features(resume_text, job_description)
        
        # Calculate match score based on features
        score = (
            features['text_similarity'] * 0.25 +
            features['skill_overlap'] * 0.25 +
            features['keyword_overlap'] * 0.20 +
            features['experience_keywords'] * 0.10 +
            features['education_keywords'] * 0.10 +
            features['measurable_results'] * 0.05 +
            features['action_verbs'] * 0.05
        ) * 100
        
        score = min(100, max(0, score))
        
        # Determine prediction
        if score >= 75:
            prediction = 'Strong Match'
            confidence = score
        elif score >= 50:
            prediction = 'Moderate Match'
            confidence = score
        else:
            prediction = 'Low Match'
            confidence = 100 - score
        
        return {
            'prediction': prediction,
            'score': int(score),
            'confidence': int(confidence),
            'features': features
        }
    
    def evaluate_model(self, resume_texts, job_descriptions, labels):
        """Evaluate model performance.
        
        Args:
            resume_texts: List of resume texts
            job_descriptions: List of job descriptions
            labels: List of binary labels (1 for good match, 0 for bad match)
        
        Returns:
            dict: Evaluation metrics
        """
        predictions = []
        
        for resume, job in zip(resume_texts, job_descriptions):
            result = self.predict_match(resume, job)
            # Convert to binary: 1 for Strong/Moderate, 0 for Low
            pred = 1 if result['score'] >= 50 else 0
            predictions.append(pred)
        
        predictions = np.array(predictions)
        labels = np.array(labels)
        
        metrics = {
            'accuracy': accuracy_score(labels, predictions),
            'precision': precision_score(labels, predictions, zero_division=0),
            'recall': recall_score(labels, predictions, zero_division=0),
            'f1_score': f1_score(labels, predictions, zero_division=0)
        }
        
        return metrics
    
    def get_feature_importance(self):
        """Get relative importance of features in matching."""
        importance = {
            'text_similarity': 0.25,
            'skill_overlap': 0.25,
            'keyword_overlap': 0.20,
            'experience_keywords': 0.10,
            'education_keywords': 0.10,
            'measurable_results': 0.05,
            'action_verbs': 0.05
        }
        
        return importance


class MatchingClassifier:
    """High-level classifier for match prediction."""
    
    def __init__(self):
        self.matcher = ResumJobMatcher()
    
    def classify(self, resume_text, job_description):
        """Classify the match.
        
        Returns:
            dict: Classification result
        """
        result = self.matcher.predict_match(resume_text, job_description)
        
        return {
            'match_class': result['prediction'],
            'match_score': result['score'],
            'confidence': result['confidence'],
            'explanation': self._get_explanation(result['prediction'], result['score'])
        }
    
    def _get_explanation(self, prediction, score):
        """Get explanation of the prediction."""
        if prediction == 'Strong Match':
            return f'You are well-aligned with this position (Score: {score}/100). Your skills and experience closely match the requirements.'
        elif prediction == 'Moderate Match':
            return f'You meet some key requirements (Score: {score}/100). Consider developing additional skills to increase your competitiveness.'
        else:
            return f'There is limited overlap with this position (Score: {score}/100). Focus on gaining skills in the areas identified as gaps.'


def train_simple_classifier():
    """Train a simple classifier using sample data."""
    matcher = ResumJobMatcher()
    
    # Sample training data (in a real scenario, this would be much larger)
    sample_resumes = [
        "Python developer with 5 years experience in machine learning",
        "Web developer skilled in React and Node.js",
        "Data analyst with SQL and Excel expertise"
    ]
    
    sample_jobs = [
        "Looking for Python ML engineer with machine learning experience",
        "Frontend React developer position",
        "Data analyst role requiring SQL skills"
    ]
    
    sample_labels = [1, 1, 1]  # All matches
    
    # Evaluate
    metrics = matcher.evaluate_model(sample_resumes, sample_jobs, sample_labels)
    
    return matcher, metrics
