# -*- coding: utf-8 -*-
import os
from collections import defaultdict

from elasticsearch import Elasticsearch
from settings.settings_source_code import body_settings_sourcecode
from settings_generic import body_settings_generic

config = defaultdict()
config['DEST_PATH'] = os.environ.get('DEST_PATH') or "."
config['ES_HOST'] = os.environ.get('ES_HOST') or 'localhost'
config['ES_PORT'] = os.environ.get('ES_PORT') or '9200'
config['ES_USER'] = os.environ.get('ES_USER') or 'admin'
config['ES_PASSWORD'] = os.environ.get('ES_PASSWORD') or 'pass'
config['ES_USE_SSL'] = os.environ.get('ES_USE_SSL') == "True"
config['ES_SOURCECODE_INDEX'] = os.environ.get('ES_SOURCECODE_INDEX') or 'sourcecode'
config['ES_TAGCLOUD_INDEX'] = os.environ.get('ES_TAGCLOUD_INDEX') or 'tagcloud'

if config['ES_USE_SSL']:
    config['ES_URL'] = "https://{0}:{1}".format(config['ES_HOST'], config['ES_PORT'])
else:
    config['ES_URL'] = "http://{0}:{1}".format(config['ES_HOST'], config['ES_PORT'])


config['INDEXES'] = defaultdict()


es = Elasticsearch(
    hosts=[{'host': config['ES_HOST'], 'port': config['ES_PORT']}],
    http_auth=(config['ES_USER'], config['ES_PASSWORD']),
    use_ssl=config['ES_USE_SSL'],
    verify_certs=False
)

config['es'] = es

job_sourcecode = {"index-pattern": config['ES_SOURCECODE_INDEX'], "settings": body_settings_sourcecode, "prefix": "SOURCECODE__",
                 "namespace": "default", "date_field": "date_modified", "description": "Source Code", "module_name": "ElkEtlPythonCode",
                 "class_name": "ElkEtlPythonCode", "kibana_date_format": "yyyy-MM-dd HH:mm:ss",
                 "src_path": "../data"}

job_tagcloud = {"index-pattern": config['ES_TAGCLOUD_INDEX'], "settings": body_settings_generic, "prefix": "TAGCLOUD__",
                 "namespace": "default", "description": "Tag Cloud", "module_name": "ElkEtlTagCloud",
                 "class_name": "ElkEtlTagCloud", "kibana_date_format": "yyyy-MM-dd HH:mm:ss",
                 "es": es}

config['INDEXES']['job_sourcecode'] = job_sourcecode
config['INDEXES']['job_tagcloud'] = job_tagcloud
