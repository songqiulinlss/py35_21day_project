from configparser import ConfigParser
from common.handle_path import CONF_DIR
import os

class Config(ConfigParser):
    '''再创建对象时，直接加载配置文件中的内容'''
    def __init__(self,conf_file):
        super().__init__()
        self.read(conf_file,encoding='utf-8')
conf = Config(os.path.join(CONF_DIR,"config.ini"))

if __name__ == '__main__':

    # conf = ConfigParser()
    # conf.read(r'D:\python\python35\py35_17day\config.ini',encoding='utf-8')
    name = conf.get("logging",'name')
    level = conf.get("logging",'level')
    filenmae = conf.get("logging",'filenmae')
    sh_level = conf.get("logging",'sh_level')
    fh_level = conf.get("logging",'fh_level')
    print(name)
    print(level)
    print(filenmae)
    print(sh_level)
    print(fh_level)