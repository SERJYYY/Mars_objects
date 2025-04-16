from django.shortcuts import render, get_object_or_404, redirect
from .models import MarsObject, RequestItem, RequestStatus, MarsRequest, Rover
from django.views.decorators.http import require_POST
from django.db import transaction, connection
from django.contrib import messages
from django.http import HttpResponseNotAllowed


def home(request):
    query = request.GET.get("q", "")
    objects = MarsObject.objects.filter(is_deleted=False)
    if query:
        objects = objects.filter(name__icontains=query)

    # Получить заявку-черновик текущего пользователя
    draft_request = MarsRequest.objects.filter(
        creator=request.user,
        status=RequestStatus.DRAFT
    ).first()

    return render(request, "home.html", {
        "objects": objects,
        "query": query,
        "draft_request": draft_request,
    })




@require_POST
@transaction.atomic
def add_to_cart(request, object_id):
    mars_object = get_object_or_404(MarsObject, pk=object_id, is_deleted=False)

    # Получаем или создаём черновик заявки
    draft_request, _ = MarsRequest.objects.get_or_create(
        creator=request.user, 
        status=RequestStatus.DRAFT,
        defaults={"creator": request.user}
    )

    # Проверяем, добавлена ли услуга уже в заявку
    if draft_request.requestitem_set.filter(service=mars_object).exists():
        messages.error(request, "Эта услуга уже добавлена в заявку.")
    else:
        RequestItem.objects.create(
            request=draft_request,
            service=mars_object
        )
        messages.success(request, "Услуга успешно добавлена в заявку.")

    return redirect("home")


def service_detail(request, object_id):
    mars_object = get_object_or_404(MarsObject, id=object_id, is_deleted=False)
    return render(request, 'detail.html', {'obj': mars_object})


def cart_view(request):
    draft_request = MarsRequest.objects.filter(status=RequestStatus.DRAFT).first()
    items = RequestItem.objects.filter(request=draft_request) if draft_request else []
    rovers = Rover.objects.all()

    return render(request, "request.html", {
        "request_data": draft_request,
        "services": [item.service for item in items],
        "items": items,
        "request_id": draft_request.id if draft_request else "—",
        "rovers": rovers,
        "statuses": RequestStatus.choices,
    })



def delete_request(request, request_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed("Only POST method is allowed")
    
    # Получаем заявку
    draft_request = get_object_or_404(MarsRequest, id=request_id, creator=request.user)
    
    # Выполняем SQL-запрос на обновление статуса заявки с учетом правильного имени таблицы
    with connection.cursor() as cursor:
        cursor.execute(
            'UPDATE "Mars_marsrequest" SET status = %s WHERE id = %s', 
            ['deleted', draft_request.id]
        )
    
    messages.success(request, "Заявка успешно удалена.")
    return redirect('home')


@require_POST
@transaction.atomic
def save_request(request):
    # Получаем черновик заявки текущего пользователя
    draft_request = MarsRequest.objects.filter(creator=request.user, status=RequestStatus.DRAFT).first()

    if not draft_request:
        messages.error(request, "Нет черновика заявки.")
        return redirect("home")

    # Получаем данные из формы (марсоход и статус)
    rover_id = request.POST.get("rover")
    status = request.POST.get("status")

    # Проверяем, выбран ли марсоход
    if not rover_id or not status:
        messages.error(request, "Марсоход и статус должны быть выбраны.")
        return redirect("home")

    # Обновляем марсоход и статус заявки
    draft_request.rover_id = rover_id
    draft_request.status = status
    draft_request.save()

    # Проверяем, что в заявке есть хотя бы один элемент
    items = draft_request.requestitem_set.all()
    if not items:
        messages.error(request, "В заявке нет услуг.")
        return redirect("home")

    messages.success(request, "Заявка успешно сохранена.")
    return redirect("home")
    
def remove_from_cart(request, item_id):
    # Получаем объект из корзины (если он существует)
    item = get_object_or_404(RequestItem, id=item_id)

    # Удаляем элемент из корзины
    item.delete()

    # Перенаправляем обратно на страницу корзины
    return redirect('cart')