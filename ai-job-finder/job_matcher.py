def match_jobs(jobs, skills):
    """
    Match jobs based on extracted skills from resume.
    Returns jobs ranked by skill relevance.
    """
    
    if not skills:
        return []
    
    # Define skill categories and related keywords
    skill_keywords = {
        "python": ["python", "django", "flask", "pandas", "numpy", "scipy"],
        "sql": ["sql", "database", "mysql", "postgresql", "nosql"],
        "machine learning": ["machine learning", "ml", "deep learning", "neural network", "ai", "artificial intelligence", "nlp"],
        "data analysis": ["data analysis", "analytics", "tableau", "power bi", "data visualization", "statistical"]
    }
    
    matched_jobs = []
    
    for job in jobs:
        title_lower = job["title"].lower()
        company_lower = job["company"].lower()
        
        skill_matches = []
        
        # Check for each skill and related keywords
        for skill in skills:
            keywords = skill_keywords.get(skill.lower(), [skill.lower()])
            
            for keyword in keywords:
                if keyword in title_lower or keyword in company_lower:
                    skill_matches.append(skill)
                    break
        
        # Only include jobs with at least one skill match
        if skill_matches:
            job_with_score = job.copy()
            job_with_score["matched_skills"] = skill_matches
            job_with_score["relevance_score"] = len(skill_matches)
            matched_jobs.append(job_with_score)
    
    # Sort by relevance score (descending)
    matched_jobs.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return matched_jobs