from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

application_history = []

def apply_to_job(job, resume_path):
    """Open job page and try to click apply button"""

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(job["url"])

        time.sleep(5)

        apply_button = driver.find_element(By.XPATH, "//button[contains(text(),'Apply')]")
        apply_button.click()

        time.sleep(3)

        driver.quit()

        return True, "Opened job and clicked Apply"

    except Exception as e:
        return False, f"Apply failed: {str(e)}"


def auto_apply_jobs(jobs, resume_path, max_applications=5, progress_callback=None):

    results = []
    total = min(len(jobs), max_applications)

    for idx, job in enumerate(jobs[:max_applications]):

        if progress_callback:
            progress_callback(idx, total, "Applying to job", job)

        success, message = apply_to_job(job, resume_path)

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
        "by_source": {}
    }