#coding=utf-8
import unittest
from ddt import ddt,data,unpack,file_data



@ddt
class ddtTestcase(unittest.TestCase):
    # @data(1,2,3)
    # def test_ddt1(self,value):
    #     print value
    #     self.assertEqual(value,2,"不相等")
    #     #self.assertEqual(value,2)

    # @data((1,2),(2,3),(2,2))
    # @unpack
    # def test_tuple(self,*args,**kwargs):
    #     print args

    @unpack
    @data({"a":1,"b":2},{"d":3,"e":2})
    def test_dict(self,value1,value2):
        print value1,value2

    @file_data('dd.json')
    def test_file(self,value):
        print value


if __name__=='__main__':
    unittest.main()
