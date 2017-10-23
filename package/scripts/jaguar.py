# -*- coding: utf-8 -*-
import os
import base64
from time import sleep
from resource_management import *

class JAGUARMaster(Script):
    
    def install(self, env):      
        import params
        env.set_params(params)
        self.install_packages(env)
        #install go
        Execute('cd /tmp; wget ' + params.godownloadlocation + ' -O go.tar.gz;tar -C /usr/local -xzf go.tar.gz;')
        Directory([params.install_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.install_dir + '; wget ' + params.downloadlocation + ' -O astrodb.tar.gz  ')
        Execute('cd ' + params.install_dir + '; tar -xvf astrodb.tar.gz')
        Execute('cd ' + params.install_dir + ';rm -rf latest; ln -s astrodb latest')         

    def configure(self, env):  
        import params
        env.set_params(params)
        print "config"

    def start(self, env):
        import params
        env.set_params(params)
        
        self.configure(env)
        Execute(format("export PATH=$PATH:/usr/local/go/bin;cd {install_dir}/latest/jaguar-go/bin && nohup ./jaguar > ../log/jaguar_run.log 2>&1 &"))        
        Execute("rm -rf /etc/jaguar.pid;pidof ./jaguar | cut -d ' ' -f 1 >> /etc/jaguar.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(format("cat /etc/jaguar.pid|xargs kill -9 "), ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/etc/jaguar.pid")


if __name__ == "__main__":
    JAGUARMaster().execute()
