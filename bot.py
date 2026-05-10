import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Memastikan log langsung muncul (No Buffering)
def print_log(text):
    print(f"[*] {text}", flush=True)

def run_bot():
    print_log("Memulai konfigurasi Chrome...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # User-Agent agar tidak terdeteksi sebagai server
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        target_url = "https://www.febspot.com/ref/440627/"
        print_log(f"Mengakses target: {target_url}")
        
        driver.get(target_url)
        
        # Beri waktu loading yang cukup
        time.sleep(15)
        
        print_log(f"Berhasil dimuat! Judul halaman: {driver.title}")
        
        # Jika Anda ingin mengambil screenshot untuk bukti di log (base64)
        # driver.save_screenshot("debug.png")
        
    except Exception as e:
        print_log(f"ERROR: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print_log("Browser ditutup.")

if __name__ == "__main__":
    run_bot()
