# from glob import glob
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import json
# from collections import defaultdict
# base_json = 'dataset/resume_dataset.json'
# def pop_annot(raw_line):
#     in_line = defaultdict(list, **raw_line)
#     if 'annotation' in in_line:
#         labels = in_line['annotation']
#         for c_lab in labels:
#             if len(c_lab['label'])>0:
#                 in_line[c_lab['label'][0]] += c_lab['points']
#     return in_line
# with open(base_json, 'r') as f:
#     # data is jsonl and so we parse it line-by-line
#     resume_data = [json.loads(f_line) for f_line in f.readlines()]
#     resume_df = pd.DataFrame([pop_annot(line) for line in resume_data])
# resume_df['length'] = resume_df['content'].map(len)
# # resume_df['length'].hist()
# # print(resume_df.sample(3))

# def extract_higlights(raw_line):
#     in_line = defaultdict(list, **raw_line)
#     if 'annotation' in in_line:
#         labels = in_line['annotation']
#         for c_lab in labels:
#             if len(c_lab['label'])>0:
#                 in_line['highlight'] += [dict(category = c_lab['label'][0], **cpts) for cpts in c_lab['points']]
#     return in_line
# resume_hl_df = pd.DataFrame([extract_higlights(line) for line in resume_data])
# resume_hl_df['length'] = resume_hl_df['content'].map(len)
# # resume_hl_df['length'].hist()
# # resume_hl_df.sample(3)

# from string import ascii_lowercase, digits
# valid_chars = ascii_lowercase+digits+'@., '
# focus_col = 'highlight'
# focus_df = resume_hl_df[['content', focus_col, 'length']].copy().dropna()
# # clean up the text but maintain the length
# focus_df['kosher_content'] = resume_df['content'].str.lower().map(lambda c_text: ''.join([c if c in valid_chars else ' ' for c in c_text]))
# # print(focus_col, 'with', focus_df.shape[0], 'complete results')
# # print('First result')
# for _, c_row in focus_df.query('length<2000').sample(1, random_state = 20).iterrows():
#     # print(len(c_row['content']))
#     for yoe in c_row[focus_col]:
#         s,e = yoe['start'], yoe['end']
#         print(yoe)
#         # print(c_row['content'][s:e+1])

############################################  NOTE  ########################################################
#
#           Creates NER training data in Spacy format from JSON downloaded from Dataturks.
#
#           Outputs the Spacy training data which can be used for Spacy training.
#
############################################################################################################
import json
import random
import logging
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from spacy.gold import GoldParse
from spacy.scorer import Scorer
from sklearn.metrics import accuracy_score
def convert_dataturks_to_spacy(dataturks_JSON_FilePath):
    try:
        training_data = []
        lines=[]
        with open(dataturks_JSON_FilePath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                #only a single point in text annotation.
                point = annotation['points'][0]
                labels = annotation['label']
                # handle both list of labels or a single label.
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    #dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                    entities.append((point['start'], point['end'] + 1 ,label))


            training_data.append((text, {"entities" : entities}))

        return training_data
    except Exception as e:
        logging.exception("Unable to process " + dataturks_JSON_FilePath + "\n" + "error = " + str(e))
        return None

import spacy
################### Train Spacy NER.###########
def train_spacy():

    TRAIN_DATA = convert_dataturks_to_spacy("dataset/resume_dataset.json")
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(10):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    #test the model and evaluate it
    examples = convert_dataturks_to_spacy("dataset/resume_dataset_test.json")
    tp=0
    tr=0
    tf=0

    ta=0
    c=0        
    for text,annot in examples:

        f=open("resume"+str(c)+".txt","w")
        doc_to_test=nlp(text)
        d={}
        for ent in doc_to_test.ents:
            d[ent.label_]=[]
        for ent in doc_to_test.ents:
            d[ent.label_].append(ent.text)

        for i in set(d.keys()):

            f.write("\n\n")
            f.write(i +":"+"\n")
            for j in set(d[i]):
                f.write(j.replace('\n','')+"\n")
        d={}
        for ent in doc_to_test.ents:
            d[ent.label_]=[0,0,0,0,0,0]
        for ent in doc_to_test.ents:
            doc_gold_text= nlp.make_doc(text)
            gold = GoldParse(doc_gold_text, entities=annot.get("entities"))
            y_true = [ent.label_ if ent.label_ in x else 'Not '+ent.label_ for x in gold.ner]
            y_pred = [x.ent_type_ if x.ent_type_ ==ent.label_ else 'Not '+ent.label_ for x in doc_to_test]  
            if(d[ent.label_][0]==0):
                #f.write("For Entity "+ent.label_+"\n")   
                #f.write(classification_report(y_true, y_pred)+"\n")
                (p,r,f,s)= precision_recall_fscore_support(y_true,y_pred,average='weighted')
                a=accuracy_score(y_true,y_pred)
                d[ent.label_][0]=1
                d[ent.label_][1]+=p
                d[ent.label_][2]+=r
                d[ent.label_][3]+=f
                d[ent.label_][4]+=a
                d[ent.label_][5]+=1
        c+=1
    for i in d:
        print("\n For Entity "+i+"\n")
        print("Accuracy : "+str((d[i][4]/d[i][5])*100)+"%")
        print("Precision : "+str(d[i][1]/d[i][5]))
        print("Recall : "+str(d[i][2]/d[i][5]))
        print("F-score : "+str(d[i][3]/d[i][5]))
train_spacy()