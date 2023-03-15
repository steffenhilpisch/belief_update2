from otree.api import *
import random
import math

from belief_survey_step2.first_step_data import possibilities, group_weights

author = 'Steffen Hilpisch'

doc = """
This app presents participants with information and asks for probabilistic beliefs.
"""


class Constants(BaseConstants):
    # From Otree
    name_in_url = 'guessing_survey'
    players_per_group = None

    # Main inputs
    prob_urn = 0.75  # distribution of balls in relevant urn (i.e. 3/4 red balls in red urn and vice versa)
    prob_fake = 0.6  # distribution of balls in box (i.e. 6 out of 10 balls in box are uninformative)
    prob_box = 0.5  # distribution of non-urn balls (i.e. uninformative ball distribution 3-3
    num_balls = 2  # number of balls shown - not including verifications
    verifications = [2]
    scoring_rule_factor = 3

    # test questions
    test1_label = '1. What are the chances that the red urn is randomly selected?'
    test1_choices = [[1, '50%'], [2, '30%'], [3, '90%'], [4, '0%']]

    test2_label = '2. How many informative balls are in the black box?'
    test2_choices = [[1, '2'], [2, '4'], [3, '6'], [4, '8']]

    test3_label = '3. How many uninformative balls are in the black box?'
    test3_choices = [[1, '2'], [2, '4'], [3, '6'], [4, '8']]

    test4_label = '4. A single blue ball labeled with a "?" is drawn from the black box. What does that mean?'
    test4_choices = [
        [1, 'The urn selected in the beginning is more likely to be red.'],
        [2, 'This does not tell me anything about the urn selected in the beginning.'],
        [3, 'The urn selected in the beginning is more likely to be blue.']
    ]
    test5_label = '5. You see a red ball with a question mark written on it. What does that mean?'
    test5_choices = [
        [1, 'It is unclear if the ball is red or blue.'],
        [2, 'The ball is uninformative.'],
        [3, 'It is unclear if the ball is informative or uninformative.'],
        [4, 'The ball is informative.']
    ]
    test6_label = '6. What is our policy on deception?'
    test6_choices = [
        [1, 'We apply a strict no-deception rule, meaning that everything you see written during the study is correct.'],
        [2, 'We may provide you with false information if this is to our benefit.'],
        [3, 'We may provide you with false information to simplify explanations']
    ]
    test_questions_solution = [1, 2, 3, 3, 3, 1]  # Correct answers to the 4 test questions. TO UPDATE
    test_questions_required = 5  # Number of correct test questions required to proceed with experiment.

    num_rounds = num_balls + 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Variables for instruction test
    test1 = models.IntegerField(doc='Test question 1',
                                label=Constants.test1_label,
                                choices=Constants.test1_choices,
                                widget=widgets.RadioSelect)
    test2 = models.IntegerField(doc='Test question 2',
                                label=Constants.test2_label,
                                choices=Constants.test2_choices,
                                widget=widgets.RadioSelect)
    test3 = models.IntegerField(doc='Test question 3',
                                label=Constants.test3_label,
                                choices=Constants.test3_choices,
                                widget=widgets.RadioSelect)
    test4 = models.IntegerField(doc='Test question 4',
                                label=Constants.test4_label,
                                choices=Constants.test4_choices,
                                widget=widgets.RadioSelect)
    test5 = models.IntegerField(doc='Test question 5',
                                label=Constants.test5_label,
                                choices=Constants.test5_choices,
                                widget=widgets.RadioSelect)
    test6 = models.IntegerField(doc='Test question 6',
                                label=Constants.test6_label,
                                choices=Constants.test6_choices,
                                widget=widgets.RadioSelect)

    test_correct = models.IntegerField(doc='Number of correct test questions')

    # Treatment variable
    treat = models.IntegerField(doc='Variable indicating treatment')

    # we always choose the blue urn
    ball = models.StringField(doc='Ball color shown')
    verification = models.StringField(doc='Fake/confirm signal')
    belief = models.IntegerField(doc='Reported belief p(R)')

    # Round variables
    verify_round = models.BooleanField(doc='True/false variable indicating verification rounds')
    pay_round = models.IntegerField(doc='Randomly chosen payoff round')

    # Variables for additional indep variables
    sr_button_clicks = models.IntegerField(
        doc='Number of times clicked tell me more button in instructions for scoring rule')
    info_button_clicks = models.IntegerField(doc='Number of times clicked background instruction button')
    minus_button_clicks = models.IntegerField(doc='Number of times clicked on minus button to adjust belief report')
    plus_button_clicks = models.IntegerField(doc='Number of times clicked on plus button to adjust belief report')

