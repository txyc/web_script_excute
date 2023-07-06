import pytest
import argparse
import pdb
from ocr_web import Ocr_web
import logging

class Test_format_ocr_sql:

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

    # python3.9版本以后，可以直接使用encoding参数编码记录的日志格式
    logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s %(message)s', 
                        handlers=[logging.FileHandler("./log/test.log", encoding='utf-8', mode='a+'),],
                        level=logging.INFO)

    # 用于上传图片到指定网址提取文字信息
    logging.info("上传图片到指定网址{}提取文字信息".format(ocr_transfer_url))
    @pytest.mark.parametrize("login_url, username, password, transfer_url, sql_url, sql_username, sql_password, database, pic_path",
                            [[ocr_login_url, ocr_username, ocr_password, ocr_transfer_url, sql_url, sql_username, sql_password, database, pic_path]])
    def test_get_ocr_info(self, login_url, username, password, transfer_url, sql_url, sql_username, sql_password, database, pic_path):
        ocr_web = Ocr_web()

        logging.info("获取指定路径{}下的图片路径".format(pic_path))
        picpathlist = ocr_web.get_picture_list(pic_path)
        logging.info("获取到的图片路径{}".format(picpathlist))

        logging.info("登陆指定网址获取cookie信息")
        browser, cookies = ocr_web.login_save_session(login_url, username, password)
        logging.info("获取到cookie信息{}".format(cookies))
        assert len(cookies) > 0
        
        logging.info("使用cookie信息到指定网址转化图片信息")
        pdb.set_trace()
        table_list, data_list = ocr_web.upload_transfer_picture(browser, cookies, transfer_url, picpathlist)
        logging.info("获取到的文字序号信息为{}".format(table_list))
        assert len(table_list) > 0
        logging.info("获取到的文字内容信息为{}".format(data_list))
        assert len(data_list) > 0

        logging.info("将获取到的文字信息上传到数据库")
        rs_data_list = ocr_web.insert_data_to_mysql(sql_url, sql_username, sql_password, database, table_list, data_list)
        logging.info("数据库内的数据信息为{}".format(rs_data_list))
        assert len(rs_data_list) > 0
    
if __name__ == "__main__":
    pytest.main(["-vs"])