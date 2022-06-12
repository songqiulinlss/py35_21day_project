import unittest
import os
import requests
from unittestreport import ddt,list_data
from common.handle_excel import HandleExel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_replace import replace_data


@ddt
class TestLogin(unittest.TestCase):
    excel = HandleExel(os.path.join(DATA_DIR,'apicases.xlsx'),'login')
    #读取用例的数据
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env','headers'))
    @list_data(cases)
    def test_login(self,item):
        url = self.base_url + item['url']
        item['data'] = replace_data(item['data'],TestLogin)
        params = eval(item['data'])
        method = item['method'].lower()
        expected = eval(item['expected'])
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        # 断言
        print("预期结果:",expected)
        print("实际结果:", res)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            my_log.error("用例-----[{}]-----执行失败".format(item['title']))
            # my_log.error(e)
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例-----[{}]-----执行通过".format(item['title']))

    # def AssertDictIn(self,expected,res):
    #     '''字典成员运算的逻辑'''
    #     for k,v in expected.items():
    #         if res.get(k) == v:
    #             pass
    #         else:
    #             raise AssertionError("{} not in {}".format(expected,res))