from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import gauss
import time, datetime, random, pytz
import numpy as np

""" class DateChecker(Page):
    def vars_for_template(self):
        config = self.session.config
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        hours_to_add = int(config['hours_to_utc'])
        start_date = datetime.datetime(int(config['start_year']),
                                       int(config['start_month']),
                                       int(config['start_day']),
                                       int(config['start_hour']),
                                       int(config['start_min']))
        naive_start_date_in_utc = start_date + datetime.timedelta(hours=hours_to_add)
        utc_start_date = pytz.timezone("UTC").localize(naive_start_date_in_utc)
        end_date = datetime.datetime(int(config['end_year']),
                                     int(config['end_month']),
                                     int(config['end_day']),
                                     int(config['end_hour']),
                                     int(config['end_min']))
        naive_end_date_in_utc = end_date + datetime.timedelta(hours=hours_to_add)
        utc_end_date = pytz.timezone("UTC").localize(naive_end_date_in_utc)
        not_yet_open = utc_now < utc_start_date
        now_open = (utc_start_date <= utc_now < utc_end_date)
        closed = utc_end_date <= utc_now
        open_time = start_date.strftime("%Y-%m-%d %H:%M:%S")
        close_time = end_date.strftime("%Y-%m-%d %H:%M:%S")

        return{
            'open': now_open,
            'not_yet_open': not_yet_open,
            'closed': closed,
            'open_time': open_time,
            'close_time': close_time
        }"""


class Welcome(Page):
    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        config = self.session.config
        ppvars = p.participant.vars
        ppcomps = ppvars['components']
        ppvars['start_time'] = datetime.datetime.now()
        return {
            'participation_fee': config['participation_fee'],
        }

    def before_next_page(self):
        p = self.player
        ppvars = p.participant.vars
        print("ID in ppvars is:", ppvars['prolific_id'], "Completed:", ppvars['completed'])
        print("Prolific ID as label is:", p.participant.label)


class Instructions(Page):
    def vars_for_template(self):
        config = self.session.config
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']
        return {
            'participation_fee': config['participation_fee'],

            'letters_per_word': Constants.default_letters_per_word,
            'mean_additional_income': 3,
        }


class Practice(Page):
    live_method = 'live_update_performance_practice'

    form_model = 'player'
    form_fields = ['performance_practice', 'mistakes_practice']

    if Constants.practice_use_timeout:
        timeout_seconds = Constants.practice_seconds

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']

        letters_per_word = Constants.default_letters_per_word
        task_list = [j for j in range(letters_per_word)]
        legend_list = [j for j in range(26)]

        return {'legend_list': legend_list,
                'letters_per_word': letters_per_word,
                'task_list': task_list,
                }

    def before_next_page(self):
        p = self.player
        ppvars = p.participant.vars
        ppvars['tasks_done_during_practice'] = p.performance_practice


class FirstBeliefElicitation(Page):
    form_model = 'player'
    form_fields = ['belief_performance1', 'belief_relative1']


class BeforeProduction(Page):

    def vars_for_template(self):
        p = self.player
        p.performance_production = 0  # nicht unbedingt notwendig
        ppvars = p.participant.vars
        s_constants = p.session.vars['constant_values']
        ppcomps = ppvars['components']

        print('Components so far are', ppcomps)

        return {
            'tasks1min': ppcomps['tasks1min'],
        }


class Production(Page):
    live_method = 'live_update_performance_production'

    form_model = 'player'
    form_fields = ['performance_production', 'mistakes_production']
    if Constants.production_use_timeout:
        timeout_seconds = Constants.production_seconds

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']

        letters_per_word = Constants.default_letters_per_word
        task_list = [j for j in range(letters_per_word)]
        legend_list = [j for j in range(26)]

        return {'legend_list': legend_list,
                'letters_per_word': letters_per_word,
                'task_list': task_list,
                }

    def before_next_page(self):
        p = self.player
        ppvars = p.participant.vars
        s_constants = p.session.vars['constant_values']
        ppcomps = ppvars['components']
        if p.performance_production is None:
            ppcomps['production'] = 0
        else:
            ppcomps['production'] = p.performance_production
        ppcomps['income'] = ppcomps['production'] * Constants.tokens_per_task

        print('Components so far are', ppcomps)


class BeforeTournament(WaitPage):
    after_all_players_arrive = 'tournament_group'


class Tournament(Page):
    form_model = 'player'
    form_fields = ['part_control', 'part_treat']

    def vars_for_template(self):
        p = self.player
        pcontrol = p.control_treatment
        pgreen = p.green
        pcontrol_first = p.control_first

        return {'pcontrol': pcontrol,
                'pgreen': pgreen,
                'pcontrol_first': pcontrol_first,
                }


class SecondBeliefElicitation(Page):
    form_model = 'player'
    form_fields = ['belief_performance2', 'belief_relative2']


class BeforeBonus(WaitPage):
    after_all_players_arrive = 'tournament_outcome'

    #before_next_page = 'set_outcome'


class Bonus(Page):
    form_model = 'player'
    form_fields = 'bonus'


page_sequence = [Welcome,
                 Instructions,
                 Practice,
                 FirstBeliefElicitation,
                 BeforeProduction,
                 Production,
                 BeforeTournament,
                 Tournament,
                 SecondBeliefElicitation,
                 BeforeBonus#,
                 #Bonus

                 ]
