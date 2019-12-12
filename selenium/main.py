from selenium import webdriver
from Tools.tools import user_agent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import json

opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
opt.add_experimental_option("prefs", prefs)
opt.add_argument('--disable-gpu')
# 设置为无头
# opt.add_argument('--headless')
opt.add_argument(f'user-agent={user_agent}')
# opt.add_argument(f"--proxy-server={ip_c}")
driver = webdriver.Chrome(chrome_options=opt)
driver.get('https://weibo.com/')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginname")))
driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
username = driver.find_element_by_id('loginname')
password = driver.find_element_by_xpath('//input[@type="password"]')
submit = driver.find_element_by_xpath('//a[@node-type="submitBtn"]')
username.send_keys('15896963082')
sleep(1)
password.send_keys('fl626630250')
sleep(1)
submit.click()

sleep(6)
cookie = driver.get_cookies()
cookie_json = json.dumps(cookie)
with open('cookie.json', 'w') as f:
    f.write(cookie_json)
sleep(2)
driver.quit()
