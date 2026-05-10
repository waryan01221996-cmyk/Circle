import time
import requests
import random
import string
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def print_log(text):
    print(f"[*] {text}", flush=True)

# --- FUNGSI EMAIL SEMENTARA (Mail.tm) ---
def get_temp_email():
    try:
        domain_res = requests.get("https://api.mail.tm/domains").json()
        domain = domain_res['hydra:member'][0]['domain']
        user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"{user}@{domain}"
        password = "SecurePass123!"
        
        res = requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password})
        if res.status_code == 201:
            return email, password
    except:
        pass
    return None, None

def check_verification(email, password):
    print_log("Memeriksa kotak masuk untuk link verifikasi...")
    try:
        token_res = requests.post("https://api.mail.tm/token", json={"address": email, "password": password})
        token = token_res.json()['token']
        headers = {"Authorization": f"Bearer {token}"}

        for _ in range(15): # Cek setiap 10 detik selama 150 detik
            time.sleep(10)
            msgs = requests.get("https://api.mail.tm/messages", headers=headers).json()['hydra:member']
            if msgs:
                msg_id = msgs[0]['id']
                detail = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers).json()
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', detail['text'])
                for link in links:
                    if "confirm" in link or "verify" in link or "febspot" in link:
                        return link
    except Exception as e:
        print_log(f"Gagal cek email: {e}")
    return None

# --- FUNGSI UTAMA BOT ---
def run_bot():
    email, pwd = get_temp_email()
    if not email:
        print_log("Gagal membuat email sementara.")
        return

    print_log(f"Menggunakan Email: {email}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Langsung panggil webdriver (GitHub sudah sedia chromedriver di PATH)
    driver = webdriver.Chrome(options=options)

    try:
        # 1. Buka Link Referral
        print_log("Membuka halaman Febspot...")
        driver.get("https://www.febspot.com/ref/440627/")
        time.sleep(10)

        # 2. Logika Pengisian Form (Contoh ID elemen umum)
        # Catatan: Jika Febspot menggunakan Captcha, bot ini akan tertahan di sini.
        try:
            # Contoh jika pendaftaran langsung ada di halaman tersebut
            # driver.find_element(By.NAME, "email").send_keys(email)
            # driver.find_element(By.NAME, "password").send_keys("Password123!")
            # driver.find_element(By.ID, "submit-btn").click()
            print_log("Formulir pendaftaran telah disimulasikan.")
        except:
            print_log("Elemen form tidak ditemukan (Mungkin terhalang Captcha/Popup).")

        # 3. Verifikasi
        verif_link = check_verification(email, pwd)
        if verif_link:
            print_log(f"Link ditemukan! Mengaktivasi: {verif_link}")
            driver.get(verif_link)
            time.sleep(5)
            print_log("Proses selesai.")
        else:
            print_log("Tidak ada email verifikasi yang masuk.")

    except Exception as e:
        print_log(f"Terjadi error: {e}")
    finally:
        driver.quit()
        print_log("Browser ditutup.")

if __name__ == "__main__":
    run_bot()
