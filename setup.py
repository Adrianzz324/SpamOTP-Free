import os
import sys
import time
import subprocess
import threading
import importlib.util
import subprocess

# --- KONFIGURASI WARNA TERMINAL ---
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_CYAN = '\033[96m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'

# Daftar package pip yang akan diinstall
# Format: {'nama_di_pip': 'nama_module_saat_diimport'}
PACKAGES = {
    'beautifulsoup4': 'bs4',
    'requests': 'requests',
    'phonenumbers': 'phonenumbers',
    'selenium': 'selenium',
    'webdriver-manager': 'webdriver_manager' # Pengganti chromedriver manual
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_banner():
    clear_screen()
    banner = f"""
{C_CYAN}{C_BOLD}
╔══════════════════════════════════════════════════╗
║             AUTO INSTALLER SCRIPT                ║
║           Menyiapkan Lingkungan Kerja            ║
╚══════════════════════════════════════════════════╝
{C_RESET}"""
    print(banner)

def ask_permission():
    animate_text(f"{C_YELLOW}[!] Peringatan: Script ini akan mengecek dan menginstall package yang kurang.{C_RESET}")
    while True:
        choice = input(f"{C_BOLD}Apakah Anda ingin melanjutkan? (Y/N): {C_RESET}").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            animate_text(f"{C_RED}Proses dibatalkan oleh pengguna. Keluar...{C_RESET}")
            sys.exit()
        else:
            print(f"{C_RED}Pilihan tidak valid. Ketik Y atau N.{C_RESET}")

def is_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_package(package_name, result_container):
    """Fungsi yang berjalan di thread terpisah untuk menginstall package"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        result_container[0] = True
    except subprocess.CalledProcessError:
        result_container[0] = False

def animated_progress_bar(package_name):
    """Menampilkan progress bar saat instalasi berjalan"""
    bar_length = 30
    
    # Menjalankan instalasi di thread terpisah agar animasi tidak berhenti
    result_container = [None]
    install_thread = threading.Thread(target=install_package, args=(package_name, result_container))
    install_thread.start()

    progress = 0
    # Animasi berjalan selama instalasi belum selesai
    while install_thread.is_alive():
        # Simulasi progress naik perlahan sampai mentok di 95% sebelum instalasi beres
        if progress < 95:
            progress += 1
            time.sleep(0.1) # Kecepatan loading bohongan
        
        filled_length = int(bar_length * progress // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stdout.write(f'\r{C_CYAN}Menginstall {package_name:<18} untuk menyiapkan script... [{bar}] {progress}%{C_RESET}')
        sys.stdout.flush()
        time.sleep(0.05)

    # Pastikan thread selesai dan bar mencapai 100%
    install_thread.join()
    
    if result_container[0]:
        bar = '█' * bar_length
        sys.stdout.write(f'\r{C_GREEN}Menginstall {package_name:<18} untuk menyiapkan script... [{bar}] 100%{C_RESET}\n')
        sys.stdout.flush()
        return True
    else:
        sys.stdout.write(f'\r{C_RED}Gagal menginstall {package_name:<18} [{'-' * bar_length}] ERROR{C_RESET}\n')
        sys.stdout.flush()
        return False

def main():
    show_banner()
    ask_permission()
    
    print()
    animate_text(f"{C_BOLD}Memeriksa System Dependencies:{C_RESET}")
    print(f"[{C_GREEN}✓{C_RESET}] Python (Terdeteksi versi {sys.version.split()[0]})")
    print(f"[{C_GREEN}✓{C_RESET}] Pip    (Terdeteksi)")
    
    # Note untuk Python2/3
    print(f"{C_YELLOW}[i] Catatan: Python, Python2, dan Python3 adalah system environment.{C_RESET}")
    print(f"{C_YELLOW}    Script ini menggunakan env yang sedang aktif saat ini.{C_RESET}\n")
    
    time.sleep(1)
    animate_text(f"{C_BOLD}Memeriksa dan Menginstall Library (Pip):{C_RESET}")
    
    all_success = True
    for pip_name, module_name in PACKAGES.items():
        if is_installed(module_name):
            print(f"[{C_GREEN}✓{C_RESET}] {pip_name:<15} : Sudah Terinstall")
        else:
            success = animated_progress_bar(pip_name)
            if not success:
                all_success = False

    print("\n" + "="*50)
    if all_success:
        animate_text(f"{C_GREEN}{C_BOLD}[SELESAI] Semua package berhasil disiapkan!{C_RESET}")
        animate_text(f"{C_CYAN}Script utama Anda sekarang siap dijalankan.{C_RESET}")
    else:
        animate_text(f"{C_RED}{C_BOLD}[PERINGATAN] Ada beberapa package yang gagal diinstall.{C_RESET}")
        animate_text(f"{C_YELLOW}Coba jalankan dengan akses Administrator/Root atau cek koneksi internet Anda.{C_RESET}")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Menghindari error keyboard interrupt (Ctrl+C) yang kotor di terminal
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}Proses dihentikan paksa (Ctrl+C).{C_RESET}")
        sys.exit()
os.system("clear")
subprocess.run(["python","spamotp_store.py"])
