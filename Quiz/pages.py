from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class General(Page):
    form_model = 'player'
    form_fields = ['q_age', 'q_gender', 'q_occupation', 'q_study_field', 'q_n_experiment',
                   'q_math', 'q_GPA_now', 'q_abitur', 'q_budget', 'q_spending']

class Falk(Page):
    form_model = 'player'
    form_fields = ['q_falk_risk', 'q_falk_neg_rec',
                   'q_falk_pos_rec']

# class Self_Image(Page):
    # form_model = 'player'
    # form_fields = ['q_fair_1', 'q_fair_2', 'q_fair_3', 'q_fair_4', 'q_fair_5', 'q_fair_6',
                   # 'q_generous_1', 'q_generous_2', 'q_generous_3', 'q_generous_4', 'q_generous_5', 'q_generous_6',
                   # 'q_kind_1', 'q_kind_2', 'q_kind_3', 'q_kind_4', 'q_kind_5', 'q_kind_6']


class Lottery(Page):
    form_model = 'player'
    form_fields = ['lottery_1', 'lottery_2', 'lottery_3', 'lottery_4', 'lottery_5', 'lottery_6']


    def before_next_page(self):
        # Get payoff for those lottery decision
        self.player.calc_lottery_payoff()

page_sequence = [General, Falk]
