import os
import utils
import spacy
import pprint
from spacy.matcher import Matcher

class ResumeParse(object):
    def __init__(self, resume):
        nlp = spacy.load('en_core_web_sm')
        self.__matcher = matcher = Matcher(nlp.vocab)
        self.__details = {
            'name'         : None,
            'email'        : None,
            'mobile_number': None
        }
        self.__resume = resume
        self.__text   = utils.extract_text(self.__resume)
        self.__text   = ' '.join(self.__text.split())
        self.__nlp    = nlp(self.__text)
        self.__get_basic_details()

    def __repr__(self):
        pprint.pprint(self.__details)
        return 'Done'

    def __get_basic_details(self):
        name   = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email  = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text)
        self.__details['name'] = name
        self.__details['email'] = email
        self.__details['mobile_number'] = mobile
        return

if __name__ == '__main__':
    directory = os.listdir('resumes')
    resumes = []
    os.chdir('resumes')
    for file in directory:
        if os.path.splitext(file)[1] == '.pdf':
            resumes.append(file)
    for resume in resumes:
        obj = ResumeParse(resume)
        print(obj)
        del obj