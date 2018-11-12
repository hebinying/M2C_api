#coding=utf-8
import xlrd

class ExcelUtil():
    def __init__(self,excelPath,sheetName="Sheet1"):
        self.data=xlrd.open_workbook(excelPath)
        self.table=self.data.sheet_by_index(0)
        self.keys=self.table.row_values(0)
        self.nrows=self.table.nrows
        self.ncols=self.table.ncols
        print self.nrows,self.ncols


    def dict_data(self):
        if self.nrows<=1:
            print "总行数小于1，无测试数据，请检查数据信息"
        else:
            r=[]
            for j in range(1,self.nrows):
                s={}
                # rowNum做什么用的
                s['rowNum']=j
                values=self.table.row_values(j)
                print j
                for x in range(0,self.ncols-1):
                    s[self.keys[x]]=values[x]

                print s
                r.append(s)
            return r


if __name__=="__main__":
    filepath="api_manage.xlsx"
    sheetName="Sheet1"
    data=ExcelUtil(filepath)
    print data.dict_data()
