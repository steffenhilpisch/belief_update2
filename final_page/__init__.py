from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1
    pass

class Player(BasePlayer):
    pass

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class FinalPage(Page):
    # feedback on correct urn and payment.
    pass

page_sequence = [
    FinalPage,
                 ]