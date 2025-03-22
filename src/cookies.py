import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from Threads.src.account import username, password

service = Service(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=service, options=chrome_options)


url = "https://www.threads.net/"


driver.get(url)
sleep(3)

try:

    login_button = driver.find_element(By.CSS_SELECTOR, ".x6ikm8r.x10wlt62.xlyipyv").click()
    sleep(5)


    username_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Username, phone or email']")

    password_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")


    username_field.click()
    sleep(1)


    username_field.send_keys(f"{username}")


    sleep(1)


    password_field.send_keys(f"{password}")


    login_submit_button = driver.find_element(By.CSS_SELECTOR, ".xwhw2v2.x1xdureb")
    login_submit_button.click()

    sleep(5)


    cookies = driver.get_cookies()

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

    print("Đã lưu cookies vào file cookies.json.")

except Exception as e:
    print("Error:", e)

finally:

    driver.quit()
