from os import environ

SESSION_CONFIGS = [
    dict(
        name='belief_update2',
        display_name='Survey on Belief Updating',
        app_sequence=[#'Intro_Step1',
                      'Intro_Step2',
                      #'belief_survey',
                      'belief_survey_step2',
                      #'questionnaire'
                      'final_page', # end for step 1 and 2
                      ],
        num_demo_participants=10,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=1.50,
    doc="",
    use_browser_bots=False,
    currency_code='EUR'
)

PARTICIPANT_FIELDS = ['signals',
                     # fields need for first step:
                     # 'ball', 'ball_extra', 'prev_verifications', 'verification_balls', 'verification_rounds', 'belief_q'

                     # fields for second step:
                      'other_report', "belief_q",
                      #'aggregate_balls'
                      ]
SESSION_FIELDS = []

# ISO-639 code
LANGUAGE_CODE = 'en-us'

REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7277142838663'

ROOMS = [
    dict(
        name='belief_update2',
        display_name='belief_update2',
    ),
    dict(
        name='belief_update2_prolific',
        display_name='belief_update2_prolific',
    ),
]
