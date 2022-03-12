import json
from copy import deepcopy

from battle.models import NTF, User, Offer, Accept


def handle_accept_create(request: json) -> json:
    try:
        request: dict = json.loads(request)
    except ValueError:
        return json.dumps(
            {
                "error": "ValueError",
            }
        )

    data = deepcopy(request)

    ntf_id = data.pop("ntfId", None)
    user_id = data.pop("userId", None)
    offer_id = data.pop("offerId", None)
    if not (ntf_id and user_id and offer_id):
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

    offer = Offer.objects.get(pk=offer_id)
    if not offer:
        return json.dumps(
            {
                "error": "offerId Error",
            }
        )
    accept = Accept.objects.create(user=user, offer=offer, **data)

    info = {"acceptId": accept.pk}
    info.update(**request)
    return json.dumps(info)


def handle_accept_list(offer_pk: int = 0) -> json:
    if offer_pk:
        offer = Offer.objects.filter(pk=offer_pk).first()
        if offer:
            offer_accepts = list(
                offer.accept_set.filter(
                    is_active=True, is_archived=False
                ).values("id")
            )
            return json.dumps(offer_accepts)

    accepts = list(
        Accept.objects.filter(is_active=True, is_archived=False).values(
            "id", "offer"
        )
    )
    return json.dumps(accepts)
