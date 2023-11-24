import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from colorama import Fore, Style
from tqdm import tqdm

def get_random_user_agent(browser, platform):
    with open('useragent.json', 'r') as file:
        user_agents = json.load(file)
    return user_agents.get(browser, {}).get(platform, "")

def colored_print(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

def search_and_click(keyword, site, max_iterations=3):
    for iteration in range(max_iterations):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        browser = random.choice(["chrome", "edge", "firefox"])
        platform = random.choice(["windows", "macos", "android", "ios"])
        
        user_agent = get_random_user_agent(browser, platform)
        chrome_options.add_argument(f"user-agent={user_agent}")
        
        driver = webdriver.Chrome(options=chrome_options)

        try:
            colored_print(f"\nMembuka halaman Google dengan User-Agent: {user_agent}...", Fore.GREEN)
            driver.get("https://www.google.com")

            colored_print(f"Melakukan pencarian dengan kata kunci '{keyword}' dan situs '{site}'...", Fore.CYAN)
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(f"{keyword} site:{site}")
            search_box.send_keys(Keys.RETURN)

            delay = random.uniform(5, 13)
            with tqdm(total=int(delay), desc="Menunggu hasil pencarian", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} detik") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

            colored_print("Mencari tautan yang mengandung teks atau link https://bikintas.online/...", Fore.MAGENTA)

            # Tunggu hingga elemen menjadi klikable
            wait = WebDriverWait(driver, 10)
            link_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://bikintas.online/')]")))

            colored_print("Klik tautan yang sesuai...", Fore.BLUE)
            
            # Gunakan JavaScript untuk memicu klik pada elemen
            driver.execute_script("arguments[0].click();", link_to_click)

            delay = random.uniform(10, 33)
            with tqdm(total=int(delay), desc="Menunggu halaman dibuka", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} detik") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

            colored_print("Halaman berhasil dibuka!", Fore.GREEN)

        except KeyboardInterrupt:
            colored_print("Dihentikan oleh pengguna.", Fore.RED)

        finally:
            colored_print("Menutup browser...", Fore.CYAN)
            driver.quit()

if __name__ == "__main__":
    # Jalankan fungsi dengan kata kunci "konveksi tas" dan situs "https://bikintas.online" maksimal 10 iterasi
    search_and_click("konveksi tas", "https://bikintas.online", max_iterations=3)
