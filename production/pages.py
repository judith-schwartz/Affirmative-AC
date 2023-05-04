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
        ppvars['prolific_id'] = p.participant.label
        ppvars['start_time'] = datetime.datetime.now()

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
            'part1_completion_fee': config['participation_fee'],

            'letters_per_word' : Constants.task_lengths[ppcomps['group']] \
            if ppvars['task_length_treatment'] else Constants.default_letters_per_word,
            'mean_additional_income': 3,
        }


class TryTask(Page):
    live_method = 'live_update_performance'

    form_model = 'player'
    form_fields = ['performance', 'mistakes']
    if Constants.fixnum_use_timeout:
        timeout_seconds = Constants.trytask_seconds

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']

        letters_per_word = Constants.task_lengths[ppcomps['group']] \
            if ppvars['task_length_treatment'] else Constants.default_letters_per_word
        task_list = [j for j in range(letters_per_word)]
        legend_list = [j for j in range(26)]

        return {'legend_list': legend_list,
                'letters_per_word': letters_per_word,
                'task_list': task_list,
                }

    def before_next_page(self):
        print('Number of tasks done is', self.player.performance)


class Instructions2(Page):
    def vars_for_template(self):
        config = self.session.config
        num_lengths = len(Constants.task_lengths.keys())
        return {
            'part1_completion_fee': config['participation_fee'],

            'num_lengths': num_lengths,
            'currency_per_250_tokens': config['real_world_currency_per_point']*250
        }


class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['comprehension_check1',
                   'comprehension_check2',
                   'comprehension_check3',
                   'gave_consent']

    def error_message(self, values):
        solutions = dict(
            comprehension_check1=2,
            comprehension_check2=2,
            comprehension_check3=1,
        )
        error_messages=dict()
        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = 'Wrong answer. Try again!'

        return error_messages

    def before_next_page(self):
        ppvars = self.player.participant.vars
        ppvars['gave_consent'] = self.player.gave_consent

    def vars_for_template(self):
        config = self.session.config
        num_lengths = len(Constants.task_lengths.keys())
        return {
            'part1_completion_fee': config['participation_fee'],

            'num_lengths': num_lengths,
            'currency_per_250_tokens': config['real_world_currency_per_point']*250
        }


class NoConsent(Page):
    def is_displayed(self):
        return not self.player.gave_consent


class BeforePractice(Page):
    def is_displayed(self):
        return self.player.gave_consent

    def before_next_page(self):
        p = self.player
        p.performance = 0


class Practice(Page):
    live_method = 'live_update_performance'

    def is_displayed(self):
        return self.player.gave_consent

    form_model = 'player'
    form_fields = ['performance', 'mistakes']

    if Constants.practice_use_timeout:
        timeout_seconds = Constants.practice_seconds

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']

        letters_per_word = Constants.task_lengths[ppcomps['group']] \
            if ppvars['task_length_treatment'] else Constants.default_letters_per_word
        task_list = [j for j in range(letters_per_word)]
        legend_list = [j for j in range(26)]

        return {'legend_list': legend_list,
                'letters_per_word': letters_per_word,
                'task_list': task_list,
                }

    def before_next_page(self):
        p = self.player
        ppvars = p.participant.vars
        ppvars['tasks_done_during_practice'] = p.performance


class BeforeSpeed(Page):
    def is_displayed(self):
        return self.player.gave_consent

    def before_next_page(self):
        p = self.player
        p.performance = 0
        ppvars = p.participant.vars
        ppvars['expiry'] = time.time() + Constants.productivity_seconds
        print(ppvars['expiry'])


class MeasuringSpeed(Page):

    live_method = 'live_update_performance'

    def is_displayed(self):
        return self.player.gave_consent

    form_model = 'player'
    form_fields = ['performance', 'mistakes']

    if Constants.fixnum_use_timeout:
        timeout_seconds = Constants.productivity_seconds

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']

        letters_per_word = Constants.task_lengths[ppcomps['group']] \
            if ppvars['task_length_treatment'] else Constants.default_letters_per_word
        task_list = [j for j in range(letters_per_word)]
        legend_list = [j for j in range(26)]

        return {'legend_list': legend_list,
                'letters_per_word': letters_per_word,
                'task_list': task_list,
                }

    def before_next_page(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']
        s_constants = p.session.vars['constant_values']

        remained_time = ppvars['expiry'] - time.time()
        ppvars['time'] = round(Constants.productivity_seconds - remained_time, 4)
        ppvars['completed_tasks_productivity'] = p.performance
        if p.performance > 0:
            ppvars['components']['tasks1min'] = round(60/(ppvars['time']/ppvars['completed_tasks_productivity']), 3)
        else:
            ppvars['components']['tasks1min'] = 0

        if ppvars['completed_tasks_productivity'] < Constants.productivity_required_tasks:
            ppvars['cannot_continue'] = True
        else:
            ppvars['cannot_continue'] = False

        print('Completed tasks: ', ppvars['completed_tasks_productivity'],
              'in', round(ppvars['time'], 2), 'seconds.')


class EndOfStudy(Page):
    def is_displayed(self):
        p = self.player
        ppvars = p.participant.vars
        return ppvars['cannot_continue']


class BeforeProduction(Page):
    def is_displayed(self):
        p = self.player
        ppvars = p.participant.vars
        return p.gave_consent and not ppvars['cannot_continue']

    def vars_for_template(self):
        p = self.player
        p.performance = 0
        ppvars = p.participant.vars
        s_constants = p.session.vars['constant_values']
        ppcomps = ppvars['components']

        print('Components so far are', ppcomps)

        return {
            'tasks1min': ppcomps['tasks1min'],
        }


class Production(Page):

    live_method = 'live_update_performance'

    def is_displayed(self):
        p = self.player
        ppvars = p.participant.vars
        return p.gave_consent and not ppvars['cannot_continue']

    form_model = 'player'
    form_fields = ['performance', 'mistakes']
    if Constants.production_use_timeout:
        timeout_seconds = Constants.production_seconds

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppcomps = ppvars['components']

        letters_per_word = Constants.task_lengths[ppcomps['group']] \
            if ppvars['task_length_treatment'] else Constants.default_letters_per_word
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
        if p.performance is None:
            ppcomps['production'] = 0
        else:
            ppcomps['production'] = p.performance
        ppcomps['income'] = ppcomps['production'] * Constants.tokens_per_task

        print('Components so far are', ppcomps)


class EndOfFirstPart(Page):

    def is_displayed(self):
        p = self.player
        ppvars = p.participant.vars
        return p.gave_consent and not ppvars['cannot_continue']

    def vars_for_template(self):
        p = self.player
        ppvars = p.participant.vars
        ppvars['completed'] = True
        ppvars['end_time'] = datetime.datetime.now()
        print('Participant variables at the end of production session are', ppvars)
        print("Start time is", ppvars['start_time'], "end time is", ppvars['end_time'])
        print('Prolific ID is', p.participant.label)
        config = self.session.config

        return {
            'completion_url': config.get('prolific_completion_url', ''),
            'completion_code': config.get('prolific_completion_code', '')
        }


page_sequence = [Welcome,
                 Instructions,
                 TryTask,
                 Instructions2,
                 ConsentPage,
                 NoConsent,
                 BeforePractice,
                 Practice,
                 BeforeSpeed,
                 MeasuringSpeed,
                 EndOfStudy,
                 BeforeProduction,
                 Production,
                 EndOfFirstPart,
                 ]
