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
import random, string, json, time, math, pickle
import numpy as np

author = 'Judith Schwartz'

doc = """
Endogenous Choice task
"""


# 1. Welcome
# 2. Instructions
# 3. Practice round (2 Min)
# 4. Belief elicitation
# 5. Instructions 2
# 6. Production
# 7. Tournament decision
# 8. Belief elicitation
# 9. Matching
# 10. Bonus distribution (own group)
# 11. Bonus distribution (other groups)


class Constants(BaseConstants):
    name_in_url = 'single'
    players_per_group = None
    num_rounds = 1
    tokens_per_task = 10

    # Task constants
    default_letters_per_word = 3

    # Task fixnum constants
    fixnum_use_timeout = True
    trytask_seconds = 60
    trytask_minutes = round(trytask_seconds / 60)
    trytask_required_tasks = 1  # Number of tasks to familiarize with task
    productivity_seconds = 60
    productivity_minutes = round(productivity_seconds / 60)
    productivity_required_tasks = 1  # Number of tasks to measure productivity

    # Task timed constants
    practice_use_timeout = True
    practice_seconds = 60
    practice_minutes = round(practice_seconds / 60)
    production_use_timeout = True
    production_seconds = 60  # This will be the duration of the production part -- 15 min = 900 secs
    production_minutes = round(production_seconds / 60)

    # Affirmative action
    color = {
        0: "blue",
        1: "green"
    }

    # Tournament

    # Tournament presentation

    # Exogenous task length
    task_lengths = 3

    # Roles
    FIRST_ROLE = 'Erster Platz'
    SECOND_ROLE = 'Zweiter Platz'
    LOST_ROLE = 'Nicht gewonnen'


