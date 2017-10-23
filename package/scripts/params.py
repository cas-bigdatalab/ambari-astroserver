from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
server_cnf_content=config['configurations']['astroserver']['content']
downloadlocation = config['configurations']['astroserver']['download.location']
godownloadlocation = config['configurations']['astroserver']['go.download.location']
install_dir = '/data/astrodb'
current_host_name = socket.gethostname()
redis_url = config['configurations']['astroserver']['redis.url']
master_node = config['clusterHostInfo']['cgwac_dbgen_master_hosts'][0]
