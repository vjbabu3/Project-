import streamlit as st
import os
from resume_parser import extract_skills
from job_scraper import get_jobs
from job_matcher import match_jobs

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Job Finder | Premium Edition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE ---
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'matched_jobs' not in st.session_state:
    st.session_state.matched_jobs = []
if 'detected_skills' not in st.session_state:
    st.session_state.detected_skills = []

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Main Background and Text */
    .stApp {
        background: radial-gradient(circle at top right, #0a192f, #020c1b);
        color: #ccd6f6;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #64ffda !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #112240 !important;
        border-right: 1px solid #233554;
    }
    
    /* Card/Container Styling */
    .job-card {
        background-color: #112240;
        border: 1px solid #233554;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .job-card:hover {
        transform: translateY(-4px);
        border-color: #64ffda;
    }
    
    /* Skill Badge */
    .skill-badge {
        background-color: #1d3557;
        color: #64ffda;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        margin-right: 8px;
        display: inline-block;
        border: 1px solid #64ffda;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #64ffda !important;
        color: #0a192f !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        border: none !important;
    }
    
    /* Divider */
    hr {
        border: 0.5px solid #233554;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/200/robot-3.png", width=120)
    st.markdown("# System Config")
    st.write("Find your next role with AI-powered matching.")
    
    st.divider()
    st.markdown("### 📊 Search Stats")
    if st.session_state.search_performed:
        st.metric("Jobs Found", len(st.session_state.matched_jobs))
        st.metric("Skills Matched", len(st.session_state.detected_skills))
    else:
        st.info("Perform a search to see stats.")
    
    st.divider()
    st.caption("Crafted for Excellence by Mr. Vijay & Mr. Ganesh")

# --- MAIN CONTENT ---
st.title("🤖 AI Job Finder Pro")
st.markdown("#### *Precision matching for your career growth*")

st.divider()

# Resume Upload Section
col_up, col_info = st.columns([1, 1])

with col_up:
    st.subheader("📤 Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF resume to extract skills", type=["pdf"], label_visibility="collapsed")

with col_info:
    if resume_file:
        resume_path = "resume.pdf"
        with open(resume_path, "wb") as f:
            f.write(resume_file.read())
        
        with st.spinner("Analyzing resume..."):
            skills = extract_skills(resume_path)
            st.session_state.detected_skills = skills
            
        st.success("Resume Analyzed!")
        
        if skills:
            st.write("**Detected Skills:**")
            skill_html = "".join([f'<span class="skill-badge">{s}</span>' for s in skills])
            st.markdown(skill_html, unsafe_allow_html=True)
        else:
            st.warning("No specific skills detected. Ensure your resume has clear keywords.")
    else:
        st.info("Awaiting resume upload...")

st.divider()

# Search Section
if st.session_state.detected_skills:
    st.subheader("🔍 Step 2: Intelligent Search")
    
    # Allow user to pick primary skill for search query
    search_query = st.selectbox(
        "Focus search on which skill?",
        options=st.session_state.detected_skills,
        index=0 if st.session_state.detected_skills else None
    )
    
    if st.button("🚀 Execute Global Search"):
        st.session_state.search_performed = True
        with st.spinner(f"Scraping global platforms for '{search_query}'..."):
            all_jobs = get_jobs(search_query)
            matched = match_jobs(all_jobs, st.session_state.detected_skills)
            st.session_state.matched_jobs = matched
            
# Results Section
if st.session_state.search_performed:
    st.subheader(f"✅ Found {len(st.session_state.matched_jobs)} Relevant Openings")
    
    if st.session_state.matched_jobs:
        for job in st.session_state.matched_jobs:
            with st.container():
                # Custom HTML for Card
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin-top: 0;">{job['title']}</h3>
                            <h5 style="color: #8892b0;">🏬 {job['company']}</h5>
                            <p style="color: #64ffda; font-weight: bold; margin-bottom: 8px;">🔗 Source: {job.get('source', 'Web')}</p>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 1.2rem; font-weight: bold; color: #64ffda;">{job['relevance_score']}/{len(st.session_state.detected_skills)}</span><br>
                            <small style="color: #8892b0;">Relevance</small>
                        </div>
                    </div>
                    <div style="margin: 12px 0;">
                        {" ".join([f'<span class="skill-badge" style="background-color: #112240; border-color: #233554">{s}</span>' for s in job['matched_skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if job.get('url'):
                    st.link_button("View Position Details", job['url'])
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.error("No matches found. Try focusing on a different skill.")
else:
    if not resume_file:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background-color: #112240; border-radius: 12px; border: 1px dashed #233554;">
            <h2 style="color: #8892b0;">Your AI Career Assistant is Ready</h2>
            <p>Upload your resume to begin the intelligent matching process.</p>
        </div>
        """, unsafe_allow_html=True)
 