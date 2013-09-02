#!../tools/python27/bin/python
#-*- coding:utf-8 -*-

import os
import string
import commands
import urllib2

class ms_task:
    #1369126657:fsp:0:0:100:36527DB56AD93746F6DE7EA0F6F6A81188DE424A:1
    taskname    = ''
    protocol    = ''
    uploadrate  = 0
    peernumber  = 0
    process     = 0
    infohashid  = ''
    state       = 0
    
    file_num   = 0
    file_list  = ''
    status      = '*'
    
    def __init__(self, taskname, protocol, uploadrate, peernumber, process, infohashid, state):
        self.taskname   = taskname
        self.protocol   = protocol
        self.uploadrate = uploadrate
        self.peernumber = peernumber
        self.process    = process
        self.infohashid = infohashid
        self.state      = state
        
        
class disk_file:
    #/media1/36527DB56AD93746F6DE7EA0F6F6A81188DE424A.dat
    file_name   = ''
    file_path   = ''
    file_prefix = ''
    full_name   = ''
    
    task_num    = 0
    task_list   = ''
    
    def __init__(self, name, path):
        self.file_name  = name
        self.file_path  = path
        fields = name.split('.')
        self.file_prefix = fields[0]
        self.full_name = os.path.join(self.file_path, self.file_name)
        
    
class tasks:
    response = ''
    task_list = []
    file_list = []
        
    CMD_1 = "df -ah | grep /media | awk '{print $6}'"
    URL_1 = 'http://127.0.0.1:6261/macross/?cmd=enumtask'
    
    def get_ms_tasks(self):
        #(status, output) = commands.getstatusoutput(self.CMD_1)
        #if(status != 0):
        #    return -1
        
        f = urllib2.urlopen(self.URL_1)
        output = f.read()
        #print output

        lines = output.split('\n')
        if(len(lines) < 2):
            return -1

        #print 'lines[0]: ', lines[0]
        expect_str = 'return=ok'
        expect_len = len(expect_str)
        get_str = lines[0]
        get_len = len(get_str)
        #print 'expect_len: %d' % (expect_len)
        #print 'get_len: %d' % (get_len)        
        if(get_len < expect_len):
            return -1
        if(get_len >= expect_len) and (cmp(get_str[0:expect_len], expect_str) != 0):
            return -1
        
        result = lines[1]
        #print 'result: ', result
        results = result.split('=')
        if(len(results) < 2):
            return -1
        
        tasks = results[1]
        #print 'tasks: ', tasks
        task_list = tasks.split('|')
        for task in task_list:
            fields = task.split(':')
            if(len(fields) < 7):
                continue
            self.task_list.append(ms_task(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6]))
            
        return 0
    
            
    def get_dir_files(self, path):
        for item in os.listdir(path):
            subpath = os.path.join(path, item)
            if(os.path.isfile(subpath)):
                print 'path: ', path, 'file: ', item
                self.file_list.append(disk_file(item, path))
                
        return 0
    
            
    def get_disk_files(self):
        (status, output) = commands.getstatusoutput(self.CMD_1)
        if(status != 0):
            return -1       
        
        disks = output.split('\n')
        for disk in disks:
            print 'disk: ', disk
            self.get_dir_files(disk)
            
        return 0
    
        
    def query_file_by_hash(self, task):        
        url =   'http://127.0.0.1:6261/macross/?cmd=querytaskstate&infohashid=%s' % (task.infohashid)
        #return=ok
        #result=1369126657|0|0|1|/media2/36527DB56AD93746F6DE7EA0F6F6A81188DE424A.dat|fsp|100
        f = urllib2.urlopen(url)
        output = f.read()
        #print output

        lines = output.split('\n')
        if(len(lines) < 2):
            return 0

        #print 'lines[0]: ', lines[0]
        expect_str = 'return=ok'
        expect_len = len(expect_str)
        get_str = lines[0]
        get_len = len(get_str)
        #print 'expect_len: %d' % (expect_len)
        #print 'get_len: %d' % (get_len)        
        if(get_len < expect_len):
            return 0
        if(get_len >= expect_len) and (cmp(get_str[0:expect_len], expect_str) != 0):
            return 0
        
        result = lines[1]
        #print 'result: ', result
        results = result.split('=')
        if(len(results) < 2):
            return 0
        
        task_state = results[1]
        fields = task_state.split('|')
        if(len(fields) < 7):
            return 0
        
        file_path = fields[4]
        if(os.path.isfile(file_path)):
            task.file_num = 1
            task.file_list = file_path
            
        return task.file_num    
        
            
    def find_files_by_hash(self, task):        
        for one_file in self.file_list:
            if(one_file.file_prefix == task.infohashid):  
                if(one_file.task_num > 0):
                    one_file.task_list += '|'
                one_file.task_list += task.infohashid
                one_file.task_num += 1              
                if(task.file_num > 0):
                    task.file_list += '|'
                task.file_list += one_file.full_name
                task.file_num += 1
                       
        return task.file_num
    
    
    def tasks_minus_files(self):
        for task in self.task_list:
            num = self.find_files_by_hash(task)
            if(num != 1):
                task.status = '?'
            if(num == 0):
                num = self.query_file_by_hash(task)
            
        return 0
    
        
    def start(self, request):
        detail = 0
        self.response = ''
        
        if 'detail' in request.args:
            detail = string.atoi(request.args['detail'][0])
            
        self.get_ms_tasks()
        self.get_disk_files()
        self.tasks_minus_files()
        #self.files_minus_tasks()
        
        if(detail == 0):
            self.response += 'task_list: %d' % (len(self.task_list))
            self.response += '\n'
            self.response += 'file_list: %d' % (len(self.file_list))
            self.response += '\n'            
            self.response += '\n'            
            for task in self.task_list:
                if(task.status == '?'):
                    self.response += task.infohashid
                    self.response += ':'
                    self.response += str(task.file_num)
                    self.response += ':'
                    self.response += task.file_list
                    self.response += ':'
                    self.response += task.status
                    self.response += '\n'
            self.response += '\n'
            for one_file in self.file_list:
                if(one_file.task_num != 1):
                    self.response += one_file.full_name
                    self.response += ':'
                    self.response += str(one_file.task_num)
                    self.response += ':'
                    self.response += one_file.task_list
                    self.response += '\n'
        elif(detail == 1):
            self.response += 'task_list: %d' % (len(self.task_list))
            self.response += '\n'
            self.response += 'file_list: %d' % (len(self.file_list))
            self.response += '\n'            
            self.response += '\n'  
            for task in self.task_list:                
                self.response += task.infohashid
                self.response += ':'
                self.response += str(task.file_num)
                self.response += ':'
                self.response += task.file_list
                self.response += ':'
                self.response += task.status
                self.response += '\n'
            self.response += '\n'
            for one_file in self.file_list:
                self.response += one_file.full_name
                self.response += ':'
                self.response += str(one_file.task_num)
                self.response += ':'
                self.response += one_file.task_list
                self.response += '\n'
        else:
            self.response += 'unsupport detail: %d\n' % (detail)         
                  
        request.write(self.response)
        
        return 0
            
