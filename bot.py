import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_bot():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # GitHub Actions sudah punya Chrome, kita tinggal panggil
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Mengakses link referral...")
        driver.get("https://www.febspot.com/ref/440627/")
        time.sleep(10)
        print(f"Berhasil mengakses. Judul: {driver.title}")
        
        # Tambahkan logika pendaftaran di sini
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
