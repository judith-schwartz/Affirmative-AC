from os import environ
SECRET_KEY = 'MY SECRET KEY'
#import django
#django.setup()



SESSION_CONFIGS = [
    dict(
        name='survey',
        display_name='survey',
        num_demo_participants=1,
        app_sequence=['payment_info'],
    ),
    dict(
        name='4',
        display_name='4',
        num_demo_participants=4,
        app_sequence=['tournament'],
    ),
    dict(
        name='8',
        display_name='8',
        num_demo_participants=8,
        app_sequence=['tournament'],

    ),
    dict(
        name='combined',
        display_name='combined',
        num_demo_participants=4,
        expShortName="ECT",
        expId=10,
        sessId=71,
        app_sequence=['tournament', 'slider_noanchor', 'Quiz', 'payment_info'],
    ),
    dict(
        name='slider_noanchor',
        display_name='slider_noanchor',
        num_demo_participants=1,
        app_sequence=['slider_noanchor'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=6.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""
PARTICIPANT_FIELDS = ['performance_production', 'performance_practice', 'belief_performance1', 'belief_relative1',
                      'belief_performance2', 'belief_relative2', 'outcome', 'all_outcomes']

SECRET_KEY = 'rx%=*vn(a2@&!w083zpn@h$$k9vm^%t!p$#yi*p0^(3i)aqb+h'

INSTALLED_APPS = ['otree']


