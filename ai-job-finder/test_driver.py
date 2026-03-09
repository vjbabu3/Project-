from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_chrome_driver():
    """Test ChromeDriver setup"""
    try:
        print("Setting up ChromeDriver...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("ChromeDriver initialized successfully!")
        print("Opening Google...")

        driver.get("https://google.com")
        print(f"Page title: {driver.title}")

        input("Press Enter to close browser...")
        driver.quit()
        print("Test completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        print("ChromeDriver test failed. Please check your setup.")

if __name__ == "__main__":
    test_chrome_driver()