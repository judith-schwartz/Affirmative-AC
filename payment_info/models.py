import random
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

doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class Constants(BaseConstants):
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1
    tournament_fee = 2
    performance_fee = 0.10
    belief_fee = 0.5


class Subsession(BaseSubsession):

    def bonus_groups(self):

        self.session.vars['T_GG'] = []
        self.session.vars['T_BG'] = []
        self.session.vars['T_GB'] = []
        self.session.vars['T_BB'] = []
        self.session.vars['C_BG'] = []
        self.session.vars['C_GB'] = []
        self.session.vars['C_GG'] = []
        self.session.vars['C_BB'] = []

        participating_players = [p for p in self.get_players() if p.participant.vars.get('Participated', False)]
        if not participating_players:
            return

        for p in self.get_players():
            selected_outcomes = p.participant.vars['selected_outcomes']

            for outcome in selected_outcomes:
                if not outcome:  # Check if the outcome dictionary is empty
                    continue  # Skip this iteration and move to the next outcome

                bonus = outcome['bonus']
                treatment = outcome.get('treatment', '')  # Use dict.get() to handle missing key
                first_color = outcome.get('first_color', '')
                second_color = outcome.get('second_color', '')

                if treatment == 'treatment' and first_color == 'green' and second_color == 'green':
                    self.session.vars['T_GG'].append(bonus)
                elif treatment == 'control' and first_color == 'blue' and second_color == 'green':
                    self.session.vars['C_BG'].append(bonus)
                elif treatment == 'treatment' and first_color == 'green' and second_color == 'blue':
                    self.session.vars['T_GB'].append(bonus)
                elif treatment == 'control' and first_color == 'blue' and second_color == 'blue':
                    self.session.vars['C_BB'].append(bonus)
                elif treatment == 'control' and first_color == 'green' and second_color == 'green':
                    self.session.vars['C_GG'].append(bonus)
                elif treatment == 'control' and first_color == 'green' and second_color == 'blue':
                    self.session.vars['C_GB'].append(bonus)

        print(self.session.vars['T_GG'])
        print(self.session.vars['T_BG'])
        print(self.session.vars['T_GB'])
        print(self.session.vars['T_BB'])
        print(self.session.vars['C_BG'])
        print(self.session.vars['C_GB'])
        print(self.session.vars['C_GG'])
        print(self.session.vars['C_BB'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bonus = models.CurrencyField(initial=0)
    performance_payout = models.CurrencyField(initial=0)
    belief_payout = models.CurrencyField(initial=0)

    def calculate_bonus(self):
        if self.participant.vars.get('Participated', False):
            outcome = self.participant.vars['outcome']
            first_place = outcome.get('first_place', False)
            second_place = outcome.get('second_place', False)
            treatment = outcome.get('treatment', 'control')
            first_color = outcome.get('first_color', 'green')
            second_color = outcome.get('second_color', 'green')

            if first_place or second_place:
                bonus_key = f"{treatment[0].upper()}_{first_color[0].upper()}{second_color[0].upper()}"

                bonus_list = self.session.vars.get(bonus_key, [])  # Use .get() method with fallback
                valid_bonus_list = [value for value in bonus_list if 0 <= value <= 10 and value != -1]

                if valid_bonus_list:
                    selected_bonus = c(random.choice(valid_bonus_list))

                    if first_place:
                        self.bonus = selected_bonus
                    elif second_place:
                        self.bonus = c(10) - selected_bonus
                else:
                    selected_bonus = round(random.uniform(0, 10), 2)  # Random value between 0 and 10 with 0.01 increments
                    if first_place:
                        self.bonus = selected_bonus
                    elif second_place:
                        self.bonus = c(10) - selected_bonus
            else:
                self.bonus = -Constants.tournament_fee

    def calculate_performance_payout(self):
        self.performance_payout = self.participant.performance_production * Constants.performance_fee

    def calculate_belief_payout(self):
        belief_performance1_correct = self.participant.belief_performance1 == self.participant.performance_practice
        belief_performance2_correct = self.participant.belief_performance2 == self.participant.performance_production

        group_players = self.group.get_players()
        group_performance_practice = [p.participant.performance_practice for p in group_players]
        group_performance_production = [p.participant.performance_production for p in group_players]

        belief_relative1_correct = self.check_belief_relative(self.participant.belief_relative1,
                                                              self.participant.performance_practice,
                                                              group_performance_practice)
        belief_relative2_correct = self.check_belief_relative(self.participant.belief_relative2,
                                                              self.participant.performance_production,
                                                              group_performance_production)

        num_correct_beliefs = 0

        if belief_performance1_correct:
            num_correct_beliefs += 1

        if belief_performance2_correct:
            num_correct_beliefs += 1

        if belief_relative1_correct:
            num_correct_beliefs += 1

        if belief_relative2_correct:
            num_correct_beliefs += 1

        self.belief_payout = num_correct_beliefs * Constants.belief_fee
        print(num_correct_beliefs)

        self.participant.vars['belief_payout'] = self.belief_payout if self.belief_payout is not None else 0

    def check_belief_relative(self, belief_relative, performance, group_performance):
        percentile_thresholds = range(0, 91, 10)
        percentile_index = belief_relative // 10

        num_players_below_threshold = sum(p < performance for p in group_performance)
        num_players_in_threshold_range = sum(
            performance - 1 <= p <= performance + percentile_thresholds[percentile_index] for p in group_performance)

        return num_players_below_threshold >= num_players_in_threshold_range

    def calculate_payoff(self):
        self.payoff = self.bonus + self.belief_payout + self.performance_payout

        print(self.payoff)
