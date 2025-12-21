import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
import json
import random
import os
import subprocess

def convert_data(json_file, output_file):
    with open(json_file, 'r') as f:
        data = []
        for line in f:
            data.append(json.loads(line))

    nlp = spacy.blank("en")
    doc_bin = DocBin()
    
    skipped = 0
    for item in data:
        text = item['content']
        annotations = item['annotation']
        doc = nlp.make_doc(text)
        ents = []
        if annotations is None:
            continue
        for annotation in annotations:
            # handle both list of labels and single label
            if isinstance(annotation['label'], list):
                if not annotation['label']:
                    continue
                label = annotation['label'][0]
            else:
                label = annotation['label']
            for point in annotation['points']:
                start = point['start']
                end = point['end']
                
                # Clean whitespace
                span_text = text[start:end]
                stripped_text = span_text.strip()
                if not stripped_text:
                    continue
                
                start_offset = span_text.find(stripped_text)
                start = start + start_offset
                end = start + len(stripped_text)
                
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    skipped += 1
                else:
                    # Remove leading/trailing whitespace tokens
                    while len(span) > 0 and span[0].text.strip() == "":
                        span = span[1:]
                    while len(span) > 0 and span[-1].text.strip() == "":
                        span = span[:-1]
                    
                    if len(span) == 0:
                        skipped += 1
                        continue
                        
                    ents.append(span)
        
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents
        doc_bin.add(doc)

    print(f"Skipped {skipped} spans due to alignment issues")
    doc_bin.to_disk(output_file)

def train_model():
    # Convert data
    print("Converting data...")
    convert_data("pyresparser/traindata.json", "train.spacy")

    # Create config
    print("Creating config...")
    if not os.path.exists("config.cfg"):
        subprocess.run(["python3", "-m", "spacy", "init", "config", "config.cfg", "--lang", "en", "--pipeline", "ner"], check=True)

    # Train
    print("Training model...")
    # This might take a while, so we'll run it as a subprocess to see output in real time if we were in a shell, 
    # but here we just wait.
    # We are training a new model 'pyresparser_model'
    cmd = [
        "python3", "-m", "spacy", "train", "config.cfg",
        "--output", "./pyresparser_model",
        "--paths.train", "./train.spacy",
        "--paths.dev", "./train.spacy" # Using train as dev for simplicity since we don't have separate dev set
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    # Create base config string
    base_config = """
[paths]
train = null
dev = null
vectors = null
init_tok2vec = null

[system]
gpu_allocator = null
seed = 0

[nlp]
lang = "en"
pipeline = ["tok2vec","ner"]
batch_size = 1000

[components]

[components.tok2vec]
factory = "tok2vec"

[components.tok2vec.model]
@architectures = "spacy.Tok2Vec.v1"

[components.tok2vec.model.embed]
@architectures = "spacy.MultiHashEmbed.v1"
width = 96
rows = [5000, 2000, 1000, 1000]
attrs = ["ORTH", "SHAPE", "PREFIX", "SUFFIX"]
include_static_vectors = false

[components.tok2vec.model.encode]
@architectures = "spacy.MaxoutWindowEncoder.v1"
width = 96
depth = 4
window_size = 1
maxout_pieces = 3

[components.ner]
factory = "ner"

[components.ner.model]
@architectures = "spacy.TransitionBasedParser.v1"
tok2vec = {"@architectures": "spacy.Tok2VecListener.v1", "width": 96}
state_type = "ner"
extra_state_tokens = false
hidden_width = 64
maxout_pieces = 2
use_upper = true

[components.ner.objective]
@architectures = "spacy.Score.v1"
type = "nerscore"

[corpora]

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = ${paths.dev}
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[corpora.train]
@readers = "spacy.Corpus.v1"
path = ${paths.train}
max_length = 0
gold_preproc = false
limit = 0
augmenter = null

[training]
dev_corpus = "corpora.dev"
train_corpus = "corpora.train"
seed = ${system.seed}
gpu_allocator = ${system.gpu_allocator}
dropout = 0.1
accumulate_gradient = 1
patience = 1600
max_epochs = 0
max_steps = 20000
eval_frequency = 200
frozen_components = []
annotating_components = []
before_to_disk = null

[training.batcher]
@schedule = "compounding.v1"
start = 100
stop = 1000
compound = 1.001
t = 0.0

[training.logger]
@loggers = "spacy.ConsoleLogger.v1"
progress_bar = false

[training.optimizer]
@optimizers = "Adam.v1"
beta1 = 0.9
beta2 = 0.999
L2_is_weight_decay = true
L2 = 0.01
grad_clip = 1.0
use_averages = false
eps = 0.00000001
learn_rate = 0.001

[training.score_weights]
ents_f = 1.0
ents_p = 0.0
ents_r = 0.0
ents_per_type = null
"""
    with open("base_config.cfg", "w") as f:
        f.write(base_config)

    train_model()
