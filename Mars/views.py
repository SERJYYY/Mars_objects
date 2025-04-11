from django.shortcuts import render
from django.http import Http404

# Коллекция услуг
objects = [
    {
        'id': 1,
        'title': 'Вулкан Олимп',
        'image_url': 'http://localhost:9000/images/1.jpg',
        'description': 'Самый высокий вулкан в Солнечной системе, достигающий высоты около 22 км.'
    },
    {
        'id': 2,
        'title': 'Долины Маринер',
        'image_url': 'http://localhost:9000/images/2.jpg',
        'description': 'Огромная система каньонов, протянувшаяся более чем на 4000 км.'
    },
    {
        'id': 3,
        'title': 'Кратер Гейла',
        'image_url': 'http://localhost:9000/images/3.jpg',
        'description': 'Кратер диаметром 154 км, где проводились исследования марсоходом Curiosity.'
    },
    {
        'id': 4,
        'title': 'Южная полярная шапка',
        'image_url': 'http://localhost:9000/images/4.jpg',
        'description': 'Обширный ледяной регион, содержащий замёрзший углекислый газ и воду.'
    },
    {
        'id': 5,
        'title': 'Северная полярная шапка',
        'image_url': 'http://localhost:9000/images/5.jpg',
        'description': 'Ледяной покров в северной части Марса, меняющий форму в зависимости от сезона.'
    },
]

# Заявки
requests_data = {
    1: {
        'name': 'Заявка на экскурсию',
        'status': 'успех',
        'rover': 'Марсоход «Curiosity»',
        'services': [1, 2]
    },
    2: {
        'name': 'Исследование кратера',
        'status': 'работает',
        'rover': 'Марсоход «Perseverance»',
        'services': [3, 5]
    },
}

# Список марсоходов
rovers = [
    "Марсоход «Perseverance»",
    "Марсоход «Curiosity»",
    "Посадочный модуль «InSight»",
    "Орбитальный аппарат «Mars Reconnaissance Orbiter»",
    "Орбитальный аппарат «ExoMars Trace Gas Orbiter»",
    "Орбитальный аппарат «MAVEN»",
    "Китайский марсоход «Чжужун»"
]


def home(request):
    query = request.GET.get('q', '').lower()
    filtered = [obj for obj in objects if query in obj['title'].lower()]
    return render(request, 'home.html', {
        'objects': filtered,
        'query': request.GET.get('q', '')
    })


def service_detail(request, object_id):
    obj = next((o for o in objects if o['id'] == object_id), None)
    if not obj:
        raise Http404("Объект не найден")
    return render(request, 'detail.html', {'obj': obj})


def view_request(request, request_id):
    data = requests_data.get(request_id)
    if not data:
        raise Http404("Заявка не найдена")

    services = [obj for obj in objects if obj['id'] in data['services']]

    return render(request, 'request.html', {
        'request_data': data,
        'services': services,
        'rovers': rovers,
        'request_id': request_id,
    })
