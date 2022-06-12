import re
class TestData():
    id = 1
    user = 'abc'
    word = 'asdasd'
s = '{"id": "#id#", "user": "#user#", "word": "#word#"}'

res1 = re.search('#(.+?)#',s)
res2 = res1.group()
res3 = res1.group(1)
value = getattr(TestData,res3)
print(res1)
print(res2)
print(res3)
print(value)


