import json

from django.http import JsonResponse
from django.views import View

from battle.models import NTF


class NTFView(View):
    def post(self, request, *args, **kwargs):
        if not request.body:
            ntf = NTF.objects.create()
            return JsonResponse({"ntfId": ntf.pk})
        try:
            data = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse(
                {
                    "error": "ValueError",
                }
            )
        ntf = NTF.objects.create(**data)
        return JsonResponse({"ntfId": ntf.pk})
