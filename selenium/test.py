from selenium import webdriver
from time import sleep
# 比较长 导入动作链类
from selenium.webdriver.common.action_chains import ActionChains
#
# driver = webdriver.Chrome()
# driver.get("http://www.baidu.com")
# sleep(3)
# driver.find_element_by_xpath("//a[@name='tj_trnews']").click()
# sleep(2)
# driver.find_element_by_xpath("//a[@href='http://image.baidu.com/'][contains(.,'图片')]").click()
# sleep(2)
# driver.back()
# sleep(2)
# driver.back()
# sleep(2)
# driver.forward()
# sleep(2)
# driver.forward()
# sleep(2)
# driver.close()
# driver.get("http://sahitest.com/demo/clicks.htm")
# sleep(2)
#
# # 找到需要操作的元素
# dbclickElement = driver.find_element_by_xpath("//input[contains(@value,'dbl click me')]")
# leftclickElement = driver.find_element_by_xpath("//input[@value='click me']")
# rightclickElement = driver.find_element_by_xpath("//input[contains(@value,'right click me')]")
# clear = driver.find_element_by_xpath('//input[@name="t1"]')
# # 传入浏览器对象构造动作链
# actionChains = ActionChains(driver)
# # 左键双击一个元素
# actionChains.double_click(dbclickElement)
# # 执行 不要忘记
# actionChains.perform()
#
# sleep(2)
#
# actionChains = ActionChains(driver)
# # 左键单击一个元素
# actionChains.click(leftclickElement)
# actionChains.perform()
# sleep(2)
#
# actionChains = ActionChains(driver)
# # 右键单击一个元素
# actionChains.context_click(rightclickElement)
# actionChains.perform()
# sleep(2)
#
# actionChains.click(clear)
# actionChains.perform()
# sleep(2)
#
# # **********************************************
#
# driver.get("http://sahitest.com/demo/mouseover.htm")
# sleep(3)
#
# # 找到需要鼠标移动指向的元素
# hiElement = driver.find_element_by_xpath("//span[contains(.,'Hi Kamlesh')]")
# writeElement = driver.find_element_by_xpath("//input[@value='Write on hover']")
# blankElement = driver.find_element_by_xpath("//input[@value='Blank on hover']")
#
# # 直接移动到某一个元素
# ActionChains(driver).move_to_element(hiElement).perform()
# sleep(2)
#
# # 在当前位置移动x,y的偏移
# ActionChains(driver).move_by_offset(10, 25).perform()
# sleep(2)
#
# # 先移动到某一个元素 再做偏移 是上面两个api的封装
# ActionChains(driver).move_to_element_with_offset(writeElement, 5, 55).perform()
# sleep(5)
#
# driver.quit()
#
# # **********************************************
#
# driver.get("http://sahitest.com/demo/dragDropMooTools.htm")
# driver.maximize_window()
# sleep(5)
# driver.save_screenshot("./dragMe.png")
#
# # 找到相关需要拖拽的元素
# dragMe = driver.find_element_by_xpath("//div[@class='drag']")
# item1 = driver.find_element_by_xpath("//div[contains(.,'Item 1')]")
# item2 = driver.find_element_by_xpath("//div[contains(.,'Item 2')]")
# item3 = driver.find_element_by_xpath("//div[contains(.,'Item 3')]")
# item4 = driver.find_element_by_xpath("//div[contains(.,'Item 4')]")
#
# # drag_and_drop 拖某一个到某一个元素
# ActionChains(driver).drag_and_drop(dragMe, item1).perform()
# sleep(2)
# ActionChains(driver).drag_and_drop(dragMe, item2).perform()
# sleep(2)
# ActionChains(driver).drag_and_drop(dragMe, item3).perform()
# sleep(2)
# ActionChains(driver).drag_and_drop(dragMe, item4).perform()
# sleep(2)
# # drag_and_drop_by_offset 按当前鼠标的位置的偏移 拖拽一个元素
# # ActionChains(driver).drag_and_drop_by_offset(dragMe,190,250).perform()
# # sleep(2)
# # click_and_hold 鼠标左键持续按住一个元素 move_to_element 移动到某一个元素
# # release 释放鼠标
# # ActionChains(driver).click_and_hold(dragMe).move_to_element(item3).release().perform()
# # sleep(2)
# # click_and_hold 鼠标左键持续按住一个元素
# # move_to_element_with_offset 移动到某一个元素再偏移一定像素
# # release 释放鼠标
# # ActionChains(driver).click_and_hold(dragMe).move_to_element_with_offset(item3,150,10).release().perform()
# # sleep(2)
#
# driver.quit()
#
# # **********************************************
#
# driver.get("http://sahitest.com/demo/keypress.htm")
# sleep(3)
#
# # 找到相关元素
# enter = driver.find_element_by_xpath("//input[@name='t2']")
# keyUp = driver.find_element_by_xpath("//label[contains(.,'Key Up')]")
# keyDown = driver.find_element_by_xpath("//label[contains(.,'Key Down')]")
# keyPress = driver.find_element_by_xpath("//label[contains(.,'Key Press')]")
#
# # 按键周期 按下-按住-抬起 操作逻辑必须符合按键周期
#
# # 按键抬起测试
# ActionChains(driver).click(keyUp).click(enter).key_down("a", enter).key_up("a").perform()
# sleep(2)
#
#
# # 按键按下测试
# keyDown.click()
# enter.click()
# ActionChains(driver).key_down("s",enter).key_up("s").perform()
# sleep(2)
#
#
# # 持续按住测试
# keyPress.click()
# enter.click()
# ActionChains(driver).key_down("d",enter).key_up("d").perform()
# sleep(2)
#
# driver.quit()
#
# # **********************************************
#
# driver.get("http://sahitest.com/demo/alertTest.htm")
# sleep(3)
#
# clickForAlert = driver.find_element_by_xpath("//input[@name='b1']")
# # 触发弹窗
# clickForAlert.click()
# sleep(1)
#
#
# # 切换操作对象
# alert = driver.switch_to_alert()
# sleep(1)
# alert.accept()
# sleep(1)
# driver.quit()
#
# # **********************************************
#
# driver.get("http://www.baidu.com")
# sleep(3)
# # 当前浏览器的标签集合
# print(len(driver.window_handles))
# print(driver.window_handles)
# print("=============================================")
# sleep(2)
#
# driver.execute_script("window.open()")
# driver.switch_to_window(driver.window_handles[1])
# driver.get("http://www.pinduoduo.com")
# print(len(driver.window_handles))
# print(driver.window_handles)
# print("=============================================")
# sleep(2)
#
# driver.execute_script("window.open()")
# driver.switch_to_window(driver.window_handles[2])
# driver.get("http://www.taobao.com")
# sleep(2)
#
# driver.switch_to_window(driver.window_handles[1])
# sleep(2)
#
# driver.switch_to_window(driver.window_handles[0])
# sleep(2)
#
# driver.close()
# sleep(2)
# driver.quit()
# is_time = False
# if not is_time:
#     print(True)
da = {'te': '是吗'}
db = {'te': '是吗'}
al = {da, db}
print(al)
