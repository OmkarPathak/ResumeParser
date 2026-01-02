# Author: Omkar Pathak

import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils


class ResumeParser(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None,
        use_gliner_extraction=False
    ):
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model"))
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__use_gliner_extraction = use_gliner_extraction
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'college_name': None,
            'degree': None,
            'designation': None,
            'experience': None,
            'company_names': None,
            'no_of_pages': None,
            'total_experience': None,
        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        cust_ent = utils.extract_entities_wih_custom_model(
                            self.__custom_nlp
                        )
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills(
                    self.__nlp,
                    self.__noun_chunks,
                    self.__skills_file
                )
        # edu = utils.extract_education(
        #               [sent.text.strip() for sent in self.__nlp.sents]
        #       )
        entities = utils.extract_entity_sections_grad(self.__text_raw)

        # extract name
        try:
            self.__details['name'] = cust_ent['Name'][0]
        except (IndexError, KeyError):
            self.__details['name'] = name

        # extract email
        self.__details['email'] = email

        # extract mobile number
        self.__details['mobile_number'] = mobile

        # extract skills
        self.__details['skills'] = skills

        # extract college name
        try:
            self.__details['college_name'] = entities['College Name']
        except KeyError:
            pass

        # extract education Degree
        try:
            self.__details['degree'] = cust_ent['Degree']
        except KeyError:
            pass

        # extract designation
        try:
            self.__details['designation'] = cust_ent['Designation']
        except KeyError:
            pass

        # extract company names
        try:
            self.__details['company_names'] = cust_ent['Companies worked at']
        except KeyError:
            pass

        try:
            self.__details['experience'] = entities['experience']
            try:
                exp = round(
                    utils.get_total_experience(entities['experience']) / 12,
                    2
                )
                self.__details['total_experience'] = str(exp)
            except KeyError:
                self.__details['total_experience'] = "0"
            
            # New structured extraction
            self.__details['experience_details'] = utils.extract_experience_sections(self.__text_raw)
            
            # GLiNER Extraction (Overlay/Enhance)
            # We use GLiNER to augment potential missing fields or improve accuracy
            gliner_ents = {}
            if self.__use_gliner_extraction:
                gliner_ents = utils.extract_entities_with_gliner(self.__text_raw)
            
            if gliner_ents:
                # Merge Company Names
                if 'company_names' in gliner_ents and gliner_ents['company_names']:
                    # If we already have some, extend. If none, set.
                    existing = self.__details.get('company_names', [])
                    if existing is None: existing = []
                    self.__details['company_names'] = list(set(existing + gliner_ents['company_names']))

                # Merge Designation (taking GLiNER as priority if existing is empty or simplistic)
                if 'designation' in gliner_ents and gliner_ents['designation']:
                    existing = self.__details.get('designation', [])
                    if existing is None: existing = []
                    # GLiNER returns a list, existing might be a list or None
                    self.__details['designation'] = list(set(existing + gliner_ents['designation']))

                # Merge Degree
                if 'degree' in gliner_ents and gliner_ents['degree']:
                    existing = self.__details.get('degree', [])
                    if existing is None: existing = []
                    self.__details['degree'] = list(set(existing + gliner_ents['degree']))
            
        except KeyError:
            self.__details['total_experience'] = 0
            self.__details['experience_details'] = []
        self.__details['no_of_pages'] = utils.get_number_of_pages(
                                            self.__resume
                                        )
        return


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    print('running resume parser..')
    for root, directories, filenames in os.walk('resumes/'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    results = [p.get() for p in results]

    pprint.pprint(results)
