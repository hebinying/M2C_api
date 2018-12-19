#coding=gbk
import unittest
from ddt import ddt,data,unpack,file_data
import ddt
import os
from common import readExcel,writeExcel,base_api
from common.readExcel import report_path
import requests
ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

# filepath=open(ROOT("../data"),'r')
#根目录运行获取路径
# data_path=os.path.join(os.path.abspath(os.getcwd()),"data")
data_path=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),"data")
report_path=report_path
print "数据获取路径："+data_path
#子目录运行获取路径
# data_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "data")
# report_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "report")

#获取测试数据
testdata=readExcel.FileUtil(data_path).get_file()

# curpath=os.path.dirname(os.path.realpath(__file__))
# textxlsx=os.path.join(curpath,"api_manage.xlsx")
#
# report_path=os.path.join(os.path.dirname(curpath),"report")
# reportxlsx=os.path.join(report_path,"result.xlsx")

print u"返回测试数据集合:%s"%testdata

@ddt.ddt
class ddtTestcase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=requests.session()
        # writeExcel.copy_excel(textxlsx,reportxlsx)
        # cls.dataxlsx=textxlsx
        # cls.reportxlsx=reportxlsx

    @ddt.data(*testdata)
    def test_api(self,data):
        print data
        res=base_api.send_requests(self.s,data)
        print u"传参-->:%s"%data
        base_api.write_result(res,filepath=data["reportfile"])
        check=data["checkpoint"]
        print u"检查点-->:%s" %check
        res_text=res["text"]
        print u"返回实际结果-->:%s" %res_text
        self.assertTrue(check in res_text)
        #需要增加结果判断

if __name__=='__main__':
    unittest.main()
