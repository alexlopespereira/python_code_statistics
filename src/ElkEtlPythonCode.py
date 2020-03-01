import glob
from ElkEtlBase import ElkEtlBase


class ElkEtlPythonCode(ElkEtlBase):

    def __init__(self, job_description, limit=1000):
        super().__init__(job_description, limit=limit)
        self.src_path = job_description['src_path']

    def load_results(self):
        file_path_wildcard = '{0}/*.{1}'.format(self.src_path, "py")
        all_filenames = [i for i in glob.glob(file_path_wildcard)]
        datalist = []
        for f in all_filenames:
            with open(f, 'rb') as file:
                string = file.read()
                datalist.append(string)
