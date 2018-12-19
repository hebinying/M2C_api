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
#��Ŀ¼���л�ȡ·��
# data_path=os.path.join(os.path.abspath(os.getcwd()),"data")
data_path=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),"data")
report_path=report_path
print "���ݻ�ȡ·����"+data_path
#��Ŀ¼���л�ȡ·��
# data_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "data")
# report_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "report")

#��ȡ��������
testdata=readExcel.FileUtil(data_path).get_file()

# curpath=os.path.dirname(os.path.realpath(__file__))
# textxlsx=os.path.join(curpath,"api_manage.xlsx")
#
# report_path=os.path.join(os.path.dirname(curpath),"report")
# reportxlsx=os.path.join(report_path,"result.xlsx")

print u"���ز������ݼ���:%s"%testdata

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
        print u"����-->:%s"%data
        base_api.write_result(res,filepath=data["reportfile"])
        check=data["checkpoint"]
        print u"����-->:%s" %check
        res_text=res["text"]
        print u"����ʵ�ʽ��-->:%s" %res_text
        self.assertTrue(check in res_text)
        #��Ҫ���ӽ���ж�

if __name__=='__main__':
    unittest.main()
