from config_elastic import config
from deploy_kibana import replace_id_upload_files
from run_etl_jobs import *


run_etl_job(config['INDEXES']['job_soucecode'])
# run_all_etls(INDEXES)

# replace_id_upload_files()
