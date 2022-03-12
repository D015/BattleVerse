import json

from django.http import JsonResponse
from django.views import View

from battle.models import User, NTF


class UserView(View):
    def post(self, request, *args, **kwargs):
        try:
            data: dict = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse(
                {
                    "error": "ValueError",
                }
            )

        ntf_id = data.pop("ntfId", None)
        if not ntf_id:
            return JsonResponse(
                {
                    "error": "KeyError",
                }
            )

        data["ntf"] = NTF.objects.filter(pk=ntf_id).first()
        user_is_exist = User.objects.filter(ntf=data["ntf"]).exists()
        if not data["ntf"] or user_is_exist:
            return JsonResponse(
                {
                    "error": "ntfId Error",
                }
            )
        user = User.objects.create(**data)
        return JsonResponse({"userId": user.pk})
