#!/usr/bin/env python3
"""
Test script to verify all components of the AI Job Auto-Applier work correctly
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from resume_parser import extract_skills
        from job_scraper import get_jobs
        from job_matcher import match_jobs
        from job_applier import auto_apply_jobs, get_application_stats
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_resume_parsing():
    """Test resume parsing functionality"""
    try:
        from resume_parser import extract_skills

        # Check if resume.pdf exists
        if os.path.exists("resume.pdf"):
            skills = extract_skills("resume.pdf")
            print(f"✅ Resume parsing successful - found skills: {skills}")
            return True
        else:
            print("⚠️  Resume.pdf not found - skipping resume parsing test")
            return True
    except Exception as e:
        print(f"❌ Resume parsing error: {e}")
        return False

def test_job_scraping():
    """Test job scraping functionality"""
    try:
        from job_scraper import get_jobs
        print("🔎 Testing job scraping (this may take a few seconds)...")
        jobs = get_jobs()
        print(f"✅ Job scraping successful - found {len(jobs)} jobs")
        if jobs:
            print(f"   Sample job: {jobs[0]['title']} at {jobs[0]['company']} ({jobs[0]['source']})")
        return True
    except Exception as e:
        print(f"❌ Job scraping error: {e}")
        return False

def test_job_matching():
    """Test job matching functionality"""
    try:
        from job_matcher import match_jobs
        from job_scraper import get_jobs

        # Get some jobs
        jobs = get_jobs()
        if not jobs:
            print("⚠️  No jobs found - skipping matching test")
            return True

        # Test matching with sample skills
        test_skills = ["python", "sql"]
        matched = match_jobs(jobs, test_skills)

        print(f"✅ Job matching successful - matched {len(matched)} jobs with skills: {test_skills}")
        return True
    except Exception as e:
        print(f"❌ Job matching error: {e}")
        return False

def test_application_stats():
    """Test application statistics functionality"""
    try:
        from job_applier import get_application_stats

        stats = get_application_stats()
        print(f"✅ Application stats loaded - {stats['total_applied']} total applications")
        return True
    except Exception as e:
        print(f"❌ Application stats error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running AI Job Auto-Applier System Tests")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Resume Parsing", test_resume_parsing),
        ("Job Scraping", test_job_scraping),
        ("Job Matching", test_job_matching),
        ("Application Stats", test_application_stats),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        print("-" * 30)

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your AI Job Auto-Applier is ready to use.")
        print("\n🚀 To start the application:")
        print("   streamlit run app.py")
        print("\n🌐 Then open: http://localhost:8501")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)