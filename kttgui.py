import json
import random
import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from colorama import Fore, Style
from tqdm import tqdm

def get_random_user_agent():
    with open('user_agent.json', 'r') as file:
        user_agents_data = json.load(file)

    user_agents = [entry['ua'] for entry in user_agents_data]
    return random.choice(user_agents)

def colored_print(message, color=Fore.WHITE):
    result_text.insert(tk.END, f"{color}{message}{Style.RESET_ALL}\n")
    result_text.see(tk.END)  # Scroll to the end

def search_and_click(keyword, site, max_iterations=3):
    for iteration in range(max_iterations):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        user_agent = get_random_user_agent()
        chrome_options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(options=chrome_options)

        try:
            colored_print(f"\nIteration {iteration + 1}: Opening Google page with User-Agent: {user_agent}...", Fore.GREEN)
            driver.get("https://www.google.com")

            colored_print(f"Performing search with keyword '{keyword}' and site '{site}'...", Fore.CYAN)
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(f"{keyword} site:{site}")
            search_box.send_keys(Keys.RETURN)

            delay = random.uniform(5, 13)
            with tqdm(total=int(delay), desc="Waiting for search results",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} seconds") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

            colored_print(f"Searching for links containing text or link 'https://bikintas.online/' on iteration {iteration + 1}...", Fore.MAGENTA)

            wait = WebDriverWait(driver, 20)
            link_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://bikintas.online/')]")))

            colored_print("Link found!:", Fore.YELLOW)
            colored_print(link_to_click.get_attribute("href"), Fore.YELLOW)

            colored_print("Clicking the corresponding link...", Fore.BLUE)
            driver.execute_script("arguments[0].click();", link_to_click)

            delay = random.uniform(3, 10)
            with tqdm(total=int(delay), desc="Waiting for the page to open",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} seconds") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

            colored_print("Page successfully opened! Scrolling...", Fore.GREEN)

            scroll_distance = random.randint(500, 1000)
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

            delay = random.uniform(5, 15)
            with tqdm(total=int(delay), desc="Scrolling", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} seconds") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

        except KeyboardInterrupt:
            colored_print("Stopped by the user.", Fore.RED)

        finally:
            colored_print("Closing the browser...", Fore.RED)
            driver.quit()

# GUI setup
def run_search():
    result_text.delete(1.0, tk.END)  # Clear previous results
    keyword = keyword_entry.get()
    site = site_entry.get()
    max_iterations = int(iterations_entry.get())
    search_and_click(keyword, site, max_iterations)

# Create the main window
window = tk.Tk()
window.title("Web Automation GUI")

# Create and place widgets
keyword_label = tk.Label(window, text="Keyword:")
keyword_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
keyword_entry = tk.Entry(window)
keyword_entry.grid(row=0, column=1, padx=5, pady=5)

site_label = tk.Label(window, text="Site:")
site_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
site_entry = tk.Entry(window)
site_entry.grid(row=1, column=1, padx=5, pady=5)

iterations_label = tk.Label(window, text="Max Iterations:")
iterations_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
iterations_entry = tk.Entry(window)
iterations_entry.grid(row=2, column=1, padx=5, pady=5)

run_button = tk.Button(window, text="Run Search", command=run_search)
run_button.grid(row=3, column=0, columnspan=2, pady=10)

result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Start the GUI event loop
window.mainloop()
