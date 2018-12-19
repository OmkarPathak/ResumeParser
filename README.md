# ResumeParser
A simple resume parser used for extracting information from resumes

# Installation

- For extracting text from various documents we use [pdfminer](https://github.com/euske/pdfminer) and [doc2text](https://github.com/ankushshah89/python-docx2txt) modules. Install them using:

```bash
pip install pdfminer        # python 2
pip install pdfminer.six    # python 3
pip install doc2text
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

- Modify `skills.csv` as per your requirements

- Modify `Education Degrees` as per you requirements in [constants.py](https://github.com/OmkarPathak/ResumeParser/blob/master/constants.py)

- Place all the resumes that you want to parse in `resumes/` directory

- Run `resume_parser.py`

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

- [ ] Extracting Projects
- [ ] Extracting hobbies
- [ ] Extracting universities
- [ ] Extracting month of passing
- [ ] Extracting Awards/ Achievements/ Recognition

# References that helped me get here

- [https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy](https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy)

- [https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/](https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)

- [https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48](https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48)