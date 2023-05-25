import random

from otree.api import *


doc = """
Slider example
"""


class Constants(BaseConstants):
    name_in_url = "slider"
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bonus0 = models.FloatField()
    bonus1 = models.FloatField()
    bonus2 = models.FloatField()
    bonus3 = models.FloatField()
    bonus4 = models.FloatField()
    bonus5 = models.FloatField()
    bonus6 = models.FloatField()



# PAGES
class SliderPage(Page):
    form_model = 'player'
    form_fields = ['bonus0']

    def vars_for_template(self):
        # Access the outcome variable from participant vars
        outcome = self.participant.vars['outcome']
        print(outcome)

        # Access individual entries in the outcome dictionary
        first_color = outcome['first_color']
        second_color = outcome['second_color']
        treatment = outcome['treatment']
        first_place = outcome['first_place']
        second_place = outcome['second_place']
        green = outcome['green']

        return {
            'first_color': first_color,
            'second_color': second_color,
            'treatment': treatment,
            'first_place': first_place,
            'second_place': second_place,
            'green': green
         }

class AdditionalSliderPage(Page):
    form_model = 'player'
    form_fields = ['bonus1', 'bonus2', 'bonus3', 'bonus4', 'bonus5', 'bonus6']

    def vars_for_template(self):
        # Fetch the list of all outcomes
        all_outcomes = self.participant.vars['all_outcomes']
        selected_outcomes = []

        # If there are less than 6 outcomes, duplicate them until we have at least 6
        while len(all_outcomes) < 6:
            all_outcomes += all_outcomes

        while len(selected_outcomes) < 6:
            # Randomly choose an outcome
            outcome = random.choice(all_outcomes)

            # Add the chosen outcome to selected_outcomes
            selected_outcomes.append(outcome)

            # Remove the chosen outcome from all_outcomes
            all_outcomes.remove(outcome)

        # Save the selected outcomes back to the participant vars
        self.participant.vars['selected_outcomes'] = selected_outcomes

        # Now create a dictionary for each selected outcome's details
        outcome_vars = {}
        for i, outcome in enumerate(selected_outcomes, start=1):
            outcome_vars[f'first_color{i}'] = outcome['first_color']
            outcome_vars[f'second_color{i}'] = outcome['second_color']
            outcome_vars[f'treatment{i}'] = outcome['treatment']

        return outcome_vars

    def before_next_page(self, timeout_happened):
        if not timeout_happened:
            # Get the selected outcomes from participant.vars
            selected_outcomes = self.participant.vars.get('selected_outcomes', [])

            # Append participant's outcome to selected outcomes
            selected_outcomes.append(self.participant.vars['outcome'])

            # store the outcomes in formfield variables and participant var
            for i in range(min(7, len(selected_outcomes))):  # Adjust range to allow for the additional outcome
                bonus = getattr(self, f'bonus{i}')
                selected_outcomes[i]['bonus'] = bonus  # store the bonus in the selected outcomes

            # Save the selected outcomes back to the participant vars
            self.participant.vars['selected_outcomes'] = selected_outcomes

class Results(Page):
    pass


page_sequence = [SliderPage,
                 AdditionalSliderPage,
                 Results]
