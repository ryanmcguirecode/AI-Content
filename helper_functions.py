import os
from datetime import datetime

def generate_content_name(name: str) -> str:
    return os.path.join("generated_content", name + "_" +  datetime.now().strftime("%m%d%Y_%H%M"))