from collections import defaultdict

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

        vecs = self.get_vecs()
        aggs = self.get_aggregations()

        data_list = []
        for a in aggs:
            data_list.append({"term": a['key'], "freq": vecs[a['key']]['term_freq'], "doc_count": a['doc_count'],
                              "count_times_freq": vecs[a['key']]['term_freq']*a['doc_count']})

        self.loaded = True
        return data_list

    def split(self, a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    def get_vecs(self):
        query = """{"size": 10000, "stored_fields": []}"""
        res = self.es.search(index=self.src_index, body=query)
        docs = {}
        for l in list(self.split(res['hits']['hits'], 10)):
            query_list = []
            for r in l:
                query_list.append(r['_id'])
            res2 = self.es.mtermvectors(index=self.src_index, ids=query_list, fields=["sourcecode"], payloads=False, positions=False, offsets=False)
            for doc in res2['docs']:
                if doc['term_vectors']:
                    for term in doc['term_vectors']['sourcecode']['terms']:
                        if term in docs.keys():
                            docs[term]['term_freq'] = docs[term]['term_freq'] + doc['term_vectors']['sourcecode']['terms'][term]['term_freq']
                        else:
                            docs[term] = doc['term_vectors']['sourcecode']['terms'][term]

        return docs

    def get_aggregations(self):

        query = """{
            "size": 0,
            "aggregations" : {
                "tagcloud" : {
                    "terms" : { "field" : "sourcecode", "size" : 5000  }
                }
            }
        }"""

        res = self.es.search(index=self.src_index, body=query)
        new_list = list(filter(lambda item: len(item['key']) > 1, res['aggregations']['tagcloud']['buckets']))
        for e in new_list:
            if len(e['key']) == 1:
                print(e['key'])
        return new_list
