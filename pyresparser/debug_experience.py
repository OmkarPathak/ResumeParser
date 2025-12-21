from pyresparser import utils
from pyresparser.resume_parser import ResumeParser
import pprint

def debug_experience(resume_path):
    print(f"Debugging {resume_path}...")
    parser = ResumeParser(resume_path)
    raw_text = parser._ResumeParser__text_raw
    
    # Get the raw experience lines as the tool sees them
    experience_list = utils.extract_entity_sections_grad(raw_text).get('experience', [])
    
    print("\n--- Raw Experience Lines ---")
    for i, line in enumerate(experience_list):
        print(f"{i}: {repr(line)}")
    
    print("\n--- Extracted Sections ---")
    sections = utils.extract_experience_sections(raw_text)
    pprint.pprint(sections)

if __name__ == "__main__":
    debug_experience("OmkarResume.pdf")
