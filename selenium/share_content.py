from selenium import webdriver
import json
from time import sleep


def get_data(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(2)
    # 等待刷新
    sleep(7)
    print(driver.page_source)
    # div_list = driver.find_elements_by_xpath('//div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like "]')
    # for div in div_list:
    #     # 发布时间
    #     put_time = div.find_element_by_xpath('.//div[@class="WB_detail"]/div[2]/a[1]').text
    #     # 内容
    #     content = div.find_element_by_xpath('.//div[@class="WB_detail"]/div[@class="WB_text W_f14"]').text
    #     # 转发量
    #     zf_num = div.find_element_by_xpath('.//div[@class="WB_handle"]/ul/li[2]').text
    #     # 评论量
    #     rp_num = div.find_element_by_xpath('.//div[@class="WB_handle"]/ul/li[3]').text
    #     # 点赞量
    #     dz_num = div.find_element_by_xpath('.//div[@class="WB_handle"]/ul/li[4]//em[2]').text
    #     print(put_time)
    #     print(content)
    #     print(zf_num)
    #     print(rp_num)
    #     print(dz_num)


def main():
    driver = webdriver.Chrome()
    with open('cookie.json', 'r') as f:
        cookie_list = json.loads(f.read())
        # driver.add_cookie(cookie_list)
    for cookie in cookie_list:
        driver.add_cookie(cookie)
        break
    driver.get('https://weibo.com/p/1003061826792401?is_all=1')
    sleep(1)
    driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
    driver.get('https://weibo.com/p/1003061826792401?is_all=1')
    sleep(10)
    for i in range(3):
        get_data(driver)
        next_page = driver.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]')
        next_page.click()
        print('**' * 20)
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@title="搜索"]')))
    # print('*****')
    # driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # sleep(2)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # sleep(2)
    # # 等待刷新
    # sleep(7)
    # print(driver.page_source)
    # div_list = driver.find_elements_by_xpath('//div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like "]')
    # next_page = driver.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]')
    # for div in div_list:
    #     # 发布时间
    #     put_time = div.find_element_by_xpath('.//div[@class="WB_detail"]/div[2]/a[1]').text
    #     # 内容
    #     content = div.find_element_by_xpath('.//div[@class="WB_detail"]/div[@class="WB_text W_f14"]').text
    #     # 转发量
    #     zf_num = div.find_element_by_xpath('.//div[@class="WB_handle"]/ul/li[2]').text
    #     # 评论量
    #     rp_num = div.find_element_by_xpath('.//div[@class="WB_handle"]/ul/li[3]').text
    #     # 点赞量
    #     dz_num = div.find_element_by_xpath('.//div[@class="WB_handle"]/ul/li[4]//em[2]').text
    #     print(put_time)
    #     print(content)
    #     print(zf_num)
    #     print(rp_num)
    #     print(dz_num)
    sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()