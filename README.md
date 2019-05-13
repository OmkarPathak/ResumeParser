# ResumeParser
A simple resume parser used for extracting information from resumes

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

- Run `python resume_parser/cli.py -f <resume_file_path>`

# Docker Installation

- For running the whole app in docker just run the following command from the root of the project

```bash
docker-compose up -d build
```

- Once all the installations are done, visit `0.0.0.0` in your broswer to use the app

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
python resume_parser/manage.py createsuperuser
python resume_parser/manage.py runserver
```

- Visit `127.0.0.1` to view the GUI

# Working:

![Working](results/resume_parser_result.png)

# Result

The module would return a list of dictionary objects with result as follows:

```
[{'education': [('BE', '2014')],
  'email': 'omkarpathak27@gmail.com',
  'experience': [' Schlumberger DATA ENGINEER Pune'],
  'mobile_number': '8087996634',
  'name': 'Omkar Pathak',
  'no_of_pages': 3,
  'skills': ['Python',
             'C',
             'Technical',
             'Linux',
             'Machine learning',
             'System',
             'Html',
             'C++',
             'Security',
             'Testing',
             'Content',
             'Apis',
             'Engineering',
             'Payments',
             'Django',
             'Excel',
             'Admissions',
             'Mysql',
             'Windows',
             'Automation',
             'Opencv',
             'Website',
             'Css',
             'Js',
             'Algorithms',
             'Flask',
             'Programming',
             'Writing',
             'Training',
             'Php',
             'Reports',
             'Photography',
             'Open source',
             'Github',
             'Analytics',
             'Api'],
  'total_experience': 0.58}]
```

# References that helped me get here

- [https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy](https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy)

- [https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/](https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)

- [https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48](https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48)

### Built with ♥ and :coffee: by [`Omkar Pathak`](http://www.omkarpathak.in/)

# Donation

If you have found my softwares to be of any use to you, do consider helping me pay my internet bills. This would encourage me to create many such softwares :)

| PayPal | <a href="https://paypal.me/omkarpathak27" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg" alt="Donate via PayPal!" title="Donate via PayPal!" /></a> |
|:-------------------------------------------:|:-------------------------------------------------------------:|
| ₹ (INR)  | <a href="https://www.instamojo.com/@omkarpathak/" target="_blank"><img src="https://www.soldermall.com/images/pic-online-payment.jpg" alt="Donate via Instamojo" title="Donate via instamojo" /></a> |
