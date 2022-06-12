import  unittest

class TestDemo(unittest.TestCase):
    def test_demo(self):
        # 实际结果
        res = {"code":0,"msg":"OK","time":"201023"}

        #预期结果
        expected = {"code":0,"msg":"OK"}

        self.assertDictIn(expected,res)

    def assertDictIn(self,expected,res):
        '''字典成员运算的逻辑'''
        for k,v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected,res))

# 实际结果
# res = {"code":0,"msg":"OK","time":"201023"}
#
# #预期结果
# expected = {"code":0,"msg":"OK"}
# for k, v in expected.items():
#     print(k,v)
