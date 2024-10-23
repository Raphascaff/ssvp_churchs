from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from Miscellaneous.utils import decode_unicode_escapes, extract_lat_long
import time
import json
import logging


search_text = input('Insira a busca: ').strip()


if search_text:
    chrome_options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(
        service=service, 
        options=chrome_options
    )

    try:
        logging.basicConfig(level=logging.DEBUG)
        search_text = search_text.replace(' ', '+')
        url = f'https://www.google.com.br/maps/search/{search_text}'
        driver.get(url)

        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ""))).click()
        except Exception:
            pass

        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

        driver.execute_script("""
            var scrollableDiv = arguments[0];
            function scrollWithinElement(scrollableDiv) {
                return new Promise((resolve, reject) => {
                    var totalHeight = 0;
                    var distance = 1000;
                    var scrollDelay = 3000;

                    var timer = setInterval(() => {
                        var scrollHeightBefore = scrollableDiv.scrollHeight;
                        scrollableDiv.scrollBy(0, distance);
                        totalHeight += distance;
                    
                        if (totalHeight >= scrollHeightBefore) {
                            totalHeight = 0;
                            setTimeout(() => {
                                var scrollHeightAfter = scrollableDiv.scrollHeight;
                                if (scrollHeightAfter > scrollHeightBefore) {
                                    // Keep scrolling
                                    return;
                                } else {
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, scrollDelay);
                        }
                    }, 200);
                });
            }

            return scrollWithinElement(scrollableDiv);
        """, scrollable_div)

        items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

        results = []

        for item in items:
            data = {}

            try:
                raw_title = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
                data['TITLE'] = decode_unicode_escapes(raw_title)
            except Exception:
                pass

            try:
                data['LINK'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                data['LATITUDE'], data['LONGITUDE'] =  extract_lat_long(data['LINK'])
            except Exception:
                pass

            try:
                data['WEBSITE'] = item.find_element(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] > div > a').get_attribute('href')
            except Exception:
                pass

            if data.get('TITLE'):
                results.append(data)

            with open('results.json', 'w', encoding='utf-8') as json_file:
                json.dump(results, json_file, ensure_ascii=False, indent=4)
    finally:
        time.sleep(60)
        driver.quit()
else:
    print("Nenhuma entrada foi fornecida.")
