import re
from pdfminer.high_level import extract_text

# Skills database with variations
skills_db = {
    "python": ["python", "py", "python programming", "python developer"],
    "sql": ["sql", "mysql", "postgresql", "database", "sql server", "oracle"],
    "machine learning": ["machine learning", "ml", "deep learning", "neural network", "ai", "artificial intelligence", "nlp", "natural language processing"],
    "data analysis": ["data analysis", "analytics", "tableau", "power bi", "data visualization", "statistical analysis", "pandas", "numpy"]
}

def extract_skills(resume):
    """
    Extract skills from resume PDF using simple text matching
    """
    try:
        text = extract_text(resume).lower()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return []

    found_skills = []

    # Check for each skill and its variations
    for skill, variations in skills_db.items():
        for variation in variations:
            if variation.lower() in text:
                found_skills.append(skill)
                break

    return list(set(found_skills))