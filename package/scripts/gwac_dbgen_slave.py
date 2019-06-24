# -*- coding: utf-8 -*-
import os
import base64
from time import sleep
from resource_management import *

class DBGENSlave(Script):
    
    def install(self, env):      
        import params
        env.set_params(params)
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

if __name__ == "__main__":
    DBGENSlave().execute()
