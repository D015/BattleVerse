#### 1. Установка зависимостей
```angular2html
pip install -r requirements.txt
```

#### 2. Запуск приложения на port 8008 (из директории где находится manager.py) 
```angular2html
daphne -p 8008 _config.asgi:application
```

Всё и API реализованно через ws:// (можно быстро дополнить http://)
PAPER = 1
SCISSORS = 2
STONE = 3
если 0 то будет рандомно
___
request
ws://127.0.0.1:8008/ntf_create {} или {"name": "the name", "description": "The description"}

response
{"ntfId": 15} или {"ntfId": 16, "name": "the name", "description": "The description"}
___
request
ws://127.0.0.1:8008/user_create {"ntfId": 15} или {"ntfId": 16, "username": "the username", "description": "The description"}

response
{"userId": 6, "ntfId": 15} или {"userId": 7, "ntfId": 16, "username": "the username", "description": "The description"}
___
request
ws://127.0.0.1:8008/battles_create {"userId": 6, "ntfId": 15}

response
{"offerId": 5, "userId": 6, "ntfId": 15, "title": "the title"}
___
request
ws://127.0.0.1:8008/battles_list

response
[{"id": 1, "title": ""}, {"id": 2, "title": ""}, {"id": 3, "title": ""}, {"id": 4, "title": ""}, {"id": 5, "title": "the title"}]
___
request
ws://127.0.0.1:8008/battles/accept {"offerId": 5, "ntfId": 16, "userId": 7}

response
{"acceptId": 2, "offerId": 5, "ntfId": 16, "userId": 7}
___
request
ws://127.0.0.1:8008/accept_list/0 список всех accept

response
[{"id": 1, "offer": 1}, {"id": 2, "offer": 5}]
___
request
ws://127.0.0.1:8008/accept_list/5 список accept по "offerId": 5

response
[{"id": 2}]
___
request
ws://127.0.0.1:8008/battles_start {"offerId": 5, "acceptId": 2}

response
{"battleId": 6, "offeror_point_start": 100, "acceptor_point_start": 100, "offeror_point_end": 100, "acceptor_point_end": 100, "offerId": 5, "acceptId": 2}
___
request
ws://127.0.0.1:8008/battles_move {"userId": 6, "battleId": 6, "choice": 3, "round": 1}

response
{"choices_are_complete": false}

{"offeror_choice": 3, "acceptor_choice": 1, "offeror_minus_point": -18, "acceptor_minus_point": 0, "offeror_point_end": 82, "acceptor_point_end": 100, "winner_round_userId": 7, "winner_battle_userId": null, "game_over": false, "choices_are_complete": true, "round": 1}
___
request
ws://127.0.0.1:8008/battles_move {"userId": 7, "battleId": 6, "choice": 1, "round": 1}

response
{"offeror_choice": 3, "acceptor_choice": 1, "offeror_minus_point": -18, "acceptor_minus_point": 0, "offeror_point_end": 82, "acceptor_point_end": 100, "winner_round_userId": 7, "winner_battle_userId": null, "game_over": false, "choices_are_complete": true, "round": 1}
___



