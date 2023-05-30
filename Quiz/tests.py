from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield SubmissionMustFail(
            pages.General, dict(q_age=11,
                                q_gender='Männlic',
                                q_study_level='Masterabschlus',
                                q_study_field='YOLO studies',
                                q_semester=-1,
                                q_n_experiment=-1,
                                q_abitur='abc',
                                q_math='xyz',
                                q_budget=-1,
                                q_spending=-1),
            error_fields=['q_age', 'q_gender', 'q_study_level', 
                   'q_semester', 'q_n_experiment', 
                   'q_abitur', 'q_math', 'q_budget', 'q_spending']
        )
        yield pages.General, dict(q_age=28,
                                  q_gender='Männlich',
                                  q_study_level='Masterabschluss',
                                  q_study_field='YOLO studies',
                                  q_semester=12,
                                  q_n_experiment=12,
                                  q_abitur=1,
                                  q_math=1,
                                  q_budget=10,
                                  q_spending=10)

        yield SubmissionMustFail(
            pages.Falk, dict(q_falk_risk=-1,
                             q_falk_time=-1,
                             q_falk_trust=-1,
                             q_falk_neg_rec=-1,
                             q_falk_pos_rec=-1,
                             q_falk_altruism=-1),
            error_fields=['q_falk_risk', 'q_falk_time',
                   'q_falk_trust', 'q_falk_neg_rec',
                   'q_falk_pos_rec', 'q_falk_altruism']
        )
        yield SubmissionMustFail(
            pages.Falk, dict(q_falk_risk=11,
                             q_falk_time=10,
                             q_falk_trust=11,
                             q_falk_neg_rec=11,
                             q_falk_pos_rec=0,
                             q_falk_altruism=1001),
            error_fields=['q_falk_risk', 
                   'q_falk_trust', 'q_falk_neg_rec',
                   'q_falk_altruism']
        )
        yield pages.Falk, dict(q_falk_risk=1,
                               q_falk_time=0,
                               q_falk_trust=10,
                               q_falk_neg_rec=6,
                               q_falk_pos_rec=3,
                               q_falk_altruism=500)