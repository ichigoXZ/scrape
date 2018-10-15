from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException,NoSuchElementException,ElementNotVisibleException
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent=some user-agent name")

desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

driver = webdriver.Chrome()     # 你的google_driver所在目录
# driver.set_page_load_timeout(2)     # 设定页面加载限制时间

def login(url):
    driver.get(url)    # 请求登录页面
    sleep(2)
    print("login...")
    driver.find_element_by_name('form_email').clear()  # 获取用户名输入框，并先清空
    driver.find_element_by_name('form_email').send_keys(u'your_email') # 输入用户名
    driver.find_element_by_name('form_password').clear()  # 获取密码框，并清空
    driver.find_element_by_name('form_password').send_keys(u'your_password') # 输入密码
    captcha=driver.find_element_by_id('captcha_image')  # 获取验证码标签
    submit=driver.find_element_by_class_name('bn-submit')#获取提交按钮
    # 判断是否需要验证码
    if captcha:
        captcha_field=driver.find_element_by_id('captcha_field')  #获取验证码输入框
        text=input("请输入验证码：")  # 控制栏输入验证码
        captcha_field.send_keys(text)  # 将输入的验证码传递给selenium打开的浏览器
    submit.click()  # 登录提交



login('https://www.douban.com')
print('login!')
sleep(2)
driver.get('https://www.douban.com/people/58059215/statuses?p=2')    #要开始删除的广播起始页地址，这里是我的广播的第2页
sleep(3)
print("action!")

while True:
# for i in range(50):           # 广播没有最后一页，所以最好设置页数
    try:
        driver.find_element_by_css_selector('a.btn.btn-action-reply-delete').click()
        sleep(1)
        try:
            Alert(driver).accept()
        except NoAlertPresentException:
            driver.back()
        sleep(3)
    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[4]/span[4]/a').click()
        sleep(3)
    except ElementNotVisibleException:
        sleep(1)


driver.close()  # 关闭chrome进程
driver.quit()  # 关闭chromewebdriver进程
