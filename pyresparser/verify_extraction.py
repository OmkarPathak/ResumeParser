import os
import shutil
from pyresparser.resume_parser import ResumeParser
import pprint

# Move model if exists
if os.path.exists("pyresparser_model/model-best"):
    model_dest = os.path.join("pyresparser", "model")
    if os.path.exists(model_dest):
        shutil.rmtree(model_dest)
    shutil.copytree("pyresparser_model/model-best", model_dest)
    print(f"Model moved to {model_dest}")

def verify(resume_path):
    print(f"Parsing {resume_path}...")
    try:
        data = ResumeParser(resume_path).get_extracted_data()
        print("\nFull Data:")
        pprint.pprint(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    for root, directories, filenames in os.walk('resumes/'):
        for filename in filenames:
            file = os.path.join(root, filename)
            verify(file)
    # verify("OmkarResume.pdf")
            
