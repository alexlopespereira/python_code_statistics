import datetime
from pathlib import Path
import os
import re

from etlelk.etlbase import EtlBase


class EtlPythonCode(EtlBase):

    def __init__(self, config, job_description, limit=1000):
        super().__init__(config, job_description, limit=limit)
        self.src_path = job_description['src_path']
        self.all_filenames = [i for i in Path(self.src_path).rglob('*.py')]
        self.limit = 50

    def load_results(self):
        # if self.offset > 500:
        #     return None

        datalist = []
        curr_limit = min(self.offset+self.limit, len(self.all_filenames))
        for f in self.all_filenames[self.offset:curr_limit]:
            with open(f, 'r') as file:
                string = file.read()
                string = re.sub(r"#.*\n", r" ", string)
                string = string.replace("\n", " ").replace("\\", "")
                string = re.sub(r'([\'"])((?:(?!\1).)*)\1', " ", string, flags=re.MULTILINE)
                date_modified = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M:%S")

                datalist.append({"sourcecode": string, "filename": os.path.basename(f), "path": os.path.abspath(f), "date_modified": date_modified})

        return datalist
