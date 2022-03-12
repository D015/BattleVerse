import json
from copy import deepcopy

from battle.models import NTF, User


def handle_user_create(request: json) -> json:
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
    if not ntf_id:

        return json.dumps(
            {
                "error": "KeyError",
            }
        )

    ntf = NTF.objects.filter(pk=ntf_id).first()
    user_is_exist = User.objects.filter(ntf=ntf).exists()
    if not ntf or user_is_exist:
        return json.dumps(
            {
                "error": "ntfId Error",
            }
        )
    user = User.objects.create(ntf=ntf, **data)
    info = {"userId": user.pk}
    info.update(**request)
    return json.dumps(info)
