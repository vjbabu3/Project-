from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

application_history = []

def get_chromedriver_path():
    """Retrieve chrome driver path and resolve Windows shortcut/license file bug"""
    path = ChromeDriverManager().install()
    if os.name == 'nt':
        if not path.lower().endswith('.exe'):
            parent_dir = os.path.dirname(path)
            exe_path = os.path.join(parent_dir, "chromedriver.exe")
            if os.path.exists(exe_path):
                return exe_path
    return path

def apply_to_job(job, resume_path, headless=False):
    """Open job page and try to click apply button"""

    try:
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(service=Service(get_chromedriver_path()), options=chrome_options)
        driver.get(job["url"])

        time.sleep(5)

        apply_button = driver.find_element(By.XPATH, "//button[contains(text(),'Apply')]")
        apply_button.click()

        time.sleep(3)

        driver.quit()

        return True, "Opened job and clicked Apply"

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return False, f"Apply failed: {str(e)}"


def auto_apply_jobs(jobs, resume_path, max_applications=5, headless=False, progress_callback=None):

    results = []
    total = min(len(jobs), max_applications)

    for idx, job in enumerate(jobs[:max_applications]):

        if progress_callback:
            progress_callback(idx, total, "Applying to job", job)

        success, message = apply_to_job(job, resume_path, headless=headless)

        status = "success" if success else "failed"

        results.append({
            "job": job,
            "status": status,
            "message": message
        })

        if success:
            application_history.append(job)

        time.sleep(2)

    return results


def get_application_stats():

    return {
        "total_applied": len(application_history),
        "last_applied": "Recently" if application_history else None,
        "by_source": {
            s: len([j for j in application_history if j.get('source') == s])
            for s in set(j.get('source', 'Unknown') for j in application_history)
        }
    }