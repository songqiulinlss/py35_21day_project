import unittest
import os
import requests
import  random
from unittestreport import ddt,list_data
from common.handle_excel import HandleExel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_mysql import HandleDB
from common.handle_replace import replace_data


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExel(os.path.join(DATA_DIR,'apicases.xlsx'),'register')
    #读取用例的数据
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    # 3、请求头(放配置文件)
    headers = eval(conf.get('env','headers'))
    db = HandleDB()
    @list_data(cases)
    def test_register(self,item):
        pass
        # 第一步:准备用例数据
        #1、接口地址
        url = self.base_url + item['url']
        #2、接口请求参数
        if '#mobile#' in item['data']:
            setattr(TestRegister,'mobile',self.random_mobile())
            # phone = self.random_mobile()
            # TestRegister['mobile'] = phone
            # item['data'] = item['data'].replace('#mobile#',phone)
        item['data'] = replace_data(item['data'],TestRegister)
        params = eval(item['data'])
        # #3、请求头(不放配置文件)
        # headers = {
        #     'X-Lemonban-Media-Type':'lemonban.v2'
        # }
        #4、获取请求方法,并转换为小写
        method = item['method'].lower()
        #5、预期结果
        expected = eval(item['expected'])
        # 第二步:请求接口,读取返回实际结果
        #requests.post(url=url,json=params,headers=self.headers)
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()        ############注册之后查询数据库是否有数据############
        sql ='select leave_amount from futureloan.member where mobile_phone="{}"'.format(params.get('mobile_phone',''))
        count = self.db.find_count(sql)

        #第三步:断言
        print("预期结果:",expected)
        print("实际结果:", res)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # self.AssertDictIn(expected,res)
            if item['check']:
                self.assertEqual(1,count)
                print('查询到的条数为:',count)
        except AssertionError as e:
            #记录日志
            my_log.error("用例-----[{}]-----执行失败".format(item['title']))
            # my_log.error(e)
            my_log.exception(e)
            # 回写结果到excel(根据公司中实际需求来决定是否回写结果到excel)  #注:回写excel需要花费大量的时间
            raise e
        else:
            my_log.info("用例-----[{}]-----执行通过".format(item['title']))

    def AssertDictIn(self,expected,res):
        '''字典成员运算的逻辑'''
        for k,v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected,res))


    def random_mobile(self):
        '''随机生成手机号'''
        phone = str(random.randint(13300000000,13399999999))

        return phone