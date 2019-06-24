from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket

# server configurations
config = Script.get_config()
download_url=config['configurations']['ASERV']['download_url']
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
server_cnf_config=config['configurations']['ASERV']['config']
server_cnf_nodehostname=config['configurations']['ASERV']['nodehostname']
current_host_name = socket.gethostname()
collector_host= config['clusterHostInfo']['metrics_collector_hosts'][0]
# redis_url = config['configurations']['astroserver']['redis.url']
# master_node = config['clusterHostInfo']['cgwac_dbgen_master_hosts'][0]