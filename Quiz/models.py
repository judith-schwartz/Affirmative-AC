from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1
    #loss_aversion_paoff_states updated in Taler.
    # First number for potential loss in lottery, second number for potential gain
    loss_aversion_payoff_states = [[-2,6], [-3,6], [-4,6], [-5,6], [-6,6], [-7,6]]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # General Questions
    q_age = models.IntegerField(label='Wie alt sind Sie?', min=16, max=99)
    q_gender = models.StringField(
        label = 'Was ist Ihr Geschlecht?',
        choices = ['Männlich', 'Weiblich', 'Divers', 'keine Angabe']
    )

    q_occupation = models.BooleanField(
        label= 'Was ist Ihre Tätigkeit?',
        choices=[[True, 'Studium'],
                 [False, 'Anderes']],
        initial=None
    )

    q_study_field = models.StringField(
        choices=["Wirtschaftswissenschaften",
                 "Psychologie",
                 "Mathematik/Naturwissenschaften",
                 "Rechts-/Sozialwissenschaften",
                 "Medizin/Gesundheitswissenschaften",
                 "Anderes",
                 "Ich studiere nicht."],
        label='Was studieren Sie?')

    q_n_experiment = models.IntegerField(label='An wie vielen Experimenten haben Sie (ungefähr) bereits teilgenommen?', max=500, min=0)

    q_math = models.FloatField(label="Was war Ihre letzte Mathenote (1,0 - 6,0)?", min=1.0, max=6.0)

    q_GPA_now = models.FloatField(label="Was ist Ihre aktuelle Durchschnittesnote bzw. die Ihres letzten Abschlusses?", min=1.0, max=6.0)

    q_abitur = models.FloatField(label="Was war die Abschlussnote Ihres letzten Schulabschlusses (1,0 - 4,0)?", min=1.0, max=6.0)

    q_budget = models.IntegerField(
        label="Wie viel Geld haben Sie monatlich (nach Abzug von Fixkosten wie Miete, Versicherungen etc.) zur Verfügung?",
        min=0, max=1000000)
    q_spending = models.IntegerField(
        label="Wie viel Geld geben Sie monatlich aus (nach Abzug von Fixkosten wie Miete, Versicherungen etc.)?",
        min=0, max=1000000)


    # Falk Questions

    q_falk_risk = models.IntegerField(
        initial=None,
        choices=list(range(11)),  # gar nicht risikobereit - sehr risikobereit
        label='Sind Sie im Allgemeinen ein risikobereiter Mensch oder versuchen Sie, Risiken zu vermeiden?',
        widget=widgets.RadioSelectHorizontal())

    # Time
    #q_falk_time = models.IntegerField(
        #initial=None,
        #choices=list(range(11)),  # gar nicht bereit zu verzichten - sehr bereit zu verzichten
        #label='Sind Sie im Vergleich zu anderen im Allgemeinen bereit heute auf etwas zu verzichten, um in der Zukunft davon zu profitieren oder sind Sie im Vergleich zu anderen dazu nicht bereit?',
        #widget=widgets.RadioSelectHorizontal())

    # Trust
    #q_falk_trust = models.IntegerField(
        #initial=None,
        #choices=list(range(11)),  # trifft gar nicht zu - trifft voll zu
        #label='Solange man mich nicht vom Gegenteil überzeugt, gehe ich stets davon aus, dass andere Menschen nur das Beste im Sinn haben.',
        #widget=widgets.RadioSelectHorizontal())

    # Neg. Rec.
    q_falk_neg_rec = models.IntegerField(
        initial=None,
        choices=list(range(11)),  # gar nicht bereit zu bestrafen - sehr bereit zu bestrafen
        label='Sind Sie jemand, der im Allgemeinen bereit ist, unfaires Verhalten zu bestrafen, auch wenn das für Sie mit Kosten verbunden ist, oder sind Sie dazu nicht bereit?',
        widget=widgets.RadioSelectHorizontal())

    # Pos. Rec.
    q_falk_pos_rec = models.IntegerField(
        initial=None,
        choices=list(range(11)),  # trifft gar nicht zu - trifft voll zu
        label='Wenn mir jemand einen Gefallen tut, bin ich bereit, diesen zu erwidern.',
        widget=widgets.RadioSelectHorizontal())

    # Altruism
    #q_falk_altruism = models.IntegerField(
        #initial=None,
        #min=0,
        #max=1000,
       # label='Stellen Sie sich folgende Situation vor: Sie haben in einem Preisausschreiben 1.000 € gewonnen. Wie viel würden Sie in Ihrer momentanen Situation für einen gemeinnützigen Zweck spenden?',
    #)
    # Fair
    #q_fair_1 = make_field('1. Ich würde mich gut fühlen, wenn ich eine Person wäre, die diese Eigenschaft hat.')
    #q_fair_2 = make_field('2. Jemand zu sein, der diese Eigenschaft hat, ist ein wichtiger Teil von dem, was ich bin.')
    #q_fair_3 = make_field('3. Ein großer Teil meines emotionalen Wohlbefindens ist damit verbunden, diese Eigenschaft zu haben.')
    #q_fair_4 = make_field('4. Ich würde mich schämen, eine Person zu sein, die diese Eigenschaft hat.')
    #q_fair_5 = make_field('5. Diese Eigenschaft zu haben, ist für mich nicht wirklich wichtig.')
    #q_fair_6 = make_field('6. Diese Eigenschaft zu haben, ist ein wichtiger Teil meines Selbstverständnisses.')

    # Großzügig
    #q_generous_1 = make_field('1. Ich würde mich gut fühlen, wenn ich eine Person wäre, die diese Eigenschaft hat.')
    #q_generous_2 = make_field('2. Jemand zu sein, der diese Eigenschaft hat, ist ein wichtiger Teil von dem, was ich bin.')
    #q_generous_3 = make_field('3. Ein großer Teil meines emotionalen Wohlbefindens ist damit verbunden, diese Eigenschaft zu haben.')
    #q_generous_4 = make_field('4. Ich würde mich schämen, eine Person zu sein, die diese Eigenschaft hat.')
    #q_generous_5 = make_field('5. Diese Eigenschaft zu haben, ist für mich nicht wirklich wichtig.')
    #q_generous_6 = make_field('6. Diese Eigenschaft zu haben, ist ein wichtiger Teil meines Selbstverständnisses.')

    # Freundlich
    #q_kind_1 = make_field('1. Ich würde mich gut fühlen, wenn ich eine Person wäre, die diese Eigenschaft hat.')
    #q_kind_2 = make_field('2. Jemand zu sein, der diese Eigenschaft hat, ist ein wichtiger Teil von dem, was ich bin.')
    #q_kind_3 = make_field('3. Ein großer Teil meines emotionalen Wohlbefindens ist damit verbunden, diese Eigenschaft zu haben.')
    #q_kind_4 = make_field('4. Ich würde mich schämen, eine Person zu sein, die diese Eigenschaft hat.')
    #q_kind_5 = make_field('5. Diese Eigenschaft zu haben, ist für mich nicht wirklich wichtig.')
    #q_kind_6 = make_field('6. Diese Eigenschaft zu haben, ist ein wichtiger Teil meines Selbstverständnisses.')

    # Loss Aversion / Lotteries
    #lottery_1 = models.BooleanField(
        #label='Lotterie 1: Mit 50% Wahrscheinlichkeit verlieren Sie 2 Euro und mit 50% '
              #'Wahrscheinlichkeit gewinnen Sie 6 Euro.',
        #choices=[[True, 'Akzeptieren'],
                 #[False, 'Ablehnen']],
        #initial=None,
        #widget=widgets.RadioSelectHorizontal()
    #)

    #lottery_2 = models.BooleanField(
        #label='Lotterie 2: Mit 50% Wahrscheinlichkeit verlieren Sie 3 Euro und mit 50% '
              #'Wahrscheinlichkeit gewinnen Sie 6 Euro.',
        #choices=[[True, 'Akzeptieren'],
                 #[False, 'Ablehnen']],
        #initial=None,
        #widget=widgets.RadioSelectHorizontal()
    #)

    #lottery_3 = models.BooleanField(
        #label='Lotterie 3: Mit 50% Wahrscheinlichkeit verlieren Sie 4 Euro und mit 50% '
              #'Wahrscheinlichkeit gewinnen Sie 6 Euro.',
        #choices=[[True, 'Akzeptieren'],
                 #[False, 'Ablehnen']],
        #initial=None,
        #widget=widgets.RadioSelectHorizontal()
    #)

    #lottery_4 = models.BooleanField(
        #label='Lotterie 4: Mit 50% Wahrscheinlichkeit verlieren Sie 5 Euro und mit 50% '
              #'Wahrscheinlichkeit gewinnen Sie 6 Euro.',
        #choices=[[True, 'Akzeptieren'],
                 #[False, 'Ablehnen']],
        #initial=None,
        #widget=widgets.RadioSelectHorizontal()
    #)

    #lottery_5 = models.BooleanField(
        #label='Lotterie 5: Mit 50% Wahrscheinlichkeit verlieren Sie 6 Euro und mit 50% '
              #'Wahrscheinlichkeit gewinnen Sie 6 Euro.',
        #choices=[[True, 'Akzeptieren'],
                 #[False, 'Ablehnen']],
        #initial=None,
        #widget=widgets.RadioSelectHorizontal()
    #)

    #lottery_6 = models.BooleanField(
        #label='Lotterie 6: Mit 50% Wahrscheinlichkeit verlieren Sie 7 Euro und mit 50% '
              #'Wahrscheinlichkeit gewinnen Sie 6 Euro.',
        #choices=[[True, 'Akzeptieren'],
                 #[False, 'Ablehnen']],
        #initial=None,
        #widget=widgets.RadioSelectHorizontal()
    #)


    #random_selected_lottery_id = models.IntegerField()
    #payoff_from_relevant_lottery = models.IntegerField()


    def calc_lottery_payoff(self):
        """
        
        A helper function to calculate the payoff received from the lottery
        decision.
        """
        all_lotteries = [self.lottery_1, self.lottery_2, self.lottery_3,
                         self.lottery_4, self.lottery_5, self.lottery_6]

        # Note that randint includes upper bound
        self.random_selected_lottery_id = random.randint(1, len(all_lotteries))
        
        # Minus one due to python index style
        relevant_lottery_decision = all_lotteries[self.random_selected_lottery_id - 1]
        # If the relevant lottery has been accepted, we take a random draw from it
        if relevant_lottery_decision:
            # Note that the probabilities are always 50/50
            # Minus one due to python index style
            self.payoff_from_relevant_lottery = random.choice(
                                                        Constants.loss_aversion_payoff_states[
                                                            self.random_selected_lottery_id - 1
                                                        ]
                                                )
        else:
            # If the lottery was rejected, the payoff is zero
            self.payoff_from_relevant_lottery = 0
        
        # Save to payoff field
        #self.payoff = self.payoff_from_relevant_lottery

        # Also add to participant vars to show it at the end in the last app
        self.participant.vars['payoff_from_relevant_lottery'] = self.payoff_from_relevant_lottery
        self.participant.vars['random_selected_lottery_id'] = self.random_selected_lottery_id
        self.participant.vars['relevant_lottery_decision'] = relevant_lottery_decision