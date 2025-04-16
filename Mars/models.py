from django.db import models
from django.contrib.auth.models import User

# Статусы заявок
class RequestStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    DELETED = 'deleted', 'Удалён'
    SUBMITTED = 'submitted', 'Сформирован'
    COMPLETED = 'completed', 'Завершён'
    REJECTED = 'rejected', 'Отклонён'


# Модель марсохода
class Rover(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название марсохода")

    def __str__(self):
        return self.name


# Объекты на Марсе
class MarsObject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# Заявка
class MarsRequest(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_requests',
        verbose_name="Создатель"
    )
    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.DRAFT,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата формирования"
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата завершения"
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='moderated_requests',
        verbose_name="Модератор"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )
    rover = models.ForeignKey(
        'Rover',  
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Марсоход"
    )

    class Meta:
        db_table = 'Mars_marsrequest'  # Указываем имя таблицы в базе данных


    def __str__(self):
        return f"Заявка #{self.id} от {self.creator.username}"


# Связующая таблица: заявка — объект
class RequestItem(models.Model):
    request = models.ForeignKey(MarsRequest, on_delete=models.PROTECT, verbose_name="Заявка")
    service = models.ForeignKey(MarsObject, on_delete=models.PROTECT, verbose_name="Объект")

    class Meta:
        unique_together = ('request', 'service')  # Ограничение уникальности: одна услуга для каждой заявки

    def __str__(self):
        return f"{self.service.name}"
