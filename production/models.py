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
import random, string, json, time
import numpy as np

author = 'Luca Drucker'

doc = """
Production stage
"""


# 1. Welcome
# 2. Instructions
# 3. 3 practice tasks
# 4. Instructions again + Consent
# 5. 3 min practice
# 6. 10 tasks for productivity
# 7. 15 min task for production
# 8. Goodbye, reminder to come back, details known tomorrow


class Constants(BaseConstants):
    name_in_url = 'part1'
    players_per_group = None
    num_rounds = 1
    tokens_per_task = 10

    # Task constants
    default_letters_per_word = 3

    # Task fixnum constants
    fixnum_use_timeout = True
    trytask_seconds = 120
    trytask_minutes = round(trytask_seconds/60)
    trytask_required_tasks = 1  # Number of tasks to familiarize with task
    productivity_seconds = 300
    productivity_minutes = round(productivity_seconds/60)
    productivity_required_tasks = 10  # Number of tasks to measure productivity

    # Task timed constants
    practice_use_timeout = True
    practice_seconds = 120
    practice_minutes = round(practice_seconds/60)
    production_use_timeout = True
    production_seconds = 900 # This will be the duration of the production part -- 15 min = 900 secs
    production_minutes = round(production_seconds/60)

    # Exogenous task length
    task_lengths = {
        1: 2,
        2: 3,
        3: 4
    }


class Subsession(BaseSubsession):
    dictionary = models.StringField()

    def creating_session(self):
        # Create task_lengh or ability treatment
        import itertools
        task_length_treatment = itertools.cycle([True, False])
        for player in self.get_players():
            player.task_length_treatment = next(task_length_treatment)

        # Create dictionary
        letters = list(string.ascii_uppercase)
        random.shuffle(letters)
        numbers = []
        N = list(range(100, 1000))
        for i in range(27):
            choice = random.choice(N)
            N.remove(choice)
            numbers.append(choice)
        d = [letters, numbers]
        dictionary = dict([(d[0][i], d[1][i]) for i in range(26)])
        self.dictionary = json.dumps(dictionary)

        self.session.vars['constant_values'] = {
            'task_lengths': Constants.task_lengths,
            'production_minutes': Constants.production_minutes,
            'productivity_required_tasks': Constants.productivity_required_tasks
        }
        s_constants = self.session.vars['constant_values']

        ps = self.get_players()
        for p in ps:
            p.participant.vars['task_length_treatment'] = p.task_length_treatment
            group = random.choice(list(Constants.task_lengths.keys())) \
                if p.participant.vars['task_length_treatment'] else ""
            p.participant.vars['completed'] = False
            p.participant.vars['prolific_id'] = ""
            p.participant.vars['own_group_id'] = ""
            p.participant.vars['spectator_group_id'] = ""
            p.participant.vars['time'] = ""
            p.participant.vars['components'] = dict(group=group,
                                                    production="",
                                                    tasks1min="",
                                                    group_mean_tasks1min="",
                                                    income="",
                                                    id_in_group="")
            p.participant.vars['start_time'] = ""
            p.participant.vars['end_time'] = ""
            p.participant.vars['gave_consent'] = ""
            p.participant.vars['completed_tasks_productivity'] = ""


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gave_consent = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No'],
        ],
        widget=widgets.RadioSelect,
        label="Do you wish to participate in the study?"
    )

    performance = models.IntegerField(initial=0, blank=True)
    mistakes = models.IntegerField(initial=0, blank=True)
    task_length_treatment = models.BooleanField()

    comprehension_check1 = models.IntegerField(
        label="When is the second part of the study?",
        choices = [
            [1, "Today."],
            [2, "Tomorrow."],
            [3, "In two days."],
        ],
        widget=widgets.RadioSelect
    )

    comprehension_check2 = models.IntegerField(
        label="If you only complete the first part, what will be your payment?",
        choices=[
            [1, "The completion bonus for the first part plus the payment after the number of tasks you do."],
            [2, "Only the completion bonus for the first part."],
            [3, "Nothing."],
        ],
        widget=widgets.RadioSelect
    )

    comprehension_check3 = models.IntegerField(
        label="How will you earn additional income on top of the completion bonuses?",
        choices=[
            [1, "The additional income will be based on the tasks you perform in the production stage"
                ", but will be determined by decisions in the second part."],
            [2, "The number of tasks you perform in the production stage will be your additional income."],
            [3, "The additional income will entirely be determined by luck."],
        ],
        widget=widgets.RadioSelect
    )

    def live_update_performance(self, data):
        own_id = self.id_in_group
        if 'performance' in data:
            perf = data['performance']
            self.performance = perf
            shuffle=False
            print('received ', perf, 'shuffle?', shuffle)
        else:
            shuffle=True
            print('received nothing, shuffle?', shuffle)
        answer = dict(performance = self.performance, shuffle=shuffle)
        return {own_id: answer}


def custom_export(players):
    # header row
    yield ['part1_session_code', 'part1_participant_code', 'prolific_id', 'gave_consent', 'completed_part1',
           'part1_start_time', 'part1_end_time', 'part1_completion_fee', 'task_length_treatment',
           'group', 'production', 'tasks1min', 'income', 'time', 'completed_tasks_productivity',
           'tasks_done_during_practice']

    # data
    for p in players:
        pp = p.participant
        ppvars = pp.vars
        ppcomps = ppvars['components']
        ps = p.session
        group = ppcomps.get('group', '')
        time = ppvars.get('time', '')
        task_length_treatment = ppvars.get('task_length_treatment', '')
        tasks_done_during_practice = ppvars.get('tasks_done_during_practice', '')
        # Add first_place and second_place to participant vars

        yield [ps.code, pp.code, pp.label, ppvars['gave_consent'],  ppvars['completed'], ppvars['start_time'],
               ppvars['end_time'], ps.config['participation_fee'], task_length_treatment,
               group, ppcomps['production'], ppcomps['tasks1min'], ppcomps['income'], time,
               ppvars['completed_tasks_productivity'], tasks_done_during_practice]
