from random import randint

from battle.constants import MINUS_POINT
from battle.models.round_ import RoundChoices, Round


def play_round(offeror_choice: int, acceptor_choice: int) -> dict:
    result = {
        "offeror_choice": offeror_choice, "acceptor_choice": acceptor_choice
    }

    if offeror_choice == acceptor_choice:
        result.update({
            "offeror_minus_point": 0,
            "acceptor_minus_point": 0,
        }
        )
        return result

    minus_point = -(randint(min(MINUS_POINT), max(MINUS_POINT)))
    choice_difference = offeror_choice - acceptor_choice
    choice_difference_abs = abs(choice_difference)
    choices_mim_max_difference = max(RoundChoices) - min(RoundChoices)

    if (
            choice_difference > 0
            and choice_difference_abs != choices_mim_max_difference
            or choice_difference < 0
            and choice_difference_abs == choices_mim_max_difference
    ):
        result.update(
            {"offeror_minus_point": 0, "acceptor_minus_point": minus_point}
        )
        return result

    result.update(
        {"offeror_minus_point": minus_point, "acceptor_minus_point": 0}
    )
    return result


def process_round_result(round_result: dict, round_: Round) -> dict:
    offeror_minus_point = round_result["offeror_minus_point"]
    acceptor_minus_point = round_result["acceptor_minus_point"]
    if not offeror_minus_point and not acceptor_minus_point:
        round_result.update(
            {
                "offeror_point_end": round_.battle.offeror_point_end,
                "acceptor_point_end": round_.battle.acceptor_point_end,
                "winner_round_userId": None,
                "winner_battle_userId": None,
                "game_over": not round_.battle.is_active,
            }
        )
        return round_result

    if offeror_minus_point:
        round_.winner = round_.battle.accept.user
        round_.offeror_minus_point = offeror_minus_point
        if round_.battle.offeror_point_end <= -offeror_minus_point:
            round_.battle.offeror_point_end = 0
            round_.battle.winner = round_.battle.accept.user
            round_.battle.is_active = False
        else:
            round_.battle.offeror_point_end += offeror_minus_point

    if acceptor_minus_point:
        round_.winner = round_.battle.accept.offer.user
        round_.acceptor_minus_point = acceptor_minus_point
        if round_.battle.acceptor_point_end <= -acceptor_minus_point:
            round_.battle.acceptor_point_end = 0
            round_.battle.winner = round_.battle.accept.offer.user
            round_.battle.is_active = False
        else:
            round_.battle.acceptor_point_end += acceptor_minus_point

    round_.save()
    round_.battle.save()

    if round_.winner:
        winner_round_user_pk = round_.winner.pk
    else:
        winner_round_user_pk = None
    if round_.battle.winner:
        winner_battle_user_pk = round_.battle.winner.pk
    else:
        winner_battle_user_pk = None

    round_result.update(
        {
            "offeror_point_end": round_.battle.offeror_point_end,
            "acceptor_point_end": round_.battle.acceptor_point_end,
            "winner_round_userId": winner_round_user_pk,
            "winner_battle_userId": winner_battle_user_pk,
            "game_over": not round_.battle.is_active,
        }
    )
    return round_result





