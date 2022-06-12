import unittest
from unittestreport import TestRunner
from common.handle_path import CASES_DIR,REPORT_DIR


class RunTest():
    def main(self):
        suite = unittest.defaultTestLoader.discover(CASES_DIR)
        runner = TestRunner(suite,
                            filename='report.html',
                            report_dir=REPORT_DIR,
                            title='接口自动化测试报告',
                            tester='宋秋林'
                            )
        runner.run()

        # 将测试结果发送到邮箱
        runner.send_email(host='smtp.qq.com',
                          port=465,
                          user='1164169068@qq.com',
                          password='lfithudxbraqjeaf',
                          to_addrs='1164169068@qq.com',
                          is_file=True)

if __name__ == '__main__':
    run = RunTest()
    run.main()



