#!../tools/python27/bin/python
#-*- coding:utf-8 -*-
import string
import commands;

class check_item:
    name    = ''
    cmd     = ''
    status  = 0
    output  = ''
    expect  = ''
    get     = ''
    result  = ''
    func    = None
    
    def __init__(self, name, cmd, status, output, expect, get, result, func):
        self.name = name
        self.cmd = cmd
        self.status = status
        self.output = output
        self.expect = expect
        self.get = get
        self.result = result
        self.func = func


class check:
    NAME_1 = 'process'
    NAME_2 = 'listen'
    NAME_3 = 'iptables'
    NAME_4 = 'limit'
    NAME_5 = 'hvod'
    NAME_6 = 'upload'
    NAME_7 = 'speed'
    NAME_8 = 'thread'
    NAME_9 = 'disk'
    NAME_10 = 'log'    
    
    CMD_1 = 'ps -ef|grep mediaserver'
    CMD_2 = 'netstat -tlnp'
    CMD_3 = 'iptables -L -n'
    CMD_4 = 'cat /proc/`/sbin/pidof mediaserver`/limits|grep \"open files\"'
    CMD_5 = 'cat /home/mediaserver/etc/ms.conf | grep load_hvod_module'
    CMD_6 = 'cat /home/mediaserver/etc/ms.conf | grep speed_peer_upload_limit'
    CMD_7 = 'cat /home/mediaserver/etc/ms.conf | grep -E \"hvod_peer_max_speed|hvod_dld_max_speed|hvod_mp4head_max_speed|hvod_speed_fresh_interval|hvod_max_pending_package|hvod_free_speed_pos\"'
    CMD_8 = 'cat /home/mediaserver/etc/ms.conf | grep accepter_thread_num'
    CMD_9 = 'cat /home/mediaserver/etc/ms.conf | grep service_devices | grep -v service_devices_reload_interval'
    CMD_10 = 'ls -l /root/clean_log.sh 2>/dev/null | wc -l; ls -l /home/mediaserver/log/peer_????????.log 2>/dev/null | wc -l; ls -l /home/mediaserver/log/peer_hvod_????????.log 2>/dev/null | wc -l'
    
