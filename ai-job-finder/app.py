import streamlit as st
import os
from resume_parser import extract_skills
from job_scraper import get_jobs
from job_matcher import match_jobs
from job_applier import auto_apply_jobs, get_application_stats

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
if 'resume_path' not in st.session_state:
    st.session_state.resume_path = None
if 'apply_results' not in st.session_state:
    st.session_state.apply_results = []
if 'apply_done' not in st.session_state:
    st.session_state.apply_done = False

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main Background and Text */
    .stApp {
        background: radial-gradient(circle at top right, #0a192f, #020c1b);
        color: #ccd6f6;
        font-family: 'Inter', sans-serif;
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

    /* Apply result card */
    .result-card-success {
        background: linear-gradient(135deg, #0d2e1a, #1a4030);
        border: 1px solid #4ade80;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .result-card-failed {
        background: linear-gradient(135deg, #2e0d0d, #401a1a);
        border: 1px solid #f87171;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
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
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #45e0be !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(100,255,218,0.3) !important;
    }
    
    /* Metric boxes */
    [data-testid="metric-container"] {
        background-color: #1a2e4a;
        border: 1px solid #233554;
        border-radius: 10px;
        padding: 12px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #64ffda;
    }
    
    /* Divider */
    hr {
        border: 0.5px solid #233554;
    }

    /* Select box */
    .stSelectbox > div > div {
        background-color: #112240 !important;
        border-color: #233554 !important;
        color: #ccd6f6 !important;
    }
    
    /* Number input */
    .stNumberInput > div > div > input {
        background-color: #112240 !important;
        border-color: #233554 !important;
        color: #ccd6f6 !important;
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
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Jobs Found", len(st.session_state.matched_jobs))
        with col2:
            st.metric("Skills", len(st.session_state.detected_skills))
    else:
        st.info("Perform a search to see stats.")
    
    if st.session_state.apply_done:
        st.divider()
        st.markdown("### 🤖 Application Stats")
        stats = get_application_stats()
        st.metric("Total Applied", stats['total_applied'])
        if stats['by_source']:
            for source, count in stats['by_source'].items():
                st.write(f"• {source}: {count}")

    st.divider()
    st.caption("Crafted for Excellence by Mr. Vijay & Mr. Ganesh")

# --- MAIN CONTENT ---
st.title("🤖 AI Job Finder Pro")
st.markdown("#### *Precision matching for your career growth*")

st.divider()

# ==========================================
# STEP 1: Resume Upload
# ==========================================
col_up, col_info = st.columns([1, 1])

with col_up:
    st.subheader("📤 Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload PDF resume to extract skills", type=["pdf"], label_visibility="collapsed")

with col_info:
    if resume_file:
        resume_path = "resume.pdf"
        with open(resume_path, "wb") as f:
            f.write(resume_file.read())
        st.session_state.resume_path = resume_path
        
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

# ==========================================
# STEP 2: Intelligent Search
# ==========================================
if st.session_state.detected_skills:
    st.subheader("🔍 Step 2: Intelligent Search")
    
    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        search_query = st.selectbox(
            "Focus search on which skill?",
            options=st.session_state.detected_skills,
            index=0 if st.session_state.detected_skills else None
        )
    with col_btn:
        st.write("") # Padding to align button
        st.write("")
        if st.button("🚀 Execute Global Search"):
            st.session_state.search_performed = True
            st.session_state.apply_done = False
            st.session_state.apply_results = []
            with st.spinner(f"Scraping global platforms for '{search_query}'..."):
                all_jobs = get_jobs(search_query)
                matched = match_jobs(all_jobs, st.session_state.detected_skills)
                st.session_state.matched_jobs = matched

# ==========================================
# STEP 3: Results
# ==========================================
if st.session_state.search_performed:
    st.subheader(f"✅ Found {len(st.session_state.matched_jobs)} Relevant Openings")
    
    if st.session_state.matched_jobs:
        for job in st.session_state.matched_jobs:
            with st.container():
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

    st.divider()

    # ==========================================
    # STEP 3: AI Auto-Applier
    # ==========================================
    st.subheader("🤖 Step 3: AI Auto-Applier")
    st.markdown(
        "Automatically open and attempt to click the **Apply** button on matched job listings using a real Chrome browser session."
    )

    if not st.session_state.matched_jobs:
        st.warning("No matched jobs to apply to. Run a search first.")
    else:
        col_cfg1, col_cfg2, col_cfg3 = st.columns([2, 2, 2])
        with col_cfg1:
            max_apps = st.number_input(
                "Max Applications",
                min_value=1,
                max_value=min(20, len(st.session_state.matched_jobs)),
                value=min(3, len(st.session_state.matched_jobs)),
                step=1,
                help="Maximum number of job listings to attempt applying to."
            )
        with col_cfg2:
            headless_mode = st.checkbox(
                "Headless Mode",
                value=False,
                help="Run Chrome in the background (no visible browser window). Uncheck to see the browser open."
            )
        with col_cfg3:
            st.write("")
            st.write("")
            if st.button("🚀 Start Auto-Apply"):
                st.session_state.apply_results = []
                st.session_state.apply_done = False

                progress_bar = st.progress(0)
                status_text = st.empty()
                results_container = st.container()

                jobs_to_apply = st.session_state.matched_jobs[:max_apps]
                total = len(jobs_to_apply)

                def update_progress(idx, total, msg, job):
                    pct = int(idx / total * 100)
                    progress_bar.progress(pct)
                    status_text.info(f"**[{idx+1}/{total}]** Applying to: **{job['title']}** at **{job['company']}**...")

                results = auto_apply_jobs(
                    jobs_to_apply,
                    st.session_state.resume_path or "resume.pdf",
                    max_applications=max_apps,
                    headless=headless_mode,
                    progress_callback=update_progress
                )

                progress_bar.progress(100)
                status_text.success("Auto-Apply session complete!")
                st.session_state.apply_results = results
                st.session_state.apply_done = True
                st.rerun()

        # Display results from a previous apply run
        if st.session_state.apply_done and st.session_state.apply_results:
            success_count = sum(1 for r in st.session_state.apply_results if r['status'] == 'success')
            failed_count = len(st.session_state.apply_results) - success_count

            col_s, col_f = st.columns(2)
            with col_s:
                st.metric("✅ Applied", success_count)
            with col_f:
                st.metric("❌ Failed", failed_count)

            st.markdown("#### Application Log")
            for r in st.session_state.apply_results:
                job = r['job']
                if r['status'] == 'success':
                    st.markdown(f"""
                    <div class="result-card-success">
                        <strong style="color:#4ade80;">✅ APPLIED</strong> — <strong>{job['title']}</strong> @ {job['company']}<br>
                        <small style="color:#a7f3d0;">{r['message']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-card-failed">
                        <strong style="color:#f87171;">❌ FAILED</strong> — <strong>{job['title']}</strong> @ {job['company']}<br>
                        <small style="color:#fca5a5;">{r['message']}</small>
                    </div>
                    """, unsafe_allow_html=True)

else:
    if not resume_file:
        st.markdown("""
        <div style="text-align: center; padding: 60px; background: linear-gradient(135deg, #112240, #0d1b33); border-radius: 16px; border: 1px dashed #233554;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
            <h2 style="color: #64ffda; margin-bottom: 12px;">Your AI Career Assistant is Ready</h2>
            <p style="color: #8892b0; font-size: 1.1rem; max-width: 480px; margin: 0 auto;">
                Upload your resume above to begin the intelligent matching process. Our AI will scan your skills and find the best matching opportunities across LinkedIn, Internshala, Naukri, Shine, and more.
            </p>
        </div>
        """, unsafe_allow_html=True)