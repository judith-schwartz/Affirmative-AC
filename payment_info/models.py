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
    performance_payout = 0.05
    belief_payout = 0.5


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

        for p in self.get_players():
            selected_outcomes = p.participant.vars['selected_outcomes']

            for outcome in selected_outcomes:
                bonus = outcome['bonus']
                treatment = outcome['treatment']
                first_color = outcome['first_color']
                second_color = outcome['second_color']

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
                print(bonus_list)
                print(bonus_key)
                if bonus_list:
                    selected_bonus = c(random.choice(bonus_list))

                    if first_place:
                        self.bonus = selected_bonus
                    elif second_place:
                        self.bonus = c(10) - selected_bonus
                else:
                    self.bonus = -Constants.tournament_fee
            else:
                self.bonus = -Constants.tournament_fee