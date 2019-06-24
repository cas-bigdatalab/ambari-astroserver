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
        Directory(["/data/"],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute("pip install pyfits==3.3 numpy astropy==2.0.7 scipy", ignore_failures=False)
        Execute("easy_install "+params.download_url+"/pywcs-1.12-py2.7-linux-x86_64.egg", ignore_failures=False)
        Execute("cd /data/;wget "+params.download_url+"/gwac.1807130845.tar.gz;tar -xzf gwac*.gz;rm -rf gwac.1807130845.tar.gz;ln -sf /data/gwac ~/gwac", ignore_failures=False)
        Execute("cd /tmp/;wget "+params.download_url+"/go1.10.3.linux-amd64.tar.gz;tar -C /usr/local -xzf /tmp/go1.10.3.linux-amd64.tar.gz;echo 'export PATH=$PATH:/usr/local/go/bin'>>~/.bashrc", ignore_failures=False)
        Execute("cd /tmp/;wget "+params.download_url+"/libsodium-1.0.13.tar.gz;tar -xzvf libsodium-1.0.13.tar.gz;cd libsodium-1.0.13;make && make install", ignore_failures=False)
        Execute("cd /tmp/;wget "+params.download_url+"/libzmq.e6f908.tar.gz;tar -xzvf libzmq.e6f908.tar.gz;cd libzmq;make && make install;ldconfig", ignore_failures=False)
        Execute("cd /tmp/;wget "+params.download_url+"/czmq.e6f908.tar.gz;tar -xzvf czmq.e6f908.tar.gz;cd czmq;make && make install;ldconfig", ignore_failures=False)
        Execute("echo export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib>>~/.bashrc", ignore_failures=False)

    def configure(self, env):
        import params
        env.set_params(params)
        server_cnf_config = InlineTemplate(params.server_cnf_config)
        server_cnf_nodehostname = InlineTemplate(params.server_cnf_nodehostname)
        File("/data/gwac/gwac_dbgen_cluster/config.sh", content=server_cnf_config)
        File("/data/gwac/gwac_dbgen_cluster/nodehostname", content=server_cnf_nodehostname)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        service_packagedir = params.service_packagedir
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')
        Execute(format("echo \"nohup {service_packagedir}/scripts/aserv_metric_send.sh {collector_host} {current_host_name} &\"|at now +1 min"))
        Execute("echo \"cd ~/gwac/gwac_dbgen_cluster/ && nohup ./sumLineAndDataSize.sh 10000 2>&1 >/dev/null &\"|at now +1 min");sleep(63)
        Execute("rm -rf /tmp/gwac_dbgen_cluster_master.pid;ps -ef | grep -v grep | grep sumLineAndDataSize.sh | awk '{print $2}'> /tmp/gwac_dbgen_cluster_master.pid")

    def stop(self, env):
        Execute("cd ~/gwac/gwac_dbgen_cluster/ && ./stopGen.sh force", ignore_failures=True)
        sleep(10)
        Execute("ps -ef|stopGen.sh |grep -v grep|cut -c 9-15|xargs kill -9 ", ignore_failures=True)
        cmd = format("ps -ef|grep aserv_metric_send.sh |grep -v grep|cut -c 9-15|xargs kill -9 ")
        Execute(cmd, ignore_failures=True)
        cmd = format("ps -ef|detectorMaster |grep -v grep|cut -c 9-15|xargs kill -9 ")
        Execute(cmd, ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/tmp/gwac_dbgen_cluster_master.pid")


if __name__ == "__main__":
    DBGENMaster().execute()
