#!/usr/local/bin/python
'''#!/home/admin/broker_project/build_tools/python272/bin/python
'''
#-*- coding:utf-8 -*-

from twisted.web import http
import sys
import json
import traceback

class RecordReasonException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, reason_line):
        Exception.__init__(self)
        self.reason_line = reason_line

class MyRequestHandler(http.Request):
  
    def process(self):
        try:
            self.__load_module()
        except:
            print traceback.format_exc()
        finally:
            self.finish()

    def __load_module(self):
        flag = 0
        try:
            print 'client: ', self.getClient()
            print 'uri: ', self.uri            
            
            if 'cmd' not in self.args:
                #print "no cmd: no module name"        
                raise RecordReasonException( 'no cmd: ' + self.uri)
            module_path = 'module.' + self.path.strip('/') + '.' + self.args['cmd'][0]
            print "module_path:", module_path

            if module_path in sys.modules:
                print module_path
                print "del original module..."
                del sys.modules[module_path]
            module = __import__(module_path)
            module_obj_0 = getattr(module, self.path.strip('/'))
            module_obj_1 = getattr(module_obj_0, self.args['cmd'][0])
            Module_Class_obj = getattr(module_obj_1, self.args['cmd'][0])()

            print "Module_Operate_obj.start ..."
            if 0 != Module_Class_obj.start(self):
                raise Exception()

        except RecordReasonException,x:
            flag = -1
            print traceback.format_exc()
            self.setResponseCode(http.NOT_FOUND)
            self.write("\r\nError Reason: '%s'.\r\n"%(x.reason_line))
        except:
            flag = -1
            print traceback.format_exc()
            self.setResponseCode(http.NOT_FOUND)
            self.write("\r\nLoad Module ... Failure\r\n")
        finally:
            return flag



class MyHttp(http.HTTPChannel):
    requestFactory = MyRequestHandler


class MyHttpFactory(http.HTTPFactory):
    protocol = MyHttp
    

if __name__=="__main__":
    from twisted.internet import reactor
    reactor.listenTCP(11000, MyHttpFactory())
    print 'running ...'
    reactor.run()
    print 'over'
