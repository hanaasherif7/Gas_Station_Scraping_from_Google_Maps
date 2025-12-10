import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

search_name = "محطات بنزين القاهرة"
driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")
time.sleep(5)

search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(search_name)
search_box.send_keys(Keys.ENTER)
time.sleep(5)

station_name = []
station_website = []
station_rate = []
status = []
num_of_reviews = []
phone_number = []
location = []
station_link = []
links = set()

for _ in range(30):
    cards = driver.find_elements(By.CSS_SELECTOR,"div.Nv2PK.tH5CWc.THOPZb")
    for card in cards:
        try:
            lin = card.find_element(By.CSS_SELECTOR,"a.hfpxzc").get_attribute("href")
            if lin not in links:
                links.add(lin)
                station_link.append(lin)
            else:
                continue
        except:
            lin = "not found"
            station_link.append(lin)
        try:
            name = card.find_element(By.CSS_SELECTOR,"div.qBF1Pd.fontHeadlineSmall").text
        except:
            name = "not found"
        station_name.append(name)
        try:
            link = card.find_elements(By.CSS_SELECTOR, "a.lcr4fd.S9kvJb")
            href = link[0].get_attribute("href") if link else None
            website = href if href else "not found"
        except:
            website = "not found"
        station_website.append(website)
        try:
            rate = card.find_element(By.CSS_SELECTOR,"span.MW4etd").text
        except:
            rate = "not found"
        station_rate.append(rate)
        try:
            reviews = card.find_element(By.CSS_SELECTOR, "span.UY7F9").text
        except:
            reviews = "not found"
        num_of_reviews.append(reviews)
        try:
            phone = card.find_element(By.CSS_SELECTOR,"span.UsdlK").text
        except:
            phone = "not found"
        phone_number.append(phone)
        try:
            stat = card.find_element(By.CSS_SELECTOR, "div.W4Efsd span[style*='color']").text
        except:
            stat = "not found"
        status.append(stat)

        try:
            card.click()
            time.sleep(2)
            try:
                loc = driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']").text
            except:
                loc = "not found"
        except:
            loc = "not found"
        location.append(loc)

    driver.execute_script("document.querySelector('div[role=\"feed\"]').scrollBy(0, 1000);")
    time.sleep(5)

file_path = f"{search_name}.csv"

df = pd.DataFrame({
    "Station name": station_name,
    "Station Website": station_website,
    "Rate": station_rate,
    "Phone number": phone_number,
    "Number of Reviews": num_of_reviews,
    "Station link": station_link,
    "Status": status,
    "Location": location
})
if not os.path.exists(file_path):
    df.drop_duplicates(subset=["Station link"],keep="first")
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
else:
    df_old = pd.read_csv(file_path)
    df_new = df[~ df['Station link'].isin(df_old['Station link'])]
    if not df_new.empty:
        df_all=pd.concat([df_old,df_new],ignore_index=True)
        df_all.drop_duplicates(subset=["Station link"],keep="first")
        df_all.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8-sig')