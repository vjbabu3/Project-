from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

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

def test_chrome_driver():
    """Test ChromeDriver setup"""
    try:
        print("[INFO] Setting up ChromeDriver...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(get_chromedriver_path())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("[OK] ChromeDriver initialized successfully!")
        print("[INFO] Opening Google...")

        driver.get("https://google.com")
        print(f"[INFO] Page title: {driver.title}")

        input("Press Enter to close browser...")
        driver.quit()
        print("[OK] Test completed successfully!")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        print("[ERROR] ChromeDriver test failed. Please check your setup.")

if __name__ == "__main__":
    test_chrome_driver()