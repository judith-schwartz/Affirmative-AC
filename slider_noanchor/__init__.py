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
    bonus0 = models.FloatField(initial=-1)
    bonus1 = models.FloatField(initial=-1)
    bonus2 = models.FloatField(initial=-1)
    bonus3 = models.FloatField(initial=-1)
    bonus4 = models.FloatField(initial=-1)
    bonus5 = models.FloatField(initial=-1)
    bonus6 = models.FloatField(initial=-1)


# PAGES
class Start(Page):
    def vars_for_template(self):
        participated = self.participant.vars.get('Participated', False)
        return {
            'participated': participated
        }

class SliderPage(Page):
    form_model = 'player'
    form_fields = ['bonus0']

    def is_displayed(self):
        return self.participant.vars.get('Participated', False)

    def vars_for_template(self):
        # Access the outcome variable from participant vars
        outcome = self.participant.vars.get('outcome')

        # Check if the outcome variable exists
        if outcome:
            first_color = outcome.get('first_color')
            second_color = outcome.get('second_color')
            treatment = outcome.get('treatment')
            first_place = outcome.get('first_place')
            second_place = outcome.get('second_place')
            green = outcome.get('green')
        else:
            # Set default values when outcome is not available
            first_color = None
            second_color = None
            treatment = None
            first_place = None
            second_place = None
            green = None

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

            # If the participant has an outcome, append it to selected outcomes
            if 'outcome' in self.participant.vars:
                selected_outcomes.append(self.participant.vars['outcome'])
            else:
                # Player does not have an outcome, handle the case
                selected_outcomes.append({})  # Add an empty dictionary as a placeholder

            # Store the outcomes in form field variables and participant var
            for i, outcome in enumerate(selected_outcomes):
                if i == 0:
                    bonus = getattr(self, 'bonus0')
                    if bonus == -1:
                        outcome['bonus'] = -1
                    else:
                        outcome['bonus'] = bonus
                else:
                    bonus = getattr(self, f'bonus{i}')
                    outcome['bonus'] = bonus

            # Save the selected outcomes back to the participant vars
            self.participant.vars['selected_outcomes'] = selected_outcomes
class Results(Page):
    pass


page_sequence = [Start, SliderPage,
                 AdditionalSliderPage]
