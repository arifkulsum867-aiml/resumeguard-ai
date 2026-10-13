#!/usr/bin/env python
"""Test script to verify ResumeGuard AI application"""

import sys

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        import streamlit
        print("[OK] Streamlit imported")
    except ImportError as e:
        print(f"[ERROR] Streamlit error: {e}")
        return False
    
    try:
        import pandas
        print("[OK] Pandas imported")
    except ImportError as e:
        print(f"[ERROR] Pandas error: {e}")
        return False
    
    try:
        import numpy
        print("[OK] NumPy imported")
    except ImportError as e:
        print(f"[ERROR] NumPy error: {e}")
        return False
    
    try:
        import sklearn
        print("[OK] Scikit-learn imported")
    except ImportError as e:
        print(f"[ERROR] Scikit-learn error: {e}")
        return False
    
    try:
        import plotly
        print("[OK] Plotly imported")
    except ImportError as e:
        print(f"[ERROR] Plotly error: {e}")
        return False
    
    try:
        from modules.resume_processor import ResumeProcessor
        print("[OK] ResumeProcessor imported")
    except ImportError as e:
        print(f"[ERROR] ResumeProcessor error: {e}")
        return False
    
    try:
        from modules.quality_analyzer import QualityAnalyzer
        print("[OK] QualityAnalyzer imported")
    except ImportError as e:
        print(f"[ERROR] QualityAnalyzer error: {e}")
        return False
    
    try:
        from modules.ats_analyzer import ATSAnalyzer
        print("[OK] ATSAnalyzer imported")
    except ImportError as e:
        print(f"[ERROR] ATSAnalyzer error: {e}")
        return False
    
    try:
        from modules.truth_checker import TruthChecker
        print("[OK] TruthChecker imported")
    except ImportError as e:
        print(f"[ERROR] TruthChecker error: {e}")
        return False
    
    try:
        from modules.job_analyzer import JobAnalyzer
        print("[OK] JobAnalyzer imported")
    except ImportError as e:
        print(f"[ERROR] JobAnalyzer error: {e}")
        return False
    
    try:
        from modules.matching_engine import MatchingEngine
        print("[OK] MatchingEngine imported")
    except ImportError as e:
        print(f"[ERROR] MatchingEngine error: {e}")
        return False
    
    try:
        from modules.project_analyzer import ProjectAnalyzer
        print("[OK] ProjectAnalyzer imported")
    except ImportError as e:
        print(f"[ERROR] ProjectAnalyzer error: {e}")
        return False
    
    try:
        from modules.ml_model import MatchingClassifier
        print("[OK] ML Model imported")
    except ImportError as e:
        print(f"[ERROR] ML Model error: {e}")
        return False
    
    return True

def test_demo_data():
    """Test demo data loading"""
    print("\nTesting demo data...")
    try:
        from utils.demo_data import list_sample_resumes, list_sample_jobs
        resumes = list_sample_resumes()
        jobs = list_sample_jobs()
        print(f"[OK] Demo resumes: {len(resumes)} samples")
        print(f"[OK] Demo jobs: {len(jobs)} samples")
        return True
    except Exception as e:
        print(f"[ERROR] Demo data error: {e}")
        return False

def test_basic_analysis():
    """Test basic analysis functionality"""
    print("\nTesting basic analysis...")
    try:
        from modules.quality_analyzer import QualityAnalyzer
        
        test_resume = """
        John Doe
        Email: john@example.com
        
        SUMMARY
        Software developer with 5 years experience
        
        EDUCATION
        Bachelor of Science in Computer Science
        
        EXPERIENCE
        Senior Developer at Tech Company (2020-2023)
        Developed Python applications
        
        SKILLS
        Python, Java, SQL, React
        """
        
        analyzer = QualityAnalyzer(test_resume)
        results = analyzer.analyze()
        
        print(f"[OK] Quality score: {results['overall_score']}/100")
        print(f"[OK] Completeness: {results['completeness_score']}/100")
        print(f"[OK] Content: {results['content_score']}/100")
        print(f"[OK] Recommendations: {len(results['recommendations'])} items")
        return True
    except Exception as e:
        print(f"[ERROR] Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("ResumeGuard AI - Application Test")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_demo_data():
        all_passed = False
    
    if not test_basic_analysis():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nTo run the application:")
        print("  streamlit run app.py")
        return 0
    else:
        print("[FAILED] SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
