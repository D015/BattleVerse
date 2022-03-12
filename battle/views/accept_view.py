import json

from django.http import JsonResponse
from django.views import View

from battle.models import User, NTF, Offer, Accept


class AcceptView(View):
    def post(self, request, *args, **kwargs):
        try:
            data: dict = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse(
                {
                    "error": "ValueError",
                }
            )
        ntf_id = data.get("ntfId")
        user_id = data.get("userId")
        offer_id = data.get("offerId")
        if not (ntf_id and user_id and offer_id):
            return JsonResponse(
                {
                    "error": "KeyError",
                }
            )

        ntf = NTF.objects.filter(pk=ntf_id).first()
        if not ntf:
            return JsonResponse(
                {
                    "error": "ntfId Error",
                }
            )

        user = User.objects.filter(pk=user_id, ntf=ntf).first()
        if not user:
            return JsonResponse(
                {
                    "error": "ntfId or userId Error",
                }
            )

        offer = Offer.objects.get(pk=offer_id)
        if not offer:
            return JsonResponse(
                {
                    "error": "offerId Error",
                }
            )
        accept = Accept.objects.create(user=user, offer=offer)
        return JsonResponse({"acceptId": accept.pk})

    def get(self, request, *args, **kwargs):
        offer_id = request["kwargs"]["pk"]
        offer = Offer.objects.get(pk=offer_id)
        offer_accepts = list(
            offer.accept_set.filter(is_active=True, is_archived=False).values(
                "id"
            )
        )
        return JsonResponse(offer_accepts, safe=False)
