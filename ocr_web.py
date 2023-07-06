# ------------------------------------------------
# 开发时间：2023-06-19
# 作者：田鑫
# 联系方式：965622832@qq.com
# ------------------------------------------------
# 功能说明：该类用于从指定路径中的图片上传到指定网址进行在线识图文字提取
import os
import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pywinauto import Desktop
from pywinauto.keyboard import send_keys  # 键盘操作
import time
import pymysql
import argparse

PicFormList = ['.jpg', '.jpeg', '.dds', '.psd', '.gif', '.bmp', '.png']


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
    def login_save_session(self, login_url, username, password):
        # 创建浏览器实例
        browser = webdriver.Chrome()
        # 设置隐式等待时长
        browser.implicitly_wait(5)
        # 连接指定连接
        browser.get(login_url)
        browser.delete_all_cookies()

        # 使用指定账户登陆指定网页
        # 指定登陆方式
        login_type_button = browser.find_element(
            By.XPATH, '//*[@id="TANGRAM__PSP_4__changePwdCodeItem"]')
        login_type_button.click()
        # 输入账户名密码后登陆账户
        username_input = browser.find_element(
            By.XPATH, '//*[@id="TANGRAM__PSP_4__userName"]')
        username_input.send_keys(username)
        password_input = browser.find_element(
            By.XPATH, '//*[@id="TANGRAM__PSP_4__password"]')
        password_input.send_keys(password)
        login_submit = browser.find_element(
            By.XPATH, '//*[@id="TANGRAM__PSP_4__submit"]')
        login_submit.click()

        # 获取连接cookies信息
        cookies = browser.get_cookies()
        time.sleep(8)
        return browser, cookies

    # 该函数用于上传图片到指定网址进行文字提取
    def upload_transfer_picture(self, new_browser, cookies, web_url, pathlist):
        # 创建浏览器实例，连接指定的网址

        # # 创建浏览器选项实例
        # chrome_options = webdriver.ChromeOptions()
        # # 打开已有的浏览器，用于调试时免登陆
        # chrome_options.add_experimental_option(
        #     "debuggerAddress", "127.0.0.1:9222")
        # new_browser = webdriver.Chrome(options=chrome_options)

        # 添加免登陆的cookies
        for cookie in cookies:#列表
            if cookie['domain'] == '.baidu.com':
                print(cookie)
                new_browser.add_cookie({'domain':'.baidu.com',#添加cookie
                                    'name':cookie['name'],
                                    'value':cookie['value'],
                                    'path':'/',
                                    'expires':None})
                break

        # 切换到指定网址
        new_browser.get(web_url)
        time.sleep(8)

        # 逐张识别图片
        for picpath in pathlist:
            image_local_input = new_browser.find_element(
                By.XPATH, '/html/body/div/div[1]/div/div[4]/div[2]/div/div/div[2]/div[2]/div[1]/div[3]/div[1]/label')
            image_local_input.click()
            # 选择图片进行上传
            # 创建一个操作桌面窗口的对象
            app = Desktop()
            dlg = app['打开']  # 窗口标题打开
            dlg.window(class_name='ToolbarWindow32',
                       title_re=".*地址.*").click()  # 选择文件地址输入的控件
            send_keys(os.path.split(picpath)[0])  # 输入文件地址
            # 回车
            send_keys('{VK_RETURN}')

            dlg['文件名(&N):Edit'].type_keys(
                os.path.split(picpath)[-1])  # 选择文件名输入的控件输入文件名
            dlg['打开(&O)'].click()  # 点击打开按钮
            time.sleep(3)
            pic_char_element = new_browser.find_element(
                By.XPATH, '/html/body/div/div[1]/div/div[4]/div[2]/div/div/div[2]/div[3]/div/div[1]/div[2]/ul')
            text_content = pic_char_element.text
            text_list = []
            table_list = []
            each_test_list = []
            data_list = []
            for text_test in text_content.split('\n')[1:]:
                text_list.append(text_test.split()[-1])
            for test_each in text_list:
                if test_each.isdigit():
                    index_test = text_list.index(test_each)
                    break
            table_list=text_list[1:index_test]
            for test_each in text_list[index_test:]:
                each_test_list.append(test_each)
                if text_list.index(test_each) % index_test == index_test - 1:
                    if len(each_test_list) > 1:
                        data_list.append(each_test_list[1:])
                    each_test_list = []
        return table_list, data_list
        # new_browser.close()


    def insert_data_to_mysql(self, host, user, password, database, table_list, data_list):
        # 打开数据库连接，参数1：主机名或IP；参数2：用户名；参数3：密码；参数4：数据库名
        db = pymysql.connect(host=host, user=user, password=password, database=database)

        # 使用cursor()创建一个cursor对象
        cursor = db.cursor()
        # 在数据库中插入数据
        cursor.executemany("insert into usr_contact_info({}) values (%s,%s,%s,%s)".format(",".join(table_list)), data_list)
        db.commit()
        # 查询所有数据

        cursor.execute("select * from usr_contact_info;")
        rs_data_all = cursor.fetchall()
        print(rs_data_all)
        # 关闭数据库

        db.close()
        return rs_data_all

