from otree.api import *
import random
import math

author = 'Lars Wittrock'

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
    prob_box = 0.5  # distribution of non-urn balls (i.e. uninformative ball distribution 3-3)
    num_rounds = 9  # number of balls shown
    aggregates = [[2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7],
                  [6, 7, 8]]  # Rounds in which color and reliability are shown
    scoring_rule_factor = 3

    # test questions
    test1_label = '1. What are the chances that the red urn is randomly selected in the beginning?'
    test1_choices = [[1, '50%'], [2, '30%'], [3, '90%'], [4, '0%']]

    test2_label = '2. How many informative balls are in the black box?'
    test2_choices = [[1, '2'], [2, '4'], [3, '6'], [4, '8']]

    test3_label = '3. How many uninformative balls are in the black box?'
    test3_choices = [[1, '2'], [2, '4'], [3, '6'], [4, '8']]

    test4_label = '4. A single blue ball labeled with a "?" is drawn from the black box. What does that imply?'
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
        [1,
         'We apply a strict no-deception rule, meaning that everything you see written during the study is correct.'],
        [2, 'We may provide you with false information if this is to our benefit.'],
        [3, 'We may provide you with false information to simplify explanations']
    ]
    test_questions_solution = [1, 2, 3, 3, 3, 1]  # Correct answers to the 4 test questions.
    test_questions_required = 5  # Number of correct test questions required to proceed with experiment.


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
    treat = models.IntegerField(doc='Variable indicating treatment for display of information')
    treat_ball_shown = models.IntegerField(doc='Variable indicating if for uninformative balls the color is displayed')

    # Variables for urn, signals and belief input
    urn = models.IntegerField(doc='Randomly generated urn color, 0=blue and 1=red')
    ball = models.StringField(doc='Ball color shown')
    check = models.StringField(doc='fake or true')
    belief = models.IntegerField(doc='Reported belief p(R)')

    # Round variables
    aggregate_round = models.BooleanField(doc='True/false variable indicating aggregate rounds')
    pay_round = models.IntegerField(doc='Randomly chosen payoff round')

    # Variables for additional indep variables
    sr_button_clicks = models.IntegerField(
        doc='Number of times clicked tell me more button in instructions for scoring rule')
    info_button_clicks = models.IntegerField(doc='Number of times clicked background instruction button')
    minus_button_clicks = models.IntegerField(doc='Number of times clicked on minus button to adjust belief report')
    plus_button_clicks = models.IntegerField(doc='Number of times clicked on plus button to adjust belief report')


