# from run_etl_jobs import *
# from config import Config
# from kibanafunctions import KibanaFunctions
from time import sleep

from etlelk import KibanaFunctions
from etlelk.run_etl_jobs import run_etl_job

from src.config import Config

config = Config()
kf = KibanaFunctions(config)
# kf.download_all()
# kf.upload_files_replacing_index_id()
kf.els.delete_index(config.es, config.INDEXES[0]['index'])
run_etl_job(config, config.INDEXES[0])
sleep(2)

kf.els.delete_index(config.es, config.INDEXES[1]['index'])
run_etl_job(config, config.INDEXES[1])
