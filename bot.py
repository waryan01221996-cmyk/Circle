import time
import requests
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def print_log(text):
    print(f"[*] {text}", flush=True)

# --- FUNGSI EMAIL SEMENTARA (Mail.tm) ---
def get_temp_email():
    # Mengambil domain yang tersedia
    domain = requests.get("https://api.mail.tm/domains").json()['hydra:member'][0]['domain']
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{username}@{domain}"
    password = "Password123!"
    
    # Membuat akun email
    data = {"address": email, "password": password}
    res = requests.post("https://api.mail.tm/accounts", json=data)
    if res.status_code == 201:
        return email, password, res.json()['id']
    return None, None, None

def get_verification_link(email, password):
    print_log("Menunggu email masuk...")
    # Login untuk mendapatkan token
    token_res = requests.post("https://api.mail.tm/token", json={"address": email, "password": password})
    token = token_res.json()['token']
    headers = {"Authorization": f"Bearer {token}"}

    # Cek inbox selama 2 menit
    for _ in range(12): 
        time.sleep(10)
        msgs = requests.get("https://api.mail.tm/messages", headers=headers).json()['hydra:member']
        if msgs:
            msg_id = msgs[0]['id']
            msg_content = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers).json()
            # Mencari link di dalam teks body email
            import re
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg_content['text'])
            return links[0] if links else None
    return None

# --- FUNGSI UTAMA BOT ---
def run_bot():
    email, pwd, account_id = get_temp_email()
    if not email:
        print_log("Gagal membuat email sementara.")
        return

    print_log(f"Email dibuat: {email}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. Buka Referral
        driver.get("https://www.febspot.com/ref/440627/")
        print_log("Membuka halaman referral...")
        
        # 2. Klik Sign Up (Sesuaikan Selector jika berubah)
        # Seringkali tombol signup ada di navbar atau modal
        time.sleep(5)
        
        # Contoh mengisi form pendaftaran
        # (Anda harus inspeksi ID/Name elemen di Febspot)
        # driver.find_element(By.NAME, "email").send_keys(email)
        # driver.find_element(By.NAME, "password").send_keys("UserPass123!")
        # driver.find_element(By.ID, "submit").click()
        
        print_log("Formulir dikirim (Simulasi).")
        
        # 3. Verifikasi Email
        verif_link = get_verification_link(email, pwd)
        if verif_link:
            print_log(f"Link verifikasi ditemukan: {verif_link}")
            driver.get(verif_link)
            time.sleep(5)
            print_log("Akun berhasil diverifikasi!")
        else:
            print_log("Link verifikasi tidak ditemukan.")

    except Exception as e:
        print_log(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
