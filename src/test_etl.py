from run_etl_jobs import *
from config import Config
from kibanafunctions import KibanaFunctions


config = Config()
kf = KibanaFunctions(config)
# kf.download_all()
kf.upload_files_replacing_index_id()
# kf.els.delete_index(config.es, config.INDEXES[0]['index'])
# kf.els.delete_index(config.es, config.INDEXES[1]['index'])
#
# run_etl_job(config, config.INDEXES[0])
# run_etl_job(config, config.INDEXES[1])

# run_all_etls(INDEXES)

# replace_id_upload_files()
