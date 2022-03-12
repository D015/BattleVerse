import json


from django.http import JsonResponse
from django.views import View

from battle.models import User, NTF, Offer


class OfferView(View):
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
        if not (ntf_id and user_id):
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
        offer = Offer.objects.create(user=user)
        return JsonResponse({"offerId": offer.pk})

    def get(self, request, *args, **kwargs):
        offers = list(
            Offer.objects.filter(is_active=True, is_archived=False).values(
                "id", "title"
            )
        )
        return JsonResponse(offers, safe=False)
