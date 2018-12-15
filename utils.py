import io
import re
import spacy
import pandas as pd
import constants as cs
from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
 
def extract_text_by_page(pdf_path):
# https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()

def extract_text(pdf_path):
    text = ''
    for page in extract_text_by_page(pdf_path):
        text += ' ' + page

    return text

def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_name(nlp_text, matcher):
    pattern = [cs.NAME_PATTERN]
    
    matcher.add('NAME', None, *pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

def extract_mobile_number(text):
    # Found this complicated regex on : https://zapier.com/blog/extract-links-email-phone-regex/
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

def extract_skills(nlp_text):
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv("skills.csv") 
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    # extraced_doc = extract_text('Brendan_Herger_Resume.pdf')
    # extraced_doc = extract_text('atulsharma.pdf')
    extraced_doc = extract_text('resumes/anjali_resume.pdf')
    extraced_doc = ' '.join(extraced_doc.split())
    doc = nlp(extraced_doc)
    
    # POS
    # for i in doc:
    #     print(i, '=>', i.ent_)

    # Entities
    # labels = set([w.label_ for w in doc.ents]) 
    # for label in labels: 
    #     entities = [cleanup(e.string, lower=False) for e in doc.ents if label==e.label_] 
    #     entities = list(set(entities)) 
    #     print(label,entities)

    # Noun Chunks
    # for idx, sentence in enumerate(doc.sents):
    #     for noun in sentence.noun_chunks:
    #         print(f"sentence {idx+1} has noun chunk '{noun}'")

    # for ent in doc.ents:
    #     if ent.label_ == 'ORG':
    #         email = extract_email(ent.text)
    #         if email:
    #             print(email)
    #     print(ent.text, ent.label_)

    # print(extraced_doc)
    print(extract_name(doc, matcher))
    # print(extract_mobile_number(extraced_doc))

    # print(extract_email('Brendan HergerHergertarian.com'))