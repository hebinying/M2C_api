#coding=gbk
import xlrd
import writeExcel
import os

# data_path=os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"data")
#��Ŀ¼���л�ȡ·��
# report_path=os.path.join(os.path.abspath(os.getcwd()),"report")
report_path=os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),"report")
print "�����·����"+report_path
#��Ŀ¼���л�ȡ·��
# report_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "report")

class FileUtil():
    def __init__(self,path):
        self.path=path
        self.textxlsx=[]
        self.reportxlsx=[]
        print "����������ԴĿ¼:%s"%(self.path)
        if os.path.exists(self.path):
            dirs = os.listdir(self.path)
            for dir in dirs:
                if os.path.splitext(dir)[1] == '.xlsx' and "m2c_api" in dir:
                    print "����������Դ��%s"%dir
                    self.textxlsx.append(os.path.join(self.path, dir))
                    self.reportxlsx.append(os.path.join(report_path, dir))

    def get_file(self):
        testcases=[]
        for i in range(0,len(self.textxlsx)):
            print "�������ݱ�%s"%self.textxlsx[i]
            # print self.reportxlsx[i]
            writeExcel.copy_excel(self.textxlsx[i], self.reportxlsx[i])
            table=TableUtil(self.textxlsx[i],self.reportxlsx[i])
            if table.execute()!=None:
                testcases.extend(table.execute())
        return testcases




class TableUtil():
    def __init__(self,excelPath,reportPath):
        self.data=xlrd.open_workbook(excelPath)
        self.path=excelPath
        self.reportpath=reportPath
        self.sheet=len(self.data.sheets())
        print "�ļ��ڱ��������%d" %self.sheet
    def execute(self):
        list=[]
        if self.sheet<=0:
            print "�����Ϊ0"
        else:
            for i in range(0,self.sheet):
                a=ExcelUtil(self.path,self.reportpath,i)
                if a.dict_data()!=None:
                    list.extend(a.dict_data())
            return list
#����ȡ
class ExcelUtil():
    def __init__(self,excelPath,reportPath,index=0):
        # print "�ļ�%s���%d����" %(excelPath,index)
        self.data=xlrd.open_workbook(excelPath)
        self.reportPath=reportPath
        self.table=self.data.sheet_by_index(index)
        self.nrows=self.table.nrows
        self.ncols=self.table.ncols
        if self.nrows>0:
            self.keys = self.table.row_values(0)
        print "�ļ�%s�ڵ�%d������������%d:%d" %(excelPath,index,self.nrows,self.ncols)


    def dict_data(self):
        if self.nrows<=1:
            print "������С��1���޲������ݣ�����������Ϣ"
        else:
            r=[]
            for j in range(1,self.nrows):
                s={}
                # rowNum��ʲô�õ�
                s['reportfile']=self.reportPath
                s['rowNum']=j
                values=self.table.row_values(j)
                for x in range(0,self.ncols-1):
                    s[self.keys[x]]=values[x]

                # print s
                r.append(s)
            return r


if __name__=="__main__":
    filepath="api_manage.xlsx"
    sheetName="Sheet1"
    # data=FileUtil(data_path)
    # print data.get_file()