#     items = [ \
#                check_item(NAME_1, CMD_1, 0, '', '', '', '', check_cmd_1), \
#                check_item(NAME_2, CMD_2, 0, '', '', '', '', check_cmd_2), \
#                check_item(NAME_3, CMD_3, 0, '', '', '', '', check_cmd_3), \
#                check_item(NAME_4, CMD_4, 0, '', '', '', '', check_cmd_4), \
#                check_item(NAME_5, CMD_5, 0, '', '', '', '', check_cmd_5), \
#                check_item(NAME_6, CMD_6, 0, '', '', '', '', check_cmd_6), \
#                check_item(NAME_7, CMD_7, 0, '', '', '', '', check_cmd_7), \
#                check_item(NAME_8, CMD_8, 0, '', '', '', '', check_cmd_8), \
#                check_item(NAME_9, CMD_9, 0, '', '', '', '', check_cmd_9), \
#                check_item(NAME_10, CMD_10, 0, '', '', '', '', check_cmd_10), \
#               ]
                
    response = ''    
 
    
    def check_cmd_1(self, item):        
        STRING1 = './daemon' #'./daemon mediaserver'
        STRING2 = 'mediaserver'
                
        num1 = 0
        num2 = 0
        numx = 0
                
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split()    
            if(len(values) < 8):
                continue        
            if(cmp(values[7], STRING1) == 0):
                num1 = num1 + 1
            elif(cmp(values[7], STRING2) == 0):
                num2 = num2 + 1 
            else:
                numx = numx + 1  
                
        item.expect = '[%d] %s \n[%d] %s' % (1, STRING1, 1, STRING2)    
        item.get = '[%d] %s \n[%d] %s' % (num1, STRING1, num2, STRING2)
        
        if(num1 == 1) and (num2 == 1):
            item.result = 'ok'      
        else:           
            item.result = 'error'
            
        return 0         


    def check_cmd_2(self, item):        
        STRING1 = '0.0.0.0:6601'
        STRING2 = '0.0.0.0:843'
        STRING3 = '0.0.0.0:80'
        STRING4 = '0.0.0.0:6261'
        STRING5 = '0.0.0.0:8888'
        
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0        
        numx = 0             
                       
        lines = item.output.split('\n')            
        for line in lines:            
            #print 'line', line
            values = line.split()
            if(len(values) < 4):
                continue
            #print 'values[3]', values[3]
            if(cmp(values[3], STRING1) == 0):
                num1 = num1 + 1
            elif(cmp(values[3], STRING2) == 0):
                num2 = num2 + 1 
            elif(cmp(values[3], STRING3) == 0):
                num3 = num3 + 1
            elif(cmp(values[3], STRING4) == 0):
                num4 = num4 + 1
            elif(cmp(values[3], STRING5) == 0):
                num5 = num5 + 1
            else:
                numx = numx + 1
    
        item.expect = '[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s' % (1, STRING1, 1, STRING2, 1, STRING3, 1, STRING4, 1, STRING5)
        item.get = '[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s' % (num1, STRING1, num2, STRING2, num3, STRING3, num4, STRING4, num5, STRING5)
        
        if(num1 == 1) and (num2 == 1) and (num3 == 1) and (num4 == 1) and (num5 == 1):
            item.result = 'ok'      
        else:
            item.result = 'error'
        
        return 0
    
        
    def check_cmd_3(self, item):
        TCP = 'tcp'
        
        STRING1  = 'dpt:6601'
        STRING2  = 'spt:6601'
        STRING3  = 'dpt:843'
        STRING4  = 'spt:843'
        STRING5  = 'dpt:80'
        STRING6  = 'spt:80'
        STRING7  = 'dpt:6261'
        STRING8  = 'spt:6261'
        STRING9  = 'dpt:8888'
        #STRING10 = 'spt:8888'
        STRING10 = 'spt:7000'
        STRING11 = 'spt:7003'
        STRING12 = 'spt:7010'
        STRING13 = 'spt:8000'
        STRING14 = 'spt:8080'
        STRING15 = 'spt:9000'
                
        num1  = 0
        num2  = 0
        num3  = 0
        num4  = 0
        num5  = 0        
        num6  = 0
        num7  = 0
        num8  = 0
        num9  = 0
        num10 = 0
        num11 = 0
        num12 = 0
        num13 = 0
        num14 = 0
        num15 = 0   
        numx  = 0     
                      
        lines = item.output.split('\n')            
        for line in lines:            
            #print 'line', line
            values = line.split()
            if(len(values) < 7):
                continue
            if(cmp(values[5], TCP) != 0):
                continue
            #print 'values[5]', values[5], 'values[6]', values[6]            
            if(cmp(values[6], STRING1) == 0):
                num1 = num1 + 1
            elif(cmp(values[6], STRING2) == 0):
                num2 = num2 + 1 
            elif(cmp(values[6], STRING3) == 0):
                num3 = num3 + 1
            elif(cmp(values[6], STRING4) == 0):
                num4 = num4 + 1
            elif(cmp(values[6], STRING5) == 0):
                num5 = num5 + 1
            elif(cmp(values[6], STRING6) == 0):
                num6 = num6 + 1 
            elif(cmp(values[6], STRING7) == 0):
                num7 = num7 + 1
            elif(cmp(values[6], STRING8) == 0):
                num8 = num8 + 1
            elif(cmp(values[6], STRING9) == 0):
                num9 = num9 + 1
            elif(cmp(values[6], STRING10) == 0):
                num10 = num10 + 1
            elif(cmp(values[6], STRING11) == 0):
                num11 = num11 + 1
            elif(cmp(values[6], STRING12) == 0):
                num12 = num12 + 1
            elif(cmp(values[6], STRING13) == 0):
                num13 = num13 + 1
            elif(cmp(values[6], STRING14) == 0):
                num14 = num14 + 1
            elif(cmp(values[6], STRING15) == 0):
                num15 = num15 + 1
            else:
                numx = numx + 1  
        
        item.expect = '[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s' \
            % (1, STRING1, 1, STRING2, 1, STRING3, 1, STRING4, 1, STRING5, 1, STRING6, 1, STRING7, 1, STRING8, 1, STRING9, 1, STRING10, 1, STRING11, 1, STRING12, 1, STRING13, 1, STRING14, 1, STRING15) 
            
        item.get = '[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s \n[%d] %s' \
            % (num1, STRING1, num2, STRING2, num3, STRING3, num4, STRING4, num5, STRING5, num6, STRING6, num7, STRING7, num8, STRING8, num9, STRING9, num10, STRING10, num11, STRING11, num12, STRING12, num13, STRING13, num14, STRING14, num15, STRING15)            
        if(num1 == 1) and (num2 == 1) and (num3 == 1) and (num4 == 1) and (num5 == 1) and (num6 == 1) and (num7 == 1) and (num8 == 1) and (num9 == 1) and (num10 == 1) and (num11 == 1) and (num12 == 1) and (num13 == 1) and (num14 == 1) and (num15 == 1):
            item.result = 'ok'      
        else: 
            item.result = 'error'
            
        return 0
    
        
    def check_cmd_4(self, item):
        #output = 'Max open files            102400               102400               files'
        KEY1 = 'Max'
        KEY2 = 'open'
        KEY3 = 'files'
        VALUE1  = '102400'
        VALUE2  = '102400'
        
        num1 = 0
        numx = 0
                        
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split()    
            if(len(values) < 6):
                continue        
            key1 = values[0].strip()
            key2 = values[1].strip()
            key3 = values[2].strip()
            value1 = values[3].strip()
            value2 = values[4].strip()
            #print 'key', key1, key2, key3, 'value1', value1, 'value2', value2
            if(cmp(key1, KEY1) == 0) and (cmp(key2, KEY2) == 0) and (cmp(key3, KEY3) == 0) and (cmp(value1, VALUE1)==0) and (cmp(value2, VALUE2)==0):
                num1 = num1 + 1
            else:
                numx = numx + 1  
        
        item.expect = 'Max open files            102400               102400               files'
        item.get = item.output
        
        if(num1 == 1):
            item.result = 'ok'      
        else:            
            item.result = 'error'
              
        return 0  
         
        
    def check_cmd_5(self, item):
        #output = 'load_hvod_module = 1'
        KEY1 = 'load_hvod_module'
        VALUE1 = '1'
        
        num1 = 0
        numx = 0            
                        
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split('=')    
            if(len(values) < 2):
                continue        
            key = values[0].strip()
            value = values[1].strip()
            #print 'key', key, 'value', value
            if(cmp(key, KEY1) == 0) and (cmp(value, VALUE1)==0):
                num1 = num1 + 1
            else:
                numx = numx + 1  
        
        item.expect = 'load_hvod_module = 1'
        item.get = item.output
        
        if(num1 == 1):
            item.result = 'ok'      
        else:
            item.result = 'error'
            
        return 0    
               
       
    def check_cmd_6(self, item):
        #output = 'speed_peer_upload_limit = 25600'
        KEY1 = 'speed_peer_upload_limit'
        VALUE1 = '25600'
        
        num1 = 0
        numx = 0
                        
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split('=')    
            if(len(values) < 2):
                continue        
            key = values[0].strip()
            value = values[1].strip()
            #print 'key', key, 'value', value
            if(cmp(key, KEY1) == 0) and (cmp(value, VALUE1)==0):
                num1 = num1 + 1
            else:
                numx = numx + 1  
        
        item.expect = 'speed_peer_upload_limit = 25600'
        item.get = item.output
        
        if(num1 == 1):
            item.result = 'ok'      
        else:
            item.result = 'error'  
            
        return 0
       
  
    def check_cmd_7(self, item):