if __name__ == "__main__":

    default_pic_path = "E:/codework/web_script_excute/resource/"
    default_ocr_login_url = "https://login.bce.baidu.com/?account="
    default_ocr_transfer_url = "https://cloud.baidu.com/product/ocr/general?p=%E5%8A%9F%E8%83%BD%E6%BC%94%E7%A4%BA&from=experience"
    default_ocr_username = "18384121601"
    default_ocr_password = "Tianxin_2015"
    default_sql_url = 'localhost'
    default_sql_username = "root"
    default_sql_password = "Tianxin_2015"
    default_database = "usr_contact_info"

    parser = argparse.ArgumentParser(usage='test',description='please input paras')
    parser.add_argument('-p', '--pic_path', dest='pic_path', type=str, default=default_pic_path, help='please imput picture path')
    parser.add_argument('-ol', '--ocr_login_url', dest='ocr_login_url', type=str, default=default_ocr_login_url, help='please imput ocr login url')
    parser.add_argument('-ot', '--ocr_transfer_url', dest='ocr_transfer_url', type=str, default=default_ocr_transfer_url, help='please imput ocr transfer url')
    parser.add_argument('-on', '--ocr_username', dest='ocr_username', type=str, default=default_ocr_username, help='please imput ocr login name')
    parser.add_argument('-op', '--ocr_password', dest='ocr_password', type=str, default=default_ocr_password, help='please imput ocr login password')
    parser.add_argument('-su', '--sql_url', dest='sql_url', type=str, default=default_sql_url, help='please imput sql url')
    parser.add_argument('-sn', '--sql_username', dest='sql_username', type=str, default=default_sql_username, help='please imput sql username')
    parser.add_argument('-sp', '--sql_password', dest='sql_password', type=str, default=default_sql_password, help='please imput sql password')
    parser.add_argument('-d', '--database', dest='database', type=str, default=default_database, help='please imput sql database')
    args = parser.parse_args()

    pic_path = args.pic_path
    ocr_login_url = args.ocr_login_url
    ocr_transfer_url = args.ocr_transfer_url
    ocr_username = args.ocr_username
    ocr_password = args.ocr_password
    sql_url = args.sql_url
    sql_username = args.sql_username
    sql_password = args.sql_password
    database = args.database

    ocr_web = Ocr_web()
    picpathlist = ocr_web.get_picture_list(pic_path)
    new_browser, cookies = ocr_web.login_save_session(ocr_login_url, ocr_username, ocr_password)
    # 

    table_list, data_list = ocr_web.upload_transfer_picture(new_browser, cookies, ocr_transfer_url, picpathlist)
    ocr_web.insert_data_to_mysql(sql_url, sql_username, sql_password, database, table_list, data_list)