def creating_session(subsession: Subsession):

    # All possible signals
    sig_blue = ["blue", '', 'img/blue_ball_q.png']
    sig_red = ["red", '', 'img/red_ball_q.png']
    # these are still valid. but we generate them on the fly so we do not have a 8 case if else spagetti
    # sig_blue_true = ["blue", "true", 'img/blue_ball_i.png']
    # sig_blue_fake = ["blue", "fake", 'img/blue_ball_u.png']
    # sig_red_true = ["red", "true", 'img/red_ball_i.png']
    # sig_red_fake = ["red", "fake", 'img/red_ball_u.png']

    # Randomizing urn and signals for each participant
    if subsession.round_number == 1:
        for player in subsession.get_players():



            # Define participant variables
            participant = player.participant

            # select one other player `row` we want to query the current player with
            # choose group (blue or red and informative or not)
            # we expect to have more than one element per group
            choosen_group = random.choices(list(group_weights.keys()), weights=group_weights.values(), k=1)[0]
            participant.other_report = random.choice(possibilities[choosen_group]) # eg data [23, 65, "informativ"]

            # used in the html part to display the correct template (mabye also used somewhere else LOL)
            participant.verification_rounds = [3]
            # what to display to the player:
            # 1: hist, no prev belief. 2: no hist, prev belief. 3: hist and prev belief
            # we show everything everytime
            player.treat = 3 #random.randint(1, 3)

            # Random pay round
            player.pay_round = random.randint(1, Constants.num_rounds)

            list_of_round_ids = range(1, Constants.num_rounds + 1)
            # TODO: check if really need this
            for i in list_of_round_ids:
                # copy information from the first round to the i-th round
                # player.in_round(i).urn = player.in_round(1).urn
                player.in_round(i).pay_round = player.in_round(1).pay_round
                player.in_round(i).treat = player.in_round(1).treat

    for player in subsession.get_players():
        if player.round_number in player.participant.verification_rounds:
            player.verify_round = True
        else:
            player.verify_round = False


####################################
# PAGES
####################################

# Instructions and test are only shown in the beginning, i.e. in round 1
class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'sr_button_clicks']

    @staticmethod
    def vars_for_template(player: Player):
        def sr_urn(report, urn):
            if urn == 'red':
                error_red = (100 - report) / 100
                score = Constants.scoring_rule_factor - Constants.scoring_rule_factor * math.pow(error_red, 2)
            else:
                error_blue = report / 100
                score = Constants.scoring_rule_factor - Constants.scoring_rule_factor * math.pow(error_blue, 2)
            return score

        example_60_red = "%.2f" % sr_urn(60, 'red')
        example_60_blue = "%.2f" % sr_urn(60, 'blue')

        def sr_report(belief, report):
            score = belief / 100 * sr_urn(report, 'red') + (1 - belief / 100) * sr_urn(report, 'blue')
            return score

        example_60_60 = "%.2f" % round(sr_report(60, 60), 2)
        example_60_10 = "%.2f" % round(sr_report(60, 10), 2)
        example_60_100 = "%.2f" % round(sr_report(60, 100), 2)

        return {
            'example_60_blue': example_60_blue,
            'example_60_red': example_60_red,
            'example_60_60': example_60_60,
            'example_60_10': example_60_10,
            'example_60_100': example_60_100
        }

    # Correct answers for test questions
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.test1 == Constants.test_questions_solution[0]:
            test1_correct = 1
        else:
            test1_correct = 0

        if player.test2 == Constants.test_questions_solution[1]:
            test2_correct = 1
        else:
            test2_correct = 0

        if player.test3 == Constants.test_questions_solution[2]:
            test3_correct = 1
        else:
            test3_correct = 0

        if player.test4 == Constants.test_questions_solution[3]:
            test4_correct = 1
        else:
            test4_correct = 0

        if player.test5 == Constants.test_questions_solution[4]:
            test5_correct = 1
        else:
            test5_correct = 0

        if player.test6 == Constants.test_questions_solution[5]:
            test6_correct = 1
        else:
            test6_correct = 0

        player.test_correct = test1_correct + test2_correct + test3_correct \
                              + test4_correct + test5_correct + test6_correct


