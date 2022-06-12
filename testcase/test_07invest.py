import  unittest
import os
import requests
from unittestreport import ddt,list_data
from common.handle_conf import conf
from common.handle_excel import HandleExel
from common.handle_log import my_log
from common.handle_path import DATA_DIR
from testcase.fixture import BaseTest
from common.handle_replace import replace_data
from common.handle_mysql import HandleDB

@ddt
class TestInvest(unittest.TestCase,BaseTest):
    excel = HandleExel(os.path.join(DATA_DIR,'apicases.xlsx'),'invest')
    cases = excel.read_data()
    db = HandleDB()
    @classmethod
    def setUpClass(cls) -> None:
        Basetest = BaseTest()
        # 普通用户登录
        Basetest.user_login()
        # 管理员用户登录
        Basetest.admin_login()
        # 添加项目
        Basetest.add_project()
        # 审核
        Basetest.audit()


    @list_data(cases)
    def test_invest(self,item):
        # 准备用例数据
        url = conf.get('env','base_url')  + item['url']
        item['data'] = replace_data(item['data'],TestInvest)
        params = eval(item['data'])
        expected = eval(item['expected'])
        method = item['method']
        #---------------投资之前查询数据库-----------------
        # 查用户表SQL
        sql1 = 'select leave_amount from futureloan.member where id="{}"'.format(self.member_id)
        # 投资记录表SQL
        sql2 = 'select * from futureloan.invest where member_id="{}"'.format(self.member_id)
        # 流水记录表SQL
        sql3 = 'select * from futureloan.financelog where pay_member_id="{}"'.format(self.member_id)
        if item['check_id']:
            s_amount = self.db.find_one(sql1)[0]
            s_invest= self.db.find_count(sql2)
            s_financelog = self.db.find_count(sql3)
        # 发送请求
        response = requests.request(method=method,url=url,json=params,headers=self.headers)
        res = response.json()
        print('预期结果:',expected)
        print('实际结果:',res)
        # ---------------投资之后查询数据库-----------------
        if item['check_id']:
            e_amount = self.db.find_one(sql1)[0]
            e_invest= self.db.find_count(sql2)
            e_financelog = self.db.find_count(sql3)
        # 断言
        try:
            self.assertEqual(expected['code'],res['code'])
            # 断言实际结果中的msg是否包含预期结果中的内容
            self.assertIn(expected['msg'],res['msg'])
            if item['check_id']:
                # 断言金额
                self.assertEqual(float(params['amount']),(s_amount-e_amount))
                # 断言投资记录
                self.assertEqual(1,e_invest-s_invest)
                # 断言流水记录
                self.assertEqual(1,e_financelog - s_financelog)
        except AssertionError as e:
            my_log.error("用例----[{}]----执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.error("用例----[{}]----执行成功".format(item['title']))
