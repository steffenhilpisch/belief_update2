from otree.api import *

author = 'Steffen hilpisch'

doc = """
Intro_Step1 to the study
"""


class Constants(BaseConstants):
    name_in_url = 'Intro_Step1'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    consent = models.BooleanField(
        widget=widgets.CheckboxInput(),
        label="I agree.",
    )

    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")

    @staticmethod
    def before_next_page(self, timeout_happened):
        self.prolific_id = self.participant.label

    welcome_button_clicks = models.IntegerField(doc="Number of clicks on button about payment details on welcome page")

    # Error messages
    @staticmethod
    def consent_error_message(value):
        print('value is', value)
        if value != 1:
            return 'Your confirmation is required to proceed.'


# PAGES

class Welcome(Page):
    form_model = 'player'
    form_fields = ['is_mobile', 'welcome_button_clicks']


class SorryNoPhone(Page):
    @staticmethod
    def is_displayed(player):
        return player.is_mobile == 1


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']





page_sequence = [Welcome, SorryNoPhone, Consent]
