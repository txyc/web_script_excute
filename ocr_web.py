# ------------------------------------------------
# 开发时间：2023-06-19
# 作者：田鑫
# 联系方式：965622832@qq.com
# ------------------------------------------------
# 功能说明：该类用于从指定路径中的图片上传到指定网址进行在线识图文字提取
import os
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pywinauto import Desktop
from pywinauto.keyboard import send_keys # 键盘操作
import time

PicFormList = ['.jpg','.jpeg','.dds','.psd','.gif','.bmp','.png']

class Ocr_web(object):
    # 该函数用于获取指定路径中的图片
    def get_picture_list(self, path):
        picpath = os.path.abspath(path)
        filenamelist = os.listdir(path)
        picpathlist = []
        for filename in filenamelist:
            if os.path.splitext(filename)[-1] in PicFormList:
                picpathlist.append(os.path.join(picpath, filename))
        return picpathlist

    # 登陆指定网址获取连接id
    def login_save_session(self, login_url, username, password, yaml_path):
        # 创建浏览器选项实例
        # chrome_options = webdriver.ChromeOptions()
        # 配置headless无界面浏览器模式
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # login_path = r'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data'
        # chrome_options.add_argument(r"user-data-dir={:s}".format(login_path))
        # 使用指定的浏览器选项打开指定网页，当前选项为无界面模式
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        # 使用指定的浏览器选项打开指定网页，当前选项为界面模式
        browser = webdriver.Chrome()
        print(browser.capabilities['browserVersion'])
        # 设置隐式等待时长
        browser.implicitly_wait(5)
        # 连接指定连接
        browser.get(login_url)

        # 使用指定账户登陆指定网页
        # 指定登陆方式
        login_type_button = browser.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_4__changePwdCodeItem"]')
        login_type_button.click()
        # 输入账户名密码后登陆账户
        username_input = browser.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_4__userName"]')
        username_input.send_keys(username)
        password_input = browser.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_4__password"]')
        password_input.send_keys(password)
        login_submit = browser.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_4__submit"]')
        login_submit.click()

        # 获取连接session信息
        remote_executor = browser.command_executor._url
        session_id = browser.session_id
        # 持久化存储
        service = dict(executor = remote_executor,sid = session_id)
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(service, f)
        return service

    def test_transfer(self, web_url, yaml_path):
        caps = {
            "capabilities": {
                "firstMatch": [
                    {"browserName": "chrome"},
                ]
            }
        }
        with open(yaml_path, 'r', encoding='utf-8') as f:
            session = yaml.safe_load(f)
        session_id = session['sid']
        remote_executor = session['executor']
        driver = webdriver.Remote(remote_executor, desired_capabilities=caps)
        driver.close()
        driver.session_id = session_id
        driver.get(web_url)
        time.sleep(30)

    # 该函数用于上传图片到指定网址进行文字提取
    def upload_transfer_picture(self, web_url, pathlist):
        # 创建浏览器实例，连接指定的网址
        # 创建浏览器选项实例
        chrome_options = webdriver.ChromeOptions()
        # 打开已有的浏览器，用于调试时免登陆
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        new_browser = webdriver.Chrome(options=chrome_options)

        # 切换到指定网址
        new_browser.get(web_url)
        for picpath in pathlist:
            image_local_input = new_browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[4]/div[2]/div/div/div[2]/div[2]/div[1]/div[3]/div[1]/label')
            image_local_input.click()
            #选择图片进行上传
            #创建一个操作桌面窗口的对象
            app=Desktop()
            dlg=app['打开'] #窗口标题打开
            dlg.window(class_name='ToolbarWindow32', title_re=".*地址.*").click() #选择文件地址输入的控件
            send_keys(os.path.split(picpath)[0]) #输入文件地址
            send_keys('{VK_RETURN}') #回车E:\codework\web_script_excute\resource

            dlg['文件名(&N):Edit'].type_keys(os.path.split(picpath)[-1])#选择文件名输入的控件输入文件名
            dlg['打开(&O)'].click() #点击打开按钮
            time.sleep(10)
            pic_char_element = new_browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[4]/div[2]/div/div/div[2]/div[3]/div/div[1]/div[2]/ul')
            text_content = pic_char_element.text
            print(text_content)
        # new_browser.close()

if __name__ == "__main__":
    ocr_web = Ocr_web()
    picpathlist = ocr_web.get_picture_list("./resource/")
    login_url = "https://login.bce.baidu.com/?account="
    web_url = "https://cloud.baidu.com/product/ocr/general?p=%E5%8A%9F%E8%83%BD%E6%BC%94%E7%A4%BA&from=experience"
    username = "18384121601"
    password = "Tianxin_2015"
    yaml_path = './session.yaml'
    ocr_web.login_save_session(login_url, username, password, yaml_path)
    ocr_web.test_transfer(web_url, yaml_path)
    # ocr_web.upload_transfer_picture(web_url, picpathlist)