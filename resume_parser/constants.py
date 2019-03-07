from nltk.corpus import stopwords

# Omkar Pathak
NAME_PATTERN      = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

# Education (Upper Case Mandatory)
EDUCATION         = [
                    'BE','B.E.', 'B.E', 'BS', 'B.S', 'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'BTECH', 'MTECH', 
                    'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
                    ]

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'

NUMBER            = r'\d+'

# For finding date ranges
MONTHS_SHORT      = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
MONTHS_LONG       = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
MONTH             = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR              = r'(((20|19)(\d{2})))'

STOPWORDS         = set(stopwords.words('english'))

RESUME_SECTIONS = [
                    'accomplishments',
                    'experience',
                    'education',
                    'interests',
                    'projects',
                    'professional experience',
                    'publications',
                    'skills',
                ]

COMPETENCIES = {
    'teamwork': [
        'supervised',
        'facilitated',
        'planned',
        'plan',
        'served',
        'serve',
        'project lead',
        'managing',
        'managed',
        'lead ',
        'project team',
        'team',
        'conducted',
        'worked',
        'gathered',
        'organized',
        'mentored',
        'assist',
        'review',
        'help',
        'involve',
        'share',
        'support',
        'coordinate',
        'cooperate',
        'contributed'
    ],
    'communication': [
        'addressed',
        'collaborated',
        'conveyed',
        'enlivened',
        'instructed',
        'performed',
        'presented',
        'spoke',
        'trained',
        'author',
        'communicate',
        'define',
        'influence',
        'negotiated',
        'outline',
        'proposed',
        'persuaded',
        'edit',
        'interviewed',
        'summarize',
        'translate',
        'write',
        'wrote',
        'project plan',
        'business case',
        'proposal',
        'writeup'
    ],
    'analytical': [
        'process improvement',
        'competitive analysis',
        'aligned',
        'strategive planning',
        'cost savings',
        'researched ',
        'identified',
        'created',
        'led',
        'measure',
        'program',
        'quantify',
        'forecasr',
        'estimate',
        'analyzed',
        'survey',
        'reduced',
        'cut cost',
        'conserved',
        'budget',
        'balanced',
        'allocate',
        'adjust',
        'lauched',
        'hired',
        'spedup',
        'speedup',
        'ran',
        'run',
        'enchanced',
        'developed'
    ],
    'result_driven': [
        'cut',
        'decrease',
        'eliminate',
        'increase',
        'lower',
        'maximize',
        'rasie',
        'reduce',
        'accelerate',
        'accomplish',
        'advance',
        'boost',
        'change',
        'improve',
        'saved',
        'save',
        'solve',
        'solved',
        'upgrade',
        'fix',
        'fixed',
        'correct',
        'achieve'           
    ],
    'leadership': [
        'advise',
        'coach',
        'guide',
        'influence',
        'inspire',
        'instruct',
        'teach',
        'authorized',
        'chair',
        'control',
        'establish',
        'execute',
        'hire',
        'multi-task',
        'oversee',
        'navigate',
        'prioritize',
        'approve',
        'administer',
        'preside',
        'enforce',
        'delegate',
        'coordinate',
        'streamlined',
        'produce',
        'review',
        'supervise',
        'terminate',
        'found',
        'set up',
        'spearhead',
        'originate',
        'innovate',
        'implement',
        'design',
        'launch',
        'pioneer',
        'institute'
    ]
}