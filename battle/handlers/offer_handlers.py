import json
from copy import deepcopy

from battle.models import NTF, User, Offer


def handle_offer_create(request: json) -> json:
    try:
        request: dict = json.loads(request)

    except ValueError:
        print("ValueError")
        return json.dumps(
            {
                "error": "ValueError",
            }
        )

    data = deepcopy(request)
    ntf_id = data.pop("ntfId", None)
    user_id = data.pop("userId", None)
    if not (ntf_id and user_id):
        return json.dumps(
            {
                "error": "KeyError",
            }
        )

    ntf = NTF.objects.filter(pk=ntf_id).first()
    if not ntf:
        return json.dumps(
            {
                "error": "ntfId Error",
            }
        )

    user = User.objects.filter(pk=user_id, ntf=ntf).first()
    if not user:
        return json.dumps(
            {
                "error": "ntfId or userId Error",
            }
        )
    offer = Offer.objects.create(user=user, **data)

    info = {"offerId": offer.pk}
    info.update(**request)
    return json.dumps(info)


def handle_offer_list() -> json:
    offers = list(
        Offer.objects.filter(is_active=True, is_archived=False).values(
            "id", "title"
        )
    )
    return json.dumps(offers)
