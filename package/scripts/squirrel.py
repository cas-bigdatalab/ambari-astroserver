# -*- coding: utf-8 -*-
import os
import base64
from time import sleep
from resource_management import *

class SquirrelMaster(Script):
    
    def install(self, env):      
        print 'installed'

    def configure(self, env):  
        import params
        env.set_params(params)
        print "config"

    def start(self, env):
        import params
        env.set_params(params)
        
        self.configure(env)
        Execute(format("cd {install_dir}/latest/gwac/ && nohup Squirrel_abDetect_test/Debug/Squirrel -times 100 -threadNumber 10 -redisHost {redis_url} -method plane -grid 4,4 -errorRadius 1.5 -searchRadius 50 -fitsHDU 3 -ref template_table/template -width 3016 -height 3016 -terminal > squirrel.log 2>&1 &"))        
        Execute("rm -rf /etc/Squirrel.pid;pidof Squirrel  | cut -d ' ' -f 1 >> /etc/Squirrel.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(format("cat /etc/Squirrel.pid|xargs kill -9 "), ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/etc/Squirrel.pid")


if __name__ == "__main__":
    SquirrelMaster().execute()
