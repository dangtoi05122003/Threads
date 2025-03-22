import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime, timedelta
import re


service = Service(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=service, options=chrome_options)


url = "https://www.threads.net/"


cookies_file = "cookies.json"
if os.path.exists(cookies_file):

    with open(cookies_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    
    driver.get(url)
    sleep(3)
    

    for cookie in cookies:
        driver.add_cookie(cookie)
    
    print("Success.")
    driver.refresh()
else:
    driver.get(url)
    print(f"Access: {url}")
    sleep(5)


path = 'log.json'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
else:
    data = []

last = driver.execute_script("return document.body.scrollHeight")
count = 0
posts_data = data

while count < 10:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    
    new = driver.execute_script("return document.body.scrollHeight")
    if new == last:
        break
    
    last = new
    count += 1

try:
    posts = driver.find_elements(By.CSS_SELECTOR, ".x1ypdohk.x1n2onr6.xvuun6i.x3qs2gp.x1w8tkb5.x8xoigl.xz9dl7a.x6bh95i.x13fuv20.xt8cgyo.xsag5q8")
    
    if posts:
        for i, post in enumerate(posts, 1):
            post_data = {}
            try:
                author = post.find_element(By.CSS_SELECTOR, ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xp07o12.xzmqwrg.x1citr7e.x1kdxza.xt0b8zv").text
            except Exception as e:
                author = "Error path author"
            post_data["author"] = author

            try:
                now = datetime.now()
                time_str = post.find_element(By.CSS_SELECTOR, ".html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs").text
                time = time_str  


                time_match = re.search(r"(\d+)(h|d|m)", time_str, re.IGNORECASE)

                if time_match:
                    value, unit = int(time_match.group(1)), time_match.group(2).lower()
                    if unit == "h": 
                        post_time = now - timedelta(hours=value)
                    elif unit == "d": 
                        post_time = now - timedelta(days=value)
                    elif unit == "m": 
                        post_time = now - timedelta(minutes=value)
                    time = post_time.strftime("%d/%m/%Y %H:%M")

            except Exception as e:
                print(f"Error: {e}")
                time = "Error path time"

            post_data["time"] = time

            try:
                content = post.find_element(By.CSS_SELECTOR, ".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xjohtrz.xo1l8bm.xp07o12.x1yc453h.xat24cr.xdj266r").text
            except Exception as e:
                content = "Error path content"
            post_data["content"] = content

            try:
                images = post.find_elements(By.CSS_SELECTOR, '.x87ps6o')
                image_urls = [img.get_attribute('src') for img in images if img.get_attribute('src') is not None]
                image_urls = [url for url in image_urls if url]
            except Exception as e:
                image_urls = []
            post_data["images"] = image_urls

            try:
                video = post.find_element(By.TAG_NAME, 'video')
                video_url = video.get_attribute('src')
            except Exception as e:
                video_url = None
            post_data["video"] = video_url

            posts_data.append(post_data)

            print(f"Bài viết {i}:")
            print(f"Tác giả: {author}")
            print(f"Thời gian: {time}")
            print(f"Nội dung: {content}")
            print(f"Ảnh: {image_urls if image_urls else 'Không có ảnh'}")
            print(f"Video: {video_url if video_url else 'Không có video'}")
            print("-" * 40)

    else:
        print("Error.")
    
except Exception as e:
    print("Error :", e)


with open(path, 'w', encoding='utf-8') as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=4)

print("Save.")
driver.quit()