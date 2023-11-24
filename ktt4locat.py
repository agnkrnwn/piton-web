import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from colorama import Fore, Style, Back
from tqdm import tqdm

def get_random_user_agent():
    with open('user_agent.json', 'r') as file:
        user_agents_data = json.load(file)

    # Extract the 'ua' (user agent) field from the JSON
    user_agents = [entry['ua'] for entry in user_agents_data]

    # Choose a random user agent from the list
    return random.choice(user_agents)

def colored_print(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

def set_random_location(driver):
    # Generate random latitude and longitude for a location in Indonesia
    # You can customize this logic based on your requirements
    latitude = random.uniform(-11.0, 6.0)
    longitude = random.uniform(94.0, 141.0)

    # Print the generated location
    colored_print(f"Setting random location: Latitude {latitude}, Longitude {longitude}", Fore.MAGENTA)

    # Use Chrome DevTools Protocol to set the geolocation
    location_script = f"navigator.geolocation.getCurrentPosition = function(callback) {{ callback({{'coords': {{'latitude': {latitude}, 'longitude': {longitude}}}}}); }};"
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": location_script})


def search_and_scroll_randomly(keyword, site, max_iterations=3):
    for iteration in range(max_iterations):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Make the browser headless

        user_agent = get_random_user_agent()
        chrome_options.add_argument(f"user-agent={user_agent}")

        # Enable Chrome DevTools Protocol
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=chrome_options)

        try:
            colored_print(f"\nIteration {iteration + 1}: Opening Google page with User-Agent: {user_agent}...", Fore.GREEN)
            
            # Set a random geolocation
            set_random_location(driver)

            driver.get("https://www.google.com")

            colored_print(f"Performing search with keyword '{keyword}' and site '{site}'...", Fore.CYAN)
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(f"{keyword} site:{site}")
            search_box.send_keys(Keys.RETURN)

            delay = random.uniform(5, 13)
            with tqdm(total=int(delay), desc="Waiting for search results", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} seconds") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

            colored_print(f"Searching for links containing text or link 'https://bikintas.online/' on iteration {iteration + 1}...", Fore.MAGENTA)

            # Wait until the element becomes clickable
            wait = WebDriverWait(driver, 10)
            link_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://bikintas.online/')]")))

            # Add a print statement when the link is found
            colored_print("Link found!:", Fore.YELLOW)
            print(link_to_click.get_attribute("href"))

            colored_print("Clicking the corresponding link...", Fore.BLUE)

            # Use JavaScript to trigger a click on the element
            driver.execute_script("arguments[0].click();", link_to_click)

            delay = random.uniform(3, 10)
            with tqdm(total=int(delay), desc="Waiting for the page to open", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} seconds") as pbar:
                while delay > 0:
                    time.sleep(1)
                    delay -= 1
                    pbar.update(1)

            colored_print("Page successfully opened! Scrolling...", Fore.GREEN)

            # Random scroll on the opened page for a duration between 15 and 30 seconds
            scroll_duration = random.uniform(15, 30)
            start_time = time.time()
            progress_bar = tqdm(total=100, desc="Scrolling Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
            while time.time() - start_time < scroll_duration:
                scroll_distance = random.randint(500, 1000)
                driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                time.sleep(1)

                # Update the progress bar based on the percentage of time spent scrolling
                elapsed_time = time.time() - start_time
                progress_percentage = min((elapsed_time / scroll_duration) * 100, 100)
                progress_bar.n = progress_percentage
                progress_bar.refresh()

            progress_bar.close()

            colored_print(f"Total time spent on the website: {round(time.time() - start_time, 2)} seconds", Fore.CYAN)

        except KeyboardInterrupt:
            colored_print("Stopped by the user.", Fore.RED)

        finally:
            colored_print("Closing the browser...", Back.RED)
            driver.quit()

if __name__ == "__main__":
    # Run the function with the keyword "konveksi tas" and site "https://bikintas.online" for a maximum of 3 iterations
    search_and_scroll_randomly("konveksi tas", "https://bikintas.online", max_iterations=2)
