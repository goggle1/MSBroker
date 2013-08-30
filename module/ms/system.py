#!../tools/python27/bin/python
#-*- coding:utf-8 -*-

import string
import commands

class check_item:
    name    = ''
    cmd     = ''
    status  = 0
    output  = ''

    def __init__(self, name, cmd, status, output):
        self.name = name
        self.cmd = cmd
        self.status = status
        self.output = output
        
        
class system:
    NAME_1 = 'cpu'
    NAME_2 = 'mem'
    NAME_3 = 'io'
    NAME_4 = 'net'
  
    COUNT = 2  
    CMD_1 = 'mpstat 1 %d' % (COUNT)    
    CMD_2 = 'free'
    CMD_3 = 'vmstat 1 %d' % (COUNT)
    CMD_4 = 'sar -n DEV 1 %d' % (COUNT)   
    
    response = ''
    
    items = [ \
             check_item(NAME_1, CMD_1, 0, ''), \
             check_item(NAME_2, CMD_2, 0, ''), \
             check_item(NAME_3, CMD_3, 0, ''), \
             check_item(NAME_4, CMD_4, 0, ''), \
             ]
    
    def check_item(self, item):
        (status, output) = commands.getstatusoutput(item.cmd)
        item.status = status
        item.output = output
        
        return 0
        
    def start(self, request):
        detail = 0
        self.response = ''
        
        if 'detail' in request.args:
                detail = string.atoi(request.args['detail'][0])
                
        for item in self.items:
            self.check_item(item)
        
        if(detail == 0):
            for item in self.items:
                self.response += 'item: '
                self.response += item.name
                self.response += '\t'
                self.response += 'info: \n'
                self.response += item.output                                    
                self.response += '\n'
                self.response += '\n'
        elif(detail == 1):
            for item in self.items:
                self.response += 'item: '
                self.response += item.name
                self.response += '\n'
                self.response += 'cmd: '
                self.response += item.cmd
                self.response += '\n'
                self.response += 'status: '
                self.response += str(item.status)
                self.response += '\n'
                self.response += 'info: '
                self.response += '\n'
                self.response += item.output
                self.response += '\n'
                self.response += '\n'
        elif(detail == 2):
            self.response += '<table border="1" style="table-layout:fixed;word-break: break-all; word-wrap: break-word;">'
            self.response += '<tr>'
            self.response += '<td width="5%">'
            self.response += 'item'
            self.response += '</td>'
            self.response += '<td width="20%">'
            self.response += 'cmd'
            self.response += '</td>'
            self.response += '<td width="5%">'
            self.response += 'status'
            self.response += '</td>'
            self.response += '<td width="70%">'
            self.response += 'info'
            self.response += '</td>'
            self.response += '</tr>'
            for item in self.items:
                self.response += '<tr>'
                self.response += '<td>'
                self.response += item.name
                self.response += '</td>'
                self.response += '<td>'
                self.response += item.cmd
                self.response += '</td>'
                self.response += '<td>'
                self.response += str(item.status)
                self.response += '</td>'
                self.response += '<td>'
                #self.response += item.output
                lines = item.output.split('\n')
                for line in lines:
                        self.response += line
                        self.response += '<br>'
                self.response += '</td>'
                self.response += '</tr>'
            self.response += '</table>'
        else:
            self.response += 'unsupport detail: %d\n' % (detail)   
        
        request.write(self.response)
            
        return 0
