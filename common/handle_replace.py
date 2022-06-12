import re

from common.handle_conf import conf


def replace_data(data,cls):

    while re.search('#(.+?)#',data):
        res2 = re.search('#(.+?)#',data)
        item = res2.group()
        attr = res2.group(1)
        try:
            value = getattr(cls,attr)
        except AttributeError:
            value = conf.get('test_data',attr)
        # 进行数据替换
        data = data.replace(item,str(value))
    return  data


if __name__ == '__main__':
    class TestData():
        id = 1
        user = 'abc'
        word = 'asdasd'
    s = '{"id": "#id#", "user": "#user#", "word": "#word#"}'

    res = replace_data(s,TestData)
    print(res)