import os
import csv
from constants import CONTENT_TYPE_PARAMETERS as CTP
from generate_prompt import Prompt

class ContentParameters:
    def __init__(self, name: str, content_identifier: str):
        self.name = name
        self.content_identifier = content_identifier

        with open(os.path.join("content_settings", "parameters.csv"), "r") as f:
            reader = csv.reader(f)
            content_identifier_index = CTP.index("content_identifier")
            rows = [row for row in reader if row[content_identifier_index] == content_identifier]
            if len(rows) != 1:
                raise Exception("Invalid content identifier")
            for i, parameter in enumerate(CTP):
                exec("self." + parameter + " = '" + rows[0][i] + "'")