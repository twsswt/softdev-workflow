'''
Created on 30 Mar 2016

@author: Tim
'''
import unittest
from models.workflows.waterfall import Waterfall
from random import Random


class Test(unittest.TestCase):

    def setUp(self):
        self.workflow = Waterfall([3,5,7])
        pass
    
    
    def testName(self):

        random = Random()
        random.seed(1)
        self.workflow.work(random, None)
        
        software_system = self.workflow.deliver()
        
        print "Operating."
        successful_operations = software_system.operate(random,10000)
        self.assertEquals(53, len(successful_operations))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()