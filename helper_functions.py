import os
from datetime import datetime

def generate_content_name(name: str) -> str:
    """ Generate unique name for content folder based on name and current time """
    
    return os.path.join(
        "generated_content", 
        name + "_" +  datetime.now().strftime("%m%d%Y_%H%M")
    )