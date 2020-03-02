from etlelk.etlbase import EtlBase


class EtlTagCloud(EtlBase):

    def __init__(self, config, job_description, limit=1000):
        super().__init__(config, job_description, limit=limit)
        self.es = job_description['es']
        self.src_index = "sourcecode__sourcecode"
        self.loaded = False

    def load_results(self):
        if self.loaded:
            return None
        query = """{
            "stored_fields": []
        }"""
        res = self.es.search(index=self.src_index, body=query)
        query_list = []
        for r in res['hits']['hits']:
            query_list.append(r['_id'])

        res2 = self.es.mtermvectors(index=self.src_index, ids=query_list, fields=["sourcecode"], payloads=False, positions=False)
        data_list = []
        for k, v in res2['docs'][0]['term_vectors']['sourcecode']['terms'].items():
            data_list.append({"term": k, "freq": v['term_freq']})

        self.loaded = True
        return data_list


    def load_results_bkp(self):
        if self.loaded:
            return None

        query = """{
            "size": 0,
            "aggregations" : {
                "tagcloud" : {
                    "terms" : { "field" : "sourcecode", "size" : 1000  }
                }
            }
        }"""

        res = self.es.search(index=self.src_index, body=query)
        self.loaded = True
        new_list = list(filter(lambda item: len(item['key']) > 1, res['aggregations']['tagcloud']['buckets']))
        for e in new_list:
            if len(e['key']) == 1:
                print(e['key'])
        return new_list
