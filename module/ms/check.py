#!../tools/python27/bin/python
#-*- coding:utf-8 -*-
import commands;

class check:
    response = ''
    
    def exec_cmd(self, cmd):
	result = 0
        try:            
            (status, output) = commands.getstatusoutput(cmd)
            print 'cmd:\t', cmd
            self.response += 'cmd:\t'
            self.response += cmd
            self.response += '\n'
            print 'status:\t', status
            self.response += 'status:\t'
            self.response += str(status)
            self.response += '\n'
            print 'output:\n', output
            self.response += 'output:\n'
            self.response += output
            self.response += '\n'
        except:
            result = -1
        finally:
            return result
    
    def start(self,request):
        result = 0
        self.response = ''
        try: 
            #output_dic=request.args
            #print 'output_dic:\n',output_dic
            #request.write(str(output_dic))
            self.exec_cmd('ps -ef|grep mediaserver')
            self.exec_cmd('netstat -tlnp')            
            self.exec_cmd('iptables -L -n')
            self.exec_cmd('cat /proc/`/sbin/pidof mediaserver`/limits|grep \"open files\"')
            self.exec_cmd('cat /home/mediaserver/etc/ms.conf | grep load_hvod_module')
            self.exec_cmd('cat /home/mediaserver/etc/ms.conf | grep speed_peer_upload_limit')
            self.exec_cmd('cat /home/mediaserver/etc/ms.conf | grep -E \"hvod_peer_max_speed|hvod_dld_max_speed|hvod_mp4head_max_speed|hvod_speed_fresh_interval|hvod_max_pending_package|hvod_free_speed_pos\"')
            self.exec_cmd('cat /home/mediaserver/etc/ms.conf | grep accepter_thread_num')
            self.exec_cmd('cat /home/mediaserver/etc/ms.conf | grep service_devices | grep -v service_devices_reload_interval')
            request.write(self.response)
        except:
            result = -1
        finally:
            return result
