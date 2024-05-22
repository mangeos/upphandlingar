from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager


def scraping(inp: str ) -> int:
        
    # # Specify the path to the Chrome browser executable
    # chrome_exe_path = "./chrome-win64/chrome-win64/chrome.exe"

    # # Create ChromeOptions instance
    # chrome_options = Options()

    # # Specify the path to the Chrome browser executable
    # chrome_options.binary_location = chrome_exe_path

    # # Create a browser instance (e.g., Chrome) and specify the Chrome executable path and options
    # ---------- loop här -----------------------
    # driver = webdriver.Chrome(options=chrome_options)
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Vissa system kräver detta argument
        chrome_options.add_argument("--no-sandbox")  # Nödvändigt för vissa system, som Docker

        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=chrome_options)

        # Go to the web page where the form is located
        driver.get('https://www.upphandlingar.nu')

        # Waiting for 3 sek  
        time.sleep(3)

        # Hitta input-elementet med hjälp av dess namn-attribut
        input_element = driver.find_element(By.NAME, 'sokruta')

        # Skriv text i input-elementet
        input_element.send_keys(inp)

        # Hitta knappen med hjälp av dess id-attribut
        button = driver.find_element(By.ID, 'sokrutan_button')

        # Klicka på knappen
        button.click()

        # Waiting for 3 sek  
        time.sleep(3)

        # Hela html sidan
        html_data = driver.page_source  

        # Skapa ett BeautifulSoup-objekt
        soup = BeautifulSoup(html_data, 'html.parser')

        # Hitta den översta div-en
        top_div = soup.find('div', class_='wpb_row wf-container sokrad')

        # Hitta nästa div-en efter den första
        next_div = top_div.find_next_sibling('div')

        # Totalt antal träffar 
        total = next_div.get_text(strip=True).split()[-2]
        
        # pprint total
        pprint(total)

        # Skriv ut antalet
        return total
    except Exception as e:
            pprint("Ett fel uppstod: ", e)
            return -1