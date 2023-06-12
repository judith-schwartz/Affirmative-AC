from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Start(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.bonus_groups()
        for player in self.subsession.get_players():
            player.calculate_bonus()
            player.calculate_performance_payout()
            player.calculate_belief_payout()
            player.calculate_payoff()
class PaymentInfo(Page):

    def vars_for_template(self):
        # Access the participant variables
        participated = self.participant.vars.get('Participated', False)
        outcome = self.participant.vars.get('outcome', {})
        payoff_plus = self.participant.payoff_plus_participation_fee()
        return {
            'bonus': self.player.bonus,
            'participated': participated,
            'outcome': outcome,
            'first_place': outcome.get('first_place', False),
            'second_place': outcome.get('second_place', False),
            'treatment': outcome.get('treatment', 'control'),
            'first_color': outcome.get('first_color', 'green'),
            'second_color': outcome.get('second_color', 'green'),
            'belief_payout': self.player.belief_payout,
            'performance_payout': self.player.performance_payout,
            'payoff': self.player.payoff,
            'payoff_plus_participation_fee': payoff_plus,
        }


page_sequence = [Start, PaymentInfo]
