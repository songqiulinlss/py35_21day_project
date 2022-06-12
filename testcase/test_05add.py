import  unittest
import os

import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandleExel
from common.handle_log import my_log
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_replace import replace_data
from common.handle_mysql import HandleDB

@ddt
class TestAdd(unittest.TestCase):
    excel = HandleExel(os.path.join(DATA_DIR,'apicases.xlsx'),'add')
    cases = excel.read_data()
    db = HandleDB()
    @classmethod
    def setUpClass(cls):
        # 第一步:请求登录接口,进行登录
        url = conf.get('env','base_url') + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data','mobile'),
            'pwd' : conf.get('test_data','pwd')
        }
        headers = eval(conf.get('env','headers'))
        response = requests.post(url=url,json=params,headers=headers)
        res = response.json()
        token = jsonpath(res,'$..token')[0]
        headers['Authorization']  = 'Bearer ' + token
        cls.headers = headers
        cls.member_id = jsonpath(res,'$..id')[0]

    @list_data(cases)
    def test_add(self,item):
        # 第一步:请求登录接口,进行登录
        url = conf.get('env','base_url') + item['url']
        expected = eval(item['expected'])
        method = item['method'].lower()
        item['data'] = replace_data(item['data'],TestAdd)
        params = eval(item['data'])
        # 调用接口之前查询数据库该用户的项目数量
        sql ='SELECT * FROM futureloan.loan WHERE member_id={}'.format(self.member_id)
        start_count = self.db.find_count(sql)
        # 第二步:调用接口
        response = requests.request(url=url,method=method,json=params,headers=self.headers)
        res = response.json()
        # 调用接口之后查询数据库该用户的项目数量
        end_count = self.db.find_count(sql)
        print("预期结果:",expected)
        print("实际结果:",res)
        # 第三步:断言
        try:
             self.assertEqual(expected['msg'],res['msg'])
             self.assertEqual(expected['code'],res['code'])
             # 根据添加的项目是否成功,来对数据库分别进行校验
             if item['res']:
                 self.assertEqual((end_count-start_count),1)
                 print("调用接口之前数据库的数量为:", start_count)
                 print("调用接口之后数据库的数量为:", end_count)
                 print("新增的项目为:", (end_count-start_count))
        except AssertionError as e:
            my_log.error("用例----[{}]----执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.error("用例----[{}]----执行成功".format(item['title']))