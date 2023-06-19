# ------------------------------------------------
# 开发时间：2023-06-19
# 作者：田鑫
# 联系方式：965622832@qq.com
# ------------------------------------------------
# 功能说明：该类用于从指定路径中的图片上传到指定网址进行在线识图文字提取
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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

    # 该函数用于上传图片到指定网址进行文字提取
    def upload_transfer_picture(self, web_url, path):
        # 创建浏览器选项实例
        chrome_options = webdriver.ChromeOptions()
        # 配置headless无界面浏览器模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 使用指定的浏览器选项打开指定网页，当前选项为无界面模式
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        browser = webdriver.Chrome()
        # 设置隐式等待时长
        browser.implicitly_wait(5)
        # 连接指定连接
        browser.get(web_url)


if __name__ == "__main__":
    ocr_web = Ocr_web()
    print(ocr_web.get_picture_list("./resource/"))