#!../tools/python27/bin/python
#-*- coding:utf-8 -*-
import string
import commands

class disks:
    response = ''
    
    CMD_1 = "df -a | grep /media" 
        
    def start(self, request):
        result = 0
        detail = 0
        self.response = ''
               
        
        #output_dic=request.args
        #print 'output_dic:\n',output_dic
        #request.write(str(output_dic))
        if 'detail' in request.args:
            detail = string.atoi(request.args['detail'][0])               
        #self.response += 'detail: %d\n' % (detail)
        
        (status, output) = commands.getstatusoutput(self.CMD_1)
        if(status != 0):
            result = -1
            self.response += 'internal error!'
        else:
            result = 0
            self.response += output
                    
        request.write(self.response)
        return result
        
