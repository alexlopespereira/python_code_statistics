import os
from collections import defaultdict
from elasticsearch import Elasticsearch
from etlelk.configbase import ConfigBase
from etlelk.settings_generic import body_settings_generic
from settings.settings_source_code import body_settings_sourcecode


class Config(ConfigBase):
    DEST_PATH = os.environ.get('DEST_PATH') or "../saved_objects"
    KIBANA_HOST = os.environ.get('KIBANA_HOST') or 'localhost'
    KIBANA_PORT = os.environ.get('KIBANA_PORT') or '5601'
    KIBANA_DEST_HOST = os.environ.get('KIBANA_DEST_HOST') or 'localhost'
    KIBANA_DEST_PORT = os.environ.get('KIBANA_DEST_PORT') or '5601'
    ES_HOST = os.environ.get('ES_HOST') or 'localhost'
    ES_PORT = os.environ.get('ES_PORT') or '9200'
    ES_USER = os.environ.get('ES_USER') or 'admin'
    ES_PASSWORD = os.environ.get('ES_PASSWORD') or 'pass'
    ES_USE_SSL = os.environ.get('ES_USE_SSL') == "True"
    ES_SOURCECODE_INDEX = os.environ.get('ES_SOURCECODE_INDEX') or 'sourcecode__sourcecode'
    ES_TAGCLOUD_INDEX = os.environ.get('ES_TAGCLOUD_INDEX') or 'tagcloud__tagcloud'

    if ES_USE_SSL:
        ES_URL = "https://{0}:{1}".format(ES_HOST, ES_PORT)
        KIBANA_URL = "https://{0}:{1}".format(KIBANA_HOST, KIBANA_PORT)
        KIBANA_DEST_URL = "https://{0}:{1}".format(KIBANA_HOST, KIBANA_PORT)
    else:
        ES_URL = "http://{0}:{1}".format(ES_HOST, ES_PORT)
        KIBANA_URL = "http://{0}:{1}".format(KIBANA_HOST, KIBANA_PORT)
        KIBANA_DEST_URL = "http://{0}:{1}".format(KIBANA_HOST, KIBANA_PORT)

    INDEXES = []
    
    
    es = Elasticsearch(
        hosts=[{'host': ES_HOST, 'port': ES_PORT}],
        http_auth=(ES_USER, ES_PASSWORD),
        use_ssl=ES_USE_SSL,
        verify_certs=False
    )

    job_sourcecode = {"index": ES_SOURCECODE_INDEX, "settings": body_settings_sourcecode, "prefix": "sourcecode__",
                     "date_field": "date_modified", "description": "Source Code", "module_name": "etlpythoncode",
                     "class_name": "EtlPythonCode", "kibana_date_format": "yyyy-MM-dd HH:mm:ss",
                     "src_path": "../data"}
    
    job_tagcloud = {"index": ES_TAGCLOUD_INDEX, "settings": body_settings_generic, "prefix": "tagcloud__",
                     "description": "Tag Cloud", "module_name": "etltagcloud",
                     "class_name": "EtlTagCloud", "kibana_date_format": "yyyy-MM-dd HH:mm:ss",
                     "es": es}
    
    INDEXES = [job_sourcecode, job_tagcloud]
