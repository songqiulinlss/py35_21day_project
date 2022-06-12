'''
审核接口:  管理员审核

审核的前置条件:
        1、管理员登录(类级别的前置)

        2、普通用户登录
            1）、普通用户角色添加项目(类级别的前置)
            2）、创建一个项目(用例级别前置)


'''
import unittest
import os
import requests
import random
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_conf import conf
from common.handle_excel import HandleExel
from common.handle_log import my_log
from common.handle_path import DATA_DIR
from common.handle_replace import replace_data
from common.handle_mysql import HandleDB

@ddt
class TestAudit(unittest.TestCase):
    excel = HandleExel(os.path.join(DATA_DIR,'apicases.xlsx'),'audit')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls) -> None:
        #---------------管理员登录---------------
        # 请求登录接口,进行登录
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data', 'admin_mobile'),
            'pwd': conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        admin_token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + admin_token
        cls.admin_headers = headers
        cls.admin_member_id = jsonpath(res, '$..id')[0]

        # --------------普通用户登录---------------
        # 请求登录接口,进行登录
        params = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers
        cls.member_id = jsonpath(res, '$..id')[0]


    def setUp(self) -> None:
        '''用例级别前置:添加项目'''
        # 第一步:准备数据
        url = conf.get('env','base_url') + '/loan/add'
        params =  {
            "member_id": self.member_id,
             "title": "学习使人进步",
             "amount": 2000,
             "loan_rate": 12.0,
             "loan_term": 3,
             "loan_date_type": 1,
             "bidding_days": 5
             }
        # 第二步: 请求添加项目的接口
        response = requests.post(url=url,json=params,headers=self.headers)
        res = response.json()
        # 第三步:提取项目的id
        TestAudit.loan_id = jsonpath(res,'$..id')[0]


    @list_data(cases)
    def test_audit(self,item):
        # 准备数据
        url = conf.get('env','base_url') + item['url']
        item['data'] = replace_data(item['data'],TestAudit)
        params = eval(item['data'])
        method = item['method']
        expected = eval(item['expected'])

        # 调用接口
        response = requests.request(method=method,url=url,json=params,headers=self.admin_headers)
        res = response.json()

        #判断是否是审核通过的用例,并且审核成功，如果是审核通过则保存项目id为审核通过的项目id
        if item['title'] == '审核通过' and  res['msg'] == 'OK':
            TestAudit.pass_loan_id = params['loan_id']
        print("预期结果:",expected)
        print("实际结果:",res)
        # 断言
        try:
             self.assertEqual(expected['msg'],res['msg'])
             self.assertEqual(expected['code'],res['code'])
             if item['check_id']:
                 sql = 'SELECT status FROM futureloan.loan WHERE id={}'.format(self.loan_id)
                 status = self.db.find_one(sql)[0]
                 print('数据库中的状态:',status)
                 print('实际的状态为:', expected['status'])
                 self.assertEqual(expected['status'],str(status))

        except AssertionError as e:
            my_log.error("用例----[{}]----执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.error("用例----[{}]----执行成功".format(item['title']))