class InstructionsFeedback(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        # Returns correct solution for each question
        test1_solution = Constants.test1_choices[Constants.test_questions_solution[0] - 1][1]
        test2_solution = Constants.test2_choices[Constants.test_questions_solution[1] - 1][1]
        test3_solution = Constants.test3_choices[Constants.test_questions_solution[2] - 1][1]
        test4_solution = Constants.test4_choices[Constants.test_questions_solution[3] - 1][1]
        test5_solution = Constants.test5_choices[Constants.test_questions_solution[4] - 1][1]
        test6_solution = Constants.test6_choices[Constants.test_questions_solution[5] - 1][1]

        return {
            'test1_solution': test1_solution,
            'test2_solution': test2_solution,
            'test3_solution': test3_solution,
            'test4_solution': test4_solution,
            'test5_solution': test5_solution,
            'test6_solution': test6_solution
        }


class UrnDraw(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class BeliefInput(Page):
    form_model = 'player'
    form_fields = ['belief', 'info_button_clicks', 'minus_button_clicks', 'plus_button_clicks']

    @staticmethod
    def vars_for_template(player: Player):
        # defining which ball is displayed -
        def pic_displayed(i):
            if player.round_number >= i:
                participant = player.participant
                pic = player.participant.ball[i - 1][2]
            else:
                pic = 'img/blank_png.png'
            return pic

        # writing signals to data set
        participant = player.participant
        # contains prozent for first two rount and then informativ or fake for 3rd round
        other_report = player.participant.other_report[player.round_number - 1]

        prev_belief = ''
        if player.round_number > 1:
            prev_belief = player.in_round(player.round_number - 1).belief

        pic1 = 'img/grey_ball_q.png' if player.round_number >= 1 else 'img/blank_png.png'

        # in the first round we show nothing
        # in the second we show the ? one
        # in the third round the displayed ball depends on the other reported.
        pic2 = 'img/blank_png.png'

        if player.round_number == 2:
            pic2 = 'img/grey_ball_q.png'
        elif player.round_number == 3:
            # uninformed starts with lowercase u
            # informed starts with lowercase i
            pic2 = f'img/grey_ball_{other_report[0]}.png'

        # Return generated variables, used for display of information
        return {
            'pic1': pic1,
            'pic2': pic2,

            "other_report": other_report,
            'prev_belief': prev_belief,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # calculate payoff
        if player.round_number == player.pay_round:
            # we do not have a urn
            player.payoff = Constants.scoring_rule_factor - \
                            Constants.scoring_rule_factor * math.pow(player.belief / 100, 2)
            # #TODO: fix we do not have a urn
            # if player.urn == 0:
            #     player.payoff = Constants.scoring_rule_factor - \
            #                     Constants.scoring_rule_factor * math.pow(player.belief / 100, 2)
            # else:
            #     player.payoff = Constants.scoring_rule_factor - \
            #                     Constants.scoring_rule_factor * math.pow(1 - player.belief / 100, 2)
        else:
            player.payoff = 0

        if player.round_number == 3: #player.participant.verification_rounds[2]:
            # we are in a verification round.
            participant = player.participant

            other_report_round1 = player.participant.other_report[0] # round 1
            other_report_round2 = player.participant.other_report[1] # round 2
            other_report_round3 = player.participant.other_report[2] # round 3

            participant.belief_q = [1,
                                    other_report_round1,
                                    player.in_round(1).belief,
                                    2,
                                    other_report_round2,
                                    player.in_round(2).belief,
                                    3,
                                    other_report_round3, # this is informativ or not informativ
                                    player.in_round(3).belief,
                                    ]

            print("belief_q: {participant.belief_q}")


# Sequence of pages to be displayed
page_sequence = [Instructions,
                 InstructionsFeedback,
                 UrnDraw,
                 BeliefInput
                 ]
