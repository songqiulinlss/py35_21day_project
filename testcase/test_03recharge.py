'''
充值的前提:登录--->提取token
unittest:
    用例级别的前置:setUp
    测试类级别的前置:setUpClass

'''
import unittest
import os
import  requests
from  unittestreport import ddt,list_data
from common.handle_excel import HandleExel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from jsonpath import  jsonpath
from common.handle_log import my_log
from  common.handle_mysql import  HandleDB
from common.handle_replace import replace_data

@ddt
class TestRecharge(unittest.TestCase):
    excel = HandleExel(os.path.join(DATA_DIR,'apicases.xlsx'),'recharge')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls):
        '''用例类的前置方法:登录提取token'''
        # 1、请求登录接口,进行登录
        url = conf.get('env','base_url') +'/member/login'
        params = {
            'mobile_phone': conf.get('test_data','mobile'),
            'pwd': conf.get('test_data','pwd')
        }
        headers = eval(conf.get('env','headers'))
        response = requests.post(url=url,json=params,headers=headers)
        res = response.json()

        # 2、登录成功之后再去提取token
        token = jsonpath(res,'$..token')[0]
        # 将token添加到请求头中
        headers['Authorization'] = 'Bearer ' + token
        #保存含有token的请求头为类属性
        cls.headers = headers
        # setattr(TestRecharge,'headers',headers)
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def test_recharge(self,item):
        # 第一步:准备数据
        url = conf.get('env', 'base_url') + item['url']
        # 动态处理需求进行替换的参数
        # item['data'] = item['data'].replace('#member_id#',str(self.member_id))
        item['data'] = replace_data(item['data'],TestRecharge)

        params = eval(item['data'])
        expected = eval(item['expected'])
        method = item['method'].lower()
        ############请求接口之前查询用户的余额############
        sql = 'select leave_amount from futureloan.member where mobile_phone="{}"'.format(
            conf.get('test_data', 'mobile'))
        start_amount = self.db.find_one(sql)[0]
        print('请求接口之前的余额为:',start_amount)

        # 第二步:发送请求,获取接口返回的实际结果
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        print("预期结果:",expected)
        print("实际结果:",res)
        ############请求接口之后查询用户的余额############
        end_amount = self.db.find_one(sql)[0]
        print('请求接口之后的余额为:',end_amount)

        # 第三步:断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            ############校验数据库用户余额变化是否等于充值金额############
            if res['msg'] == 'OK':

                self.assertEqual(float(end_amount-start_amount),params['amount'])
                print('充值金额为:',params['amount'])
            else:
                self.assertEqual(float(end_amount - start_amount),0)
            # print('')
        except AssertionError as e:
            my_log.error("用例----[{}]----执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例----[{}]----执行成功".format(item['title']))