import json
from copy import deepcopy
from random import randint

from battle.constants import POINT_START
from battle.models import Offer, Battle, User, Round
from battle.models.round_ import RoundChoices
from battle.utils import play_round, process_round_result


def handle_battle_create(request: json) -> json:
    try:
        request: dict = json.loads(request)
    except ValueError:
        return json.dumps(
            {
                "error": "ValueError",
            }
        )

    data = deepcopy(request)

    offer_id = data.pop("offerId", None)
    accept_id = data.pop("acceptId", None)
    if not (accept_id and offer_id):
        return json.dumps(
            {
                "error": "KeyError",
            }
        )

    offer = Offer.objects.filter(pk=offer_id).first()
    if not offer:
        return json.dumps(
            {
                "error": "offerId Error",
            }
        )

    accept = offer.accept_set.filter(pk=accept_id).first()
    if not accept:
        return json.dumps(
            {
                "error": "offerId or acceptId Error",
            }
        )

    battle = Battle.objects.create(
        accept=accept,
        offeror_point_start=POINT_START,
        acceptor_point_start=POINT_START,
        offeror_point_end=POINT_START,
        acceptor_point_end=POINT_START,
    )
    info = {
        "battleId": battle.pk,
        "offeror_point_start": battle.offeror_point_start,
        "acceptor_point_start": battle.acceptor_point_start,
        "offeror_point_end": battle.offeror_point_end,
        "acceptor_point_end": battle.acceptor_point_end,
    }

    info.update(**request)
    return json.dumps(info)


def handle_battle_mover(request: json, the_websocket: str) -> dict:
    try:
        data: dict = json.loads(request)
    except ValueError:
        return {"error": "ValueError"}
    user_id = data.get("userId")
    battle_id = data.get("battleId")
    choice = data.get("choice")
    round_number = data.get("round")

    if (
        user_id is None
        or battle_id is None
        or choice is None
        or round_number is None
    ):
        return {"error": "KeyError"}

    if not min(RoundChoices) <= choice <= max(RoundChoices):
        return {"error": "choice Error"}

    user = User.objects.filter(pk=user_id).first()
    if not user:
        return {"error": "userId Error"}

    battle = Battle.objects.filter(
        pk=battle_id, is_active=True, is_archived=False
    ).first()
    if not battle:
        return {"error": "battleId Error"}
    choice = (
        choice if choice else randint(min(RoundChoices), max(RoundChoices))
    )

    if not choice:
        data["choice"] = randint(min(RoundChoices), max(RoundChoices))

    round_dict = {}
    if user == battle.accept.user:
        round_dict.update(
            {"acceptor_choice": choice, "acceptor_websocket": the_websocket}
        )
    elif user == battle.accept.offer.user:
        round_dict.update(
            {"offeror_choice": choice, "offeror_websocket": the_websocket}
        )
    else:
        return {"error": "userId Error"}

    round_, _ = Round.objects.get_or_create(
        number=round_number, battle=battle
    )
    Round.objects.filter(pk=round_.pk).update(**round_dict)
    round_ = Round.objects.get(pk=round_.pk)

    round_offeror_choice = round_.offeror_choice
    round_acceptor_choice = round_.acceptor_choice
    if round_offeror_choice and round_acceptor_choice:
        round_result = play_round(
            offeror_choice=round_offeror_choice,
            acceptor_choice=round_acceptor_choice,
        )

        Round.objects.filter(pk=round_.pk).update(**round_result)

        data_round_result = process_round_result(
            round_result=round_result, round_=round_
        )
        round_ = Round.objects.get(pk=round_.pk)
        data_round_result.update(
            {
                "choices_are_complete": True,
                "round": round_number,
                "offeror_websocket": round_.offeror_websocket,
                "acceptor_websocket": round_.acceptor_websocket,
             }
        )

        return data_round_result

    return {"choices_are_complete": False}