class Subsession(BaseSubsession):
    dictionary = models.StringField()

    def creating_session(self):
        # Create control
        import itertools
        control = itertools.cycle([True, False])  # subject
        for player in self.get_players():
            player.control_treatment = next(control)

        # Sort into control and treatment group (tournament participation)
        control_group = []
        treat_group = []
        for player in self.get_players():
            if player.control_treatment:
                control_group.append(player)
            else:
                treat_group.append(player)

        # Sort into affirmative action (green)
        control_green = control_group[:len(control_group)//2]
        for player in control_group:
            if player in control_green:
                player.green = True
            else:
                player.green = False

        treat_green = treat_group[:len(treat_group)//2]
        for player in treat_group:
            if player in treat_green:
                player.green = True
            else:
                player.green = False

        # Presentation of tournament
        random.shuffle(control_group)
        random.shuffle(treat_group)

        tournament = control_group[:len(control_group) // 2]
        for player in control_group:
            if player in tournament:
                player.control_first = True
            else:
                player.control_first = False

        tournament = treat_group[:len(treat_group) // 2]
        for player in treat_group:
            if player in tournament:
                player.control_first = True
            else:
                player.control_first = False


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
            group = Constants.task_lengths
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
    def tournament_outcome(self):
        # Create list of tournament participants
        control_green = []
        control_blue = []
        treat_green = []
        treat_blue = []
        control_green_performance = []
        control_blue_performance = []
        treat_green_performance = []
        treat_blue_performance = []
        all_players = self.get_players()
        # get a list of all players that want to participate in the tournaments sorted by colour
        for p in all_players:
            if p.green:
                if p.part_control and p.control_treatment:
                    control_green.append(p)
                    control_green_performance.append(p.performance_production)
                elif p.part_treat and not p.control_treatment:
                    treat_green.append(p)
                    treat_green_performance.append(p.performance_production)
            else:
                if p.part_control and p.control_treatment:
                    control_blue.append(p)
                    control_blue_performance.append(p.performance_production)
                elif p.part_treat and not p.control_treatment:
                    treat_blue.append(p)
                    treat_blue_performance.append((p.performance_production))

        # list of tounament outcomes
        outcome_tuple_green_treat = list(zip(treat_green_performance, treat_green))
        outcome_tuple_green_control = list(zip(control_green_performance, control_green))
        outcome_tuple_blue_treat = list(zip(treat_blue_performance, treat_blue))
        outcome_tuple_blue_control = list(zip(control_blue_performance, control_blue))

        # get groups and ranking
        for p in all_players:
            if p.part_control and p.control_treatment:
                group = []

                random.shuffle(outcome_tuple_blue_control)
                random.shuffle(outcome_tuple_green_control)
                # group should consist of 2 blue & 2 green
                group.append((p.performance_production, p))
                if p.green:
                    if len(outcome_tuple_green_control) < 2:
                        green_players = [x for x in outcome_tuple_green_treat if x not in group][
                                        :2 - len(outcome_tuple_green_control)]
                        blue_players = [x for x in outcome_tuple_blue_control if x not in group][
                                       :2 - len(outcome_tuple_blue_control)]
                    else:
                        green_players = [x for x in outcome_tuple_green_control if x not in group][:1]
                        blue_players = [x for x in outcome_tuple_blue_control if x not in group][:2]
                    group.extend(green_players)
                    group.extend(blue_players)
                else:
                    if len(outcome_tuple_blue_control) < 2:
                        blue_players = [x for x in outcome_tuple_blue_treat if x not in group][
                                       :2 - len(outcome_tuple_blue_control)]
                        green_players = [x for x in outcome_tuple_green_control if x not in group][
                                        :2 - len(outcome_tuple_green_control)]
                    else:
                        blue_players = [x for x in outcome_tuple_blue_control if x not in group][:1]
                        green_players = [x for x in outcome_tuple_green_control if x not in group][:2]
                    group.extend(blue_players)
                    group.extend(green_players)

                # Sort the group by performance (highest to lowest)
                group.sort(key=lambda x: x[0], reverse=True)

                # check ranking for doubles
                ranks = {}
                rank = 1
                for performance, player in group:
                    if performance in ranks:
                        player.rank = ranks[performance]
                    else:
                        player.rank = rank
                        ranks[performance] = rank
                        rank += 1

                # Assign the ranking based on the sorted player list
                ranks = {}
                for i, (performance, player) in enumerate(group):
                    rank = i + 1
                    while rank in ranks.values():
                        rank += 1
                    ranks[player] = rank
                    if player == p:
                        if rank == 1:
                            player.first_place = True
                        elif rank == 2:
                            player.second_place = True
                        elif rank == 3:
                            player.third_place = True
                        else:
                            player.fourth_place = True

                print(ranks)



            # tournament ranking under affirmative action
            elif p.part_treat and not p.control_treatment:
                group = []

                random.shuffle(outcome_tuple_green_treat)
                random.shuffle(outcome_tuple_blue_treat)
                # group should consist of 2 blue & 2 green
                group.append((p.performance_production, p))

                if p.green:
                    if len(outcome_tuple_green_treat) < 2:
                        green_players = [x for x in outcome_tuple_green_control if x not in group][
                                        :2 - len(outcome_tuple_green_treat)]
                        blue_players = [x for x in outcome_tuple_blue_treat if x not in group][
                                       :2 - len(outcome_tuple_blue_treat)]
                    else:
                        green_players = [x for x in outcome_tuple_green_treat if x not in group][:1]
                        blue_players = [x for x in outcome_tuple_blue_treat if x not in group][:2]
                    group.extend(green_players)
                    group.extend(blue_players)


                else:

                    if len(outcome_tuple_blue_treat) < 2:

                        blue_players = [x for x in outcome_tuple_blue_control if x not in group][
                                       :2 - len(outcome_tuple_blue_treat)]
                        green_players = [x for x in outcome_tuple_green_treat if x not in group][:2]

                        if len(blue_players) < 2:
                            blue_players.extend([x for x in outcome_tuple_blue_treat if x not in group][
                                                :2 - len(blue_players)])

                    else:

                        blue_players = [x for x in outcome_tuple_blue_treat if x not in group][:1]
                        green_players = [x for x in outcome_tuple_green_treat if x not in group][:2]

                    group.extend(blue_players)
                    group.extend(green_players)


                # Sort the group based on performance

                group.sort(key=lambda x: x[0], reverse=True)

                # Assign the ranking based on the sorted player list
                green_players = [player for _, player in group if player.green]

                green_players.sort(key=lambda x: x.performance_production, reverse=True)


                for rank, player in enumerate(green_players):
                    if p == player:
                        if rank < len(green_players)-1:
                            p.first_place = True

                other_players = [player for _, player in group if not player.first_place]
                other_players.sort(key=lambda x: x.performance_production, reverse=True)
                for rank, player in enumerate(other_players):
                    if p == player:
                        if rank == 0:
                            p.second_place = True
                        elif rank == 1:
                            p.third_place = True
                        else:
                            p.fourth_place = True




class Player(BasePlayer):
    performance_practice = models.IntegerField(initial=0, blank=True)
    mistakes_practice = models.IntegerField(initial=0, blank=True)
    performance_production = models.IntegerField(initial=0, blank=True)
    mistakes_production = models.IntegerField(initial=0, blank=True)

    # Random variables
    control_treatment = models.BooleanField()
    green = models.BooleanField()
    control_first = models.BooleanField()
    # Tournament participation
    part_control = models.BooleanField(
        label="",
        widget=widgets.RadioSelect
    )
    part_treat = models.BooleanField(
        label="",
        widget=widgets.RadioSelect
    )

    rank = models.IntegerField()
    first_place = models.BooleanField()
    second_place = models.BooleanField()
    third_place = models.BooleanField()
    fourth_place = models.BooleanField()

    #tournament_outcome = {}

    #Belief Elicitation
    belief_performance1 = models.IntegerField(initial=0,
                                              label="Wie viele Aufgaben haben Sie korrekt gelöst?",
                                              min=0,
                                              max=500)
    belief_relative1 = models.IntegerField(initial=0,
                                           label="Wie viele Aufgaben mehr oder weniger haben Sie im Vergleich zum Durchschnitt korrekt gelöst?",
                                           min = -200,
                                           max = 200)
    belief_performance2 = models.IntegerField(initial=0,
                                              label="Wie viele Aufgaben haben Sie korrekt gelöst?",
                                              min=0,
                                              max=500
                                              )
    belief_relative2 = models.IntegerField(initial=0,
                                           label="Wie viele Aufgaben mehr oder weniger haben Sie im Vergleich zum Durchschnitt korrekt gelöst?",
                                           min = -200,
                                           max = 200)

    comprehension_check1 = models.IntegerField(
        label="When is the second part of the study?",
        choices=[
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

    def live_update_performance_practice(self, data):
        own_id = self.id_in_group
        if 'performance_practice' in data:
            perf = data['performance_practice']
            self.performance_practice = perf
            shuffle = False
            print('received ', perf, 'shuffle?', shuffle)
        else:
            shuffle = True
            print('received nothing, shuffle?', shuffle)
        answer = dict(performance_practice=self.performance_practice, shuffle=shuffle)
        return {own_id: answer}

    def live_update_performance_production(self, data):
        own_id = self.id_in_group
        if 'performance_production' in data:
            perf = data['performance_production']
            self.performance_production = perf
            shuffle = False
            print('received ', perf, 'shuffle?', shuffle)
        else:
            shuffle = True
            print('received nothing, shuffle?', shuffle)
        answer = dict(performance_production=self.performance_production, shuffle=shuffle)
        return {own_id: answer}


def custom_export(players):
    # header row
    yield ['part1_session_code', 'part1_participant_code', 'prolific_id', 'completed_part1',
           'part1_start_time', 'part1_end_time', 'part1_completion_fee',
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
        # task_length_treatment = ppvars.get('task_length_treatment', '')
        tasks_done_during_practice = ppvars.get('tasks_done_during_practice', '')
        yield [ps.code, pp.code, pp.label, ppvars['completed'], ppvars['start_time'],
               ppvars['end_time'], ps.config['participation_fee'], task_length_treatment,
               group, ppcomps['production'], ppcomps['tasks1min'], ppcomps['income'], time,
               ppvars['completed_tasks_productivity'], tasks_done_during_practice]
