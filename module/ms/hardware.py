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
        
        
class hardware:
    NAME_1 = 'cpu type'
    NAME_2 = 'cpu core'
    NAME_3 = 'bits'
    NAME_4 = 'mem'
    NAME_5 = 'kernel'
    NAME_6 = 'release'
    NAME_7 = 'machine'
    NAME_8 = 'net'
    
    CMD_1 = 'cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c'
    #CMD_2 = 'cat /proc/cpuinfo | grep "physical id" | uniq -c'
    CMD_2 = 'cat /proc/cpuinfo | grep "model name" | wc -l'
    CMD_3 = 'getconf LONG_BIT'
    CMD_4 = 'cat /proc/meminfo  | grep MemTotal'
    CMD_5 = 'uname -a'
    CMD_6 = 'cat /etc/issue | grep release'
    CMD_7 = 'dmidecode | grep "Product Name"'
    CMD_8 = 'ifconfig | grep "Link encap:" | awk \'{print $1}\' | grep -v lo'     
    
    response = ''
    
    items = [ \
             check_item(NAME_1, CMD_1, 0, ''), \
             check_item(NAME_2, CMD_2, 0, ''), \
             check_item(NAME_3, CMD_3, 0, ''), \
             check_item(NAME_4, CMD_4, 0, ''), \
             check_item(NAME_5, CMD_5, 0, ''), \
             check_item(NAME_6, CMD_6, 0, ''), \
             check_item(NAME_7, CMD_7, 0, ''), \
             check_item(NAME_8, CMD_8, 0, ''), \
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
                self.response += 'info: [ '
                #self.response += item.output
                lines = item.output.split('\n')
                for i in range(0, len(lines), 1):
                    if(i > 0):
                        self.response += '\t'
                    self.response += lines[i]                    
                self.response += ' ]\n'
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
            self.response += '<td width="10%">'
            self.response += 'item'
            self.response += '</td>'
            self.response += '<td width="20%">'
            self.response += 'cmd'
            self.response += '</td>'
            self.response += '<td width="10%">'
            self.response += 'status'
            self.response += '</td>'
            self.response += '<td width="60%">'
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
                self.response += item.output
                self.response += '</td>'
                self.response += '</tr>'
            self.response += '</table>'
        else:
            self.response += 'unsupport detail: %d\n' % (detail)   
        
        request.write(self.response)
            
        return 0
