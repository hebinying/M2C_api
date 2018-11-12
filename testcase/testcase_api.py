#coding=utf-8
import unittest
from ddt import ddt,data,unpack,file_data
import ddt
import os
from common import readExcel,writeExcel,base_api
import requests

curpath=os.path.dirname(os.path.realpath(__file__))
textxlsx=os.path.join(curpath,"api_manage.xlsx")

report_path=os.path.join(os.path.dirname(curpath),"report")
reportxlsx=os.path.join(report_path,"result.xlsx")

testdata=readExcel.ExcelUtil(textxlsx).dict_data()
print testdata

@ddt.ddt
class ddtTestcase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=requests.session()
        writeExcel.copy_excel(textxlsx,reportxlsx)

    @ddt.data(*testdata)
    def test_api(self,data):
        print data
        res=base_api.send_requests(self.s,data)
        base_api.write_result(res,filepath=reportxlsx)
        check=data["checkpoint"]
        print "检查点-->:%s" %check

        res_text=res["text"]
        print "返回实际结果-->:%s" %res_text

        self.assertTrue(check in res_text)

if __name__=='__main__':
    unittest.main()