#         output = '''
#             hvod_peer_max_speed = -1\n
#             hvod_dld_max_speed = -1\n
#             hvod_mp4head_max_speed = -1\n
#             hvod_speed_fresh_interval = 1\n
#             hvod_max_pending_package = 1\n
#             hvod_free_speed_pos = -1\n
#         '''
        
        KEY1 = 'hvod_peer_max_speed'
        VALUE1 = '-1'
        KEY2 = 'hvod_dld_max_speed'
        VALUE2 = '-1'
        KEY3 = 'hvod_mp4head_max_speed'
        VALUE3 = '-1'
        KEY4 = 'hvod_speed_fresh_interval'
        VALUE4 = '1'
        KEY5 = 'hvod_max_pending_package'
        VALUE5 = '1'
        KEY6 = 'hvod_free_speed_pos'
        VALUE6 = '-1'
        
        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0
        numx = 0
                        
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split('=')    
            if(len(values) < 2):
                continue        
            key = values[0].strip()
            value = values[1].strip()
            #print 'key', key, 'value', value
            if(cmp(key, KEY1) == 0) and (cmp(value, VALUE1)==0):
                num1 = num1 + 1
            elif(cmp(key, KEY2) == 0) and (cmp(value, VALUE2)==0):
                num2 = num2 + 1
            elif(cmp(key, KEY3) == 0) and (cmp(value, VALUE3)==0):
                num3 = num3 + 1
            elif(cmp(key, KEY4) == 0) and (cmp(value, VALUE4)==0):
                num4 = num4 + 1
            elif(cmp(key, KEY5) == 0) and (cmp(value, VALUE5)==0):
                num5 = num5 + 1
            elif(cmp(key, KEY6) == 0) and (cmp(value, VALUE6)==0):
                num6 = num6 + 1
            else:
                numx = numx + 1  
        
        item.expect = '''\
            hvod_peer_max_speed = -1
            hvod_dld_max_speed = -1
            hvod_mp4head_max_speed = -1
            hvod_speed_fresh_interval = 1
            hvod_max_pending_package = 1
            hvod_free_speed_pos = -1'''
        item.get = item.output
        
        if(num1 == 1) and (num2==1) and (num3==1) and (num4==1) and (num5==1) and (num6==1):
            item.result = 'ok'      
        else:
            item.result = 'error' 
            
        return 0
                
            
    def check_cmd_8(self, item):
        #output = 'accepter_thread_num=32'
        KEY1 = 'accepter_thread_num'
        VALUE1 = '32'
        
        num1 = 0
        numx = 0
                        
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split('=')    
            if(len(values) < 2):
                continue        
            key = values[0].strip()
            value = values[1].strip()
            #print 'key', key, 'value', value
            if(cmp(key, KEY1) == 0) and (cmp(value, VALUE1)==0):
                num1 = num1 + 1
            else:
                numx = numx + 1  
        
        item.expect = 'accepter_thread_num=32'
        item.get = item.output
        
        if(num1 == 1):
            item.result = 'ok'      
        else:
            item.result = 'error'
            
        return 0
      
        
    def check_cmd_9(self, item):
        #service_devices = /media1 /media2 /media3 /media4 /media5
        KEY1 = 'service_devices'
      
        lines = item.output.split('\n')            
        for line in lines:
            #print 'line', line
            values = line.split('=')    
            if(len(values) < 2):
                continue        
            key = values[0].strip()
            value = values[1].strip()
            #print 'key', key, 'value', value
            if(cmp(key, KEY1) == 0) and (len(value) > 0):
                item.get = value  
        
        df_cmd = "df -ah | grep /media | awk '{print $6}'"
        (status, output) = commands.getstatusoutput(df_cmd)
        item.expect = output
        
        disks = item.expect.split('\n')
        dirs = item.get.split()   
        
        item.result = 'ok' 
        
        num1 = len(disks)
        num2 = len(dirs)
        if(num1 != num2):
            item.result = 'error'        
            return -1
        
        for disk in disks:
            if disk not in dirs:  
                item.result = 'error' 
                return -1
        
        return 0
    
    
    def check_cmd_10(self, item):   
        item.expect = '%d\n%d\n%d\n' % (1, 7, 7)    
        item.get = item.output
           
        lines = item.output.split('\n')            
        if(len(lines) <= 3):
            item.result= 'error'
            return -1
        clean_log_sh = lines[0]
        peer_log     = lines[1]
        peer_hvod_log  = lines[2]
        
        num1 = string.atoi(clean_log_sh) 
        num2 = string.atoi(peer_log) 
        num3 = string.atoi(peer_hvod_log) 
        
        item.result = 'ok'
        
        if(num1 != 1):
            item.result = 'error'
            return -1
            
        if(num2 > 8):
            item.result = 'error'
            return -1
        
        if(num3 > 8):
            item.result = 'error'
            return -1
        
        return 0
    
        
    def check_output(self, item):
        result = 0
        try:
            if(cmp(item.cmd, self.CMD_1) == 0):
                self.check_cmd_1(item)
            elif(cmp(item.cmd, self.CMD_2) == 0):
                self.check_cmd_2(item)
            elif(cmp(item.cmd, self.CMD_3) == 0):
                self.check_cmd_3(item)
            elif(cmp(item.cmd, self.CMD_4) == 0):
                self.check_cmd_4(item)
            elif(cmp(item.cmd, self.CMD_5) == 0):
                self.check_cmd_5(item)
            elif(cmp(item.cmd, self.CMD_6) == 0):
                self.check_cmd_6(item)
            elif(cmp(item.cmd, self.CMD_7) == 0):
                self.check_cmd_7(item)
            elif(cmp(item.cmd, self.CMD_8) == 0):
                self.check_cmd_8(item)
            elif(cmp(item.cmd, self.CMD_9) == 0):
                self.check_cmd_9(item)
            else:
                item.result = 'unknown cmd'
        except:
            result = -1
        finally:
            return result
        
    
    items = [ \
               check_item(NAME_1, CMD_1, 0, '', '', '', '', check_cmd_1), \
               check_item(NAME_2, CMD_2, 0, '', '', '', '', check_cmd_2), \
               check_item(NAME_3, CMD_3, 0, '', '', '', '', check_cmd_3), \
               check_item(NAME_4, CMD_4, 0, '', '', '', '', check_cmd_4), \
               check_item(NAME_5, CMD_5, 0, '', '', '', '', check_cmd_5), \
               check_item(NAME_6, CMD_6, 0, '', '', '', '', check_cmd_6), \
               check_item(NAME_7, CMD_7, 0, '', '', '', '', check_cmd_7), \
               check_item(NAME_8, CMD_8, 0, '', '', '', '', check_cmd_8), \
               check_item(NAME_9, CMD_9, 0, '', '', '', '', check_cmd_9), \
               check_item(NAME_10, CMD_10, 0, '', '', '', '', check_cmd_10), \
              ]
    
    def check_item(self, item):
        result = 0
        try:            
            (status, output) = commands.getstatusoutput(item.cmd)
            item.status = status
            item.output = output
            #self.check_output(item)          
            item.func(self, item)            
        except:
            result = -1
        finally:
            return result
    
    def start(self, request):
        result = 0
        detail = 0
        self.response = ''
                
        try: 
            #output_dic=request.args
            #print 'output_dic:\n',output_dic
            #request.write(str(output_dic))
            if 'detail' in request.args:
                detail = string.atoi(request.args['detail'][0])               
            #self.response += 'detail: %d\n' % (detail)
            
            for i in range(0, len(self.items), 1):
                self.check_item(self.items[i])
                
            if(detail == 0):
                for i in range(0, len(self.items), 1):
                    self.response += 'item: '
                    self.response += self.items[i].name
                    self.response += '\t'
                    self.response += 'result: '
                    self.response += self.items[i].result
                    self.response += '\n' 
            elif(detail == 1):
                for i in range(0, len(self.items), 1):
                    self.response += 'item: '
                    self.response += self.items[i].name
                    self.response += '\n'
                    self.response += 'cmd: '
                    self.response += self.items[i].cmd
                    self.response += '\n'
                    self.response += 'status: '
                    self.response += str(self.items[i].status)
                    self.response += '\n'                    
                    self.response += 'result: '
                    self.response += self.items[i].result
                    self.response += '\n'  
                    self.response += 'output: \n'
                    self.response += self.items[i].output
                    self.response += '\n'
                    self.response += 'expect: \n'
                    self.response += self.items[i].expect
                    self.response += '\n'
                    self.response += 'get: \n'
                    self.response += self.items[i].get
                    self.response += '\n'                    
                    self.response += '\n' 
            elif(detail == 2):
                self.response += '<table border="1" style="table-layout:fixed;word-break: break-all; word-wrap: break-word;">'
                self.response += '<tr>'
                self.response += '<td width="4%">'
                self.response += 'item'
                self.response += '</td>'
                self.response += '<td width="18%">'
                self.response += 'cmd'
                self.response += '</td>'
                self.response += '<td width="4%">'
                self.response += 'status'
                self.response += '</td>'
                self.response += '<td width="4%">'
                self.response += 'result'
                self.response += '</td>'
                self.response += '<td width="30%">'
                self.response += 'output'
                self.response += '</td>'
                self.response += '<td width="20%">'
                self.response += 'expect'
                self.response += '</td>'
                self.response += '<td width="20%">'
                self.response += 'get'
                self.response += '</td>'
                self.response += '</tr>'
                for i in range(0, len(self.items), 1):
                    if(cmp(self.items[i].result, 'ok') == 0):
                        self.response += '<tr>'
                    else:
                        self.response += '<tr bgcolor=#AAAA00>'
                    self.response += '<td>'
                    self.response += self.items[i].name
                    self.response += '</td>'
                    self.response += '<td>'
                    self.response += self.items[i].cmd                    
                    self.response += '</td>'
                    self.response += '<td>'
                    self.response += str(self.items[i].status)
                    self.response += '</td>'                   
                    self.response += '<td>'
                    self.response += self.items[i].result
                    self.response += '</td>'
                    self.response += '<td>'
                    #self.response += self.items[i].output
                    lines = self.items[i].output.split('\n')
                    for line in lines:
                        self.response += line
                        self.response += '<br>'
                    self.response += '</td>'
                    self.response += '<td>'
                    #self.response += self.items[i].expect
                    lines = self.items[i].expect.split('\n')
                    for line in lines:
                        self.response += line
                        self.response += '<br>'
                    self.response += '</td>'
                    self.response += '<td>'
                    #self.response += self.items[i].get
                    lines = self.items[i].get.split('\n')
                    for line in lines:
                        self.response += line
                        self.response += '<br>'
                    self.response += '</td>'
                    self.response += '</tr>'
                self.response += '</table>\n'
            else:
                self.response += 'unsupport detail: %d\n' % (detail)      
                
            request.write(self.response)
        except:
            result = -1
        finally:
            return result
        
