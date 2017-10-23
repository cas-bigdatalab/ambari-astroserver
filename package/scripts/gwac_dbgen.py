# -*- coding: utf-8 -*-
import os
import base64
from time import sleep
from resource_management import *

class DBGENMaster(Script):
    
    def install(self, env):      
        import params
        env.set_params(params)
        print 'installed'
        File(format("{install_dir}/latest/gwac/abDetection.sh"),content=Template('abDetection.sh.j2'), mode=0o700)     

    def configure(self, env):  
        import params
        env.set_params(params)
        print "config"

    def start(self, env):
        import params
        env.set_params(params)
        
        self.configure(env)
        Execute(format("cd {install_dir}/latest/gwac/ && nohup ./abDetection.sh > dbgen.log 2>&1 &"))        

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(format("cat /etc/gwac_dbgen.pid|xargs kill -9 "), ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/etc/gwac_dbgen.pid")


if __name__ == "__main__":
    DBGENMaster().execute()
