# Author: Omkar Pathak

import os
import utils
import spacy
import pprint
from spacy.matcher import Matcher

class ResumeParser(object):
    def __init__(self, resume):
        nlp = spacy.load('en_core_web_sm')
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name'         : None,
            'email'        : None,
            'mobile_number': None,
            'skills'       : None,
            'education'    : None,
        }
        self.__resume      = resume
        self.__text        = utils.extract_text(self.__resume, os.path.splitext(self.__resume)[1])
        self.__text        = ' '.join(self.__text.split())
        self.__nlp         = nlp(self.__text)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        name   = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email  = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text)
        skills = utils.extract_skills(self.__nlp, self.__noun_chunks)
        edu    = utils.extract_education([sent.string.strip() for sent in self.__nlp.sents])
        self.__details['name'] = name
        self.__details['email'] = email
        self.__details['mobile_number'] = mobile
        self.__details['skills'] = skills
        self.__details['education'] = edu
        return

if __name__ == '__main__':
    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    for resume in resumes:
        obj = ResumeParser(resume)
        data.append(obj.get_extracted_data())
        del obj

    pprint.pprint(data)