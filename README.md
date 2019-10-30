# ResumeParser
A simple resume parser used for extracting information from resumes

Note: This is just a wrapper around the pyresparser. The actual source code for the parsing can be found here: [https://github.com/OmkarPathak/pyresparser](https://github.com/OmkarPathak/pyresparser)

# Installation

- For extracting text from various documents we use [pdfminer](https://github.com/euske/pdfminer) and [docx2text](https://github.com/ankushshah89/python-docx2txt) modules. Install them using:

```bash
pip install pdfminer        # python 2
pip install pdfminer.six    # python 3
pip install docx2txt
```

- For NLP operations we use spacy and nltk. Install them using:

```bash
# spaCy
pip install spacy
python -m spacy download en_core_web_sm

# nltk
pip install nltk
python -m nltk nltk.download('words')
```

- For extracting other supporting dependencies, execute:

```bash
pip install -r resume_parser/requirements.txt

# and then execute
python resume_parser/pre_requisites.py
```

- Modify `resume_parser/resume_parser/skills.csv` as per your requirements

- Modify `Education Degrees` as per you requirements in [resume_parser/resume_parser/constants.py](https://github.com/OmkarPathak/ResumeParser/blob/master/constants.py)

- Place all the resumes that you want to parse in `resume_parser/resumes/` directory

- Run `resume_parser/resume_parser/resume_parser.py`

# CLI

For running the resume extractor you can also use the `cli` provided

```bash
usage: cli.py [-h] [-f FILE] [-d DIRECTORY]

optional arguments:
  -h, --help                            show this help message and exit
  -f FILE, --file FILE                  resume file to be extracted
  -d DIRECTORY, --directory DIRECTORY   directory containing all the resumes to be extracted
```

For extracting data from a single resume file, use

```bash
python resume_parser/cli.py -f <resume_file_path>
```

For extracting data from several resumes, place them in a directory and then execute

```bash
python resume_parser/cli.py -d <resume_directory_path>
```

# GUI

- Django used
- Easy extraction and interpretation using GUI
- For running GUI execute:

```bash
python resume_parser/manage.py makemigrations
python resume_parser/manage.py migrate
python resume_parser/manage.py runserver
```

- Visit `127.0.0.1` to view the GUI

# Working:

![Working](results/resume_parser_result.png)

# Result

The module would return a list of dictionary objects with result as follows:

```
[
    {
        'education': [('BE', '2014')],
        'email': 'omkarpathak27@gmail.com',
        'mobile_number': '8087996634',
        'name': 'Omkar Pathak',
        'skills': [
            'Flask',
            'Django',
            'Mysql',
            'C',
            'Css',
            'Html',
            'Js',
            'Machine learning',
            'C++',
            'Algorithms',
            'Github',
            'Php',
            'Python',
            'Opencv'
        ]
    }
]
```

# To DO

- [x] Extracting Experience
- [ ] Extracting Projects
- [ ] Extracting hobbies
- [ ] Extracting universities
- [ ] Extracting month of passing
- [ ] Extracting Awards/ Achievements/ Recognition

# References that helped me get here

- [https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy](https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy)

- [https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/](https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)

- [https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48](https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48)
