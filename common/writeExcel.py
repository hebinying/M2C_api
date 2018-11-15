#coding=utf-8
from xlutils.copy import copy
import xlrd,xlwt

def copy_excel(excelpath1,excelpath2):
    wb1=xlrd.open_workbook(excelpath1,'rb')
    wb2=copy(wb1)
    wb2.save(excelpath2)

class Write_excel(object):
    def __init__(self,filename):
        self.filname=filename
        self.wb1=xlrd.open_workbook(self.filname)
        self.wb=copy(self.wb1)
        self.ws=self.wb.get_sheet(0)

    def write(self,row_n,col_n,value):
        self.ws.write(row_n,col_n,value)
        self.wb.save(self.filname)


if __name__=="__main__":
    copy_excel("api_manage.xlsx","copy_test.xlsx")
    wt=Write_excel("copy_test.xlsx")
    wt.write(4,5,"copy")
    wt.write(4, 6, "save")



