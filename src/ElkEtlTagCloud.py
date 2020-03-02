from ElkEtlBase import ElkEtlBase


class ElkEtlTagCloud(ElkEtlBase):

    def __init__(self, job_description, limit=1000):
        super().__init__(job_description, limit=limit)
        self.es = job_description['es']
        self.src_index = "sourcecode"
        self.loaded = False

    def load_results(self):
        if self.loaded:
            return None

        query = """{
            "size": 0,
            "aggregations" : {
                "tagcloud" : {
                    "terms" : { "field" : "sourcecode", "size" : 100  }
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
