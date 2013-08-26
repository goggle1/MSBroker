#!../tools/python27/bin/python
#-*- coding:utf-8 -*-

class example_3:
    def start(self,request):

        result = 0
        try: 
            output_dic=request.args
            print 'output_dic:\n',output_dic
            request.write(str(output_dic))
        except:
            result = -1
        finally:
            return result
        
