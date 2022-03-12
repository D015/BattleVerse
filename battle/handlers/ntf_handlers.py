import json

from battle.models import NTF


def handle_ntf_create(request: json) -> json:
    if not request:
        ntf = NTF.objects.create()
        return json.dumps({"ntfId": ntf.pk})
    try:
        data = json.loads(request)
    except ValueError:
        return json.dumps(
            {
                "error": "ValueError",
            }
        )

    ntf = NTF.objects.create(**data)
    info = {"ntfId": ntf.pk}
    info.update(**data)
    return json.dumps(info)
