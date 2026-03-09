# AI Job Finder Pro 🤖

A premium, AI-powered job discovery tool that matches your resume skills with real-time job listings across multiple global platforms.

## ✨ New in Version 2.0
- **Premium Dark-Mode UI**: A sleek, professional interface built with Streamlit.
- **Dynamic Skill Search**: Pick a skill from your resume to perform targeted global searches.
- **Improved Scraping Logic**: More robust handling of platform-specific search parameters.
- **Enhanced Relevance Scoring**: Visual indicators for how well a job matches your profile.

## 🚀 Quick Start

1. **Activate virtual environment:**
```bash
& "D:\DOUCUMENTS\.venv\Scripts\Activate.ps1"
```

2. **Navigate to project:**
```bash
cd "D:\DOUCUMENTS\AI - PROJECTS\ai-job-finder"
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
streamlit run app.py
```

## 📋 Features

### 🤖 **Intelligent Matching**
- **PDF Resume Parsing**: Automatically extracts technical skills and expertise.
- **Global Search**: Scrapes Internshala, Naukri, LinkedIn, and Indeed in real-time.
- **Selection Control**: Choose which skill to focus your search on for better results.

### 🎨 **Premium Experience**
- **Modern Aesthetics**: Radial gradients and glassmorphism-inspired components.
- **Interactive Stats**: Real-time metrics in the sidebar.
- **Responsive Cards**: Beautifully laid out job listings with skill badges and relevance scores.

## 🔧 Technical Details
- **Frontend**: Streamlit (Python-based Web Framework)
- **Scraping**: Requests & BeautifulSoup4
- **Parsing**: pdfminer.six
- **Automation Engine**: Selenium (Compatible with latest ChromeDriver)

## 📁 Project Structure
```
ai-job-finder/
├── app.py                    # Main Premium UI Application
├── job_scraper.py            # Dynamic multi-platform scraping engine
├── job_matcher.py            # Skill-based ranking logic
├── resume_parser.py          # PDF text & skill extraction
├── .gitignore                # Clean repository rules
├── requirements.txt          # Project dependencies
└── README.md                 # Documentation
```

## 🤝 Contributing
Feel free to fork and improve the matching algorithms or add more job platforms!

---
*Built with ❤️ by Mr. Vijay and Mr.Ganesh*
