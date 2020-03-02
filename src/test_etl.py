from config_elastic import config
from deploy_kibana import replace_id_upload_files
from elasticsearch_functions import delete_index
from run_etl_jobs import *


delete_index(config['es'], config['INDEXES']['job_sourcecode']['index-pattern'])
delete_index(config['es'], config['INDEXES']['job_tagcloud']['index-pattern'])

run_etl_job(config['INDEXES']['job_sourcecode'])
run_etl_job(config['INDEXES']['job_tagcloud'])

# run_all_etls(INDEXES)

# replace_id_upload_files()