def creating_session(subsession: Subsession):
    # Calculating probabilities given the input parameters
    a = (Constants.prob_urn * (1 - Constants.prob_fake))  # inf. ball, correct color: 0.3
    b = ((1 - Constants.prob_urn) * (1 - Constants.prob_fake))  # inf. ball, incorrect color: 0.1
    c = (Constants.prob_box * Constants.prob_fake)  # uninf. ball, correct color: 0.3
    d = ((1 - Constants.prob_box) * Constants.prob_fake)  # uninf. ball, incorrect color: 0.3

    # red ball in round r - true or not
    def ball_red(r):
        if (player.in_round(r).urn == 1 and draw_ball < a + c) or \
                (player.in_round(r).urn == 0 and draw_ball < b + d):
            return True
        else:
            return False

    # All possible signals
    sig_blue = ["blue", '', 'img/blue_ball_q.png']
    sig_red = ["red", '', 'img/red_ball_q.png']
    sig_blue_inf = ["blue", "informative", 'img/blue_ball_i.png']
    sig_blue_uninf = ["blue", "uninformative", 'img/blue_ball_u.png']
    sig_red_inf = ["red", "informative", 'img/red_ball_i.png']
    sig_red_uninf = ["red", "uninformative", 'img/red_ball_u.png']

    sig_uninf = ["", "uninformative", 'img/u.png']


    # Randomizing urn and signals for each participant
    if subsession.round_number == 1:
        for player in subsession.get_players():

            # Define participant variables
            participant = player.participant
            participant.signals = []

            # Randomize in which rounds signals are shown together with fake/true
            participant.aggregate_balls = random.choice(Constants.aggregates)

            # Randomizing treatment
            player.treat = random.randint(1, 3)  # 1: hist, no prev belief. 2: no hist, prev belief. 3: hist and prev belief

            player.treat_ball_shown = 1  #random.randint(0, 1)  # 0: not shown. 1: ball color shown

            # Random pay round
            player.pay_round = random.randint(1, Constants.num_rounds)

            # Random urn draw - 50-50 chance
            player.urn = round(random.uniform(0, 1))  # 0: blue and 1: red

            # Generate signals each round, given the urn draw
            list_of_round_ids = range(1, Constants.num_rounds + 1)
            for i in list_of_round_ids:
                player.in_round(i).urn = player.in_round(1).urn
                player.in_round(i).pay_round = player.in_round(1).pay_round
                player.in_round(i).treat = player.in_round(1).treat
                player.in_round(i).treat_ball_shown = player.in_round(1).treat_ball_shown

                draw_ball = random.uniform(0, 1)
                draw_inf = random.uniform(0, 1)

                # for regular rounds randomize signal (blue / red) given urn distribution and urn draw
                if i not in participant.aggregate_balls:

                    if ball_red(i):
                        participant.signals.append(sig_red)
                    else:
                        participant.signals.append(sig_blue)

                # for aggregate rounds randomize signal and informative/uninformative.
                else:

                    # for uninformative balls depending on treatment.
                    if player.treat_ball_shown == 1:

                        if ball_red(i) and draw_inf < Constants.prob_fake:
                            participant.signals.append(sig_red_uninf)

                        elif not ball_red(i) and draw_inf < Constants.prob_fake:
                            participant.signals.append(sig_blue_uninf)

                        elif ball_red(i) and draw_inf > Constants.prob_fake:
                            participant.signals.append(sig_red_inf)

                        elif not ball_red(i) and draw_inf > Constants.prob_fake:
                            participant.signals.append(sig_blue_inf)

                    else:

                        if draw_inf < Constants.prob_fake:
                            participant.signals.append(sig_uninf)

                        elif ball_red(i) and draw_inf > Constants.prob_fake:
                            participant.signals.append(sig_red_inf)

                        elif not ball_red(i) and draw_inf > Constants.prob_fake:
                            participant.signals.append(sig_blue_inf)

            print(participant.aggregate_balls)  # to check
            print(participant.signals)

    for player in subsession.get_players():

        # True/False variable if a given round is an aggregate round
        if player.round_number in player.participant.aggregate_balls:
            player.aggregate_round = True
        else:
            player.aggregate_round = False


##########################################################################
# PAGES
##########################################################################

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
                pic = player.participant.signals[i - 1][2]
            else:
                pic = 'img/blank_png.png'
            return pic

        # writing signals to data set
        player.ball = player.participant.signals[player.round_number - 1][0]
        player.check = player.participant.signals[player.round_number - 1][1]

        # current signal picture
        pic_current = player.participant.signals[player.round_number - 1][2]

        # Previous belief
        prev_belief = ''
        if player.round_number > 1:
            prev_belief = player.in_round(player.round_number - 1).belief

        # Uninformative signal without ball
        if player.check == 'uninformative' and player.treat_ball_shown == 0:
            uninf_no_ball = 1
        else:
            uninf_no_ball = 0


        # pictures displayed in history table
        pic1 = pic_displayed(1)
        pic2 = pic_displayed(2)
        pic3 = pic_displayed(3)
        pic4 = pic_displayed(4)
        pic5 = pic_displayed(5)
        pic6 = pic_displayed(6)
        pic7 = pic_displayed(7)
        pic8 = pic_displayed(8)
        pic9 = pic_displayed(9)

        # Return generated variables, used for display of information
        return {
            'pic1': pic1,
            'pic2': pic2,
            'pic3': pic3,
            'pic4': pic4,
            'pic5': pic5,
            'pic6': pic6,
            'pic7': pic7,
            'pic8': pic8,
            'pic9': pic9,

            'prev_belief': prev_belief,
            'pic_current': pic_current,
            'uninf_no_ball': uninf_no_ball,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == player.pay_round:
            if player.urn == 0:
                player.payoff = Constants.scoring_rule_factor - \
                                Constants.scoring_rule_factor * math.pow(player.belief / 100, 2)
            else:
                player.payoff = Constants.scoring_rule_factor - \
                                Constants.scoring_rule_factor * math.pow(1 - player.belief / 100, 2)
        else:
            player.payoff = 0


# Sequence of pages to be displayed
page_sequence = [Instructions,
                 InstructionsFeedback,
                 UrnDraw,
                 BeliefInput
                 ]
