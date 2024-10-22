import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

results = []

try:
    driver.get("https://arquisp.org.br/buscar-paroquias?field_lugar_paroquia_target_id=All&combine=&field_lugar_endereco_thoroughfare=&field_lugar_endereco_dependent_locality=")

    consent_button = driver.find_element(By.CSS_SELECTOR, "body > div.fundasp-lgpd-alert-wrapper > div > div:nth-child(2) > button")
    consent_button.click()

    count = 0 

    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > div.view-grouping")
        
        for item in elements:
            data = {}
            try:
                data['Parish_Name'] = item.find_element(By.CSS_SELECTOR, "div[class='view-grouping-header']").text
            except:
                pass
            try:
                data['Parish_Community'] = item.find_element(By.CSS_SELECTOR, "div[class='view-grouping-content'] > div > div[class='views-field views-field-title']").text
            except:
                pass
            try:
                data['Address'] = item.find_element(By.CSS_SELECTOR, "div[class='view-grouping-content'] > div > div[class='views-field views-field-field-lugar-endereco-premise']").text
            except:
                pass
            try:
                data['Phone'] = item.find_element(By.CSS_SELECTOR, "div[class='view-grouping-content'] > div > div[class='views-field views-field-field-lugar-telefone']").text
            except:
                data['Phone'] = None
            
            results.append(data)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#block-system-main > div > div > div.item-list > ul > li.pager-next"))
            )
            next_button.click()
            time.sleep(2) 
            count += 1 

            print(f"Page... {count}")

        except:
            print("No more pages to navigate.")
            break

finally:
    print(f"Total {count} pages processed.")
    with open('parishs.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
    time.sleep(5)
    driver.quit()