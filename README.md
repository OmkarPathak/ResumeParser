# ResumeParser
This is just a wrapper for pyresparser. I have released the resume parser as a [Python Package](https://github.com/OmkarPathak/pyresparser)

# Installation

```bash
pip install pyresparser
```

- For supported formats and other installation instructions visit: [https://github.com/OmkarPathak/pyresparser](https://github.com/OmkarPathak/pyresparser)

# Docker Installation

- For running the whole app in docker just run the following command from the root of the project

```bash
docker-compose up -d build
```

- Once all the installations are done, visit `0.0.0.0` in your broswer to use the app

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

# Notes:

- If you are running the app on windows, then you can only extract .docs and .pdf files

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
