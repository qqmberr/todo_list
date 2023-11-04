from django.utils import timezone

from django.db import models
from django.urls import reverse

# создаем функцию, которая будет полезна для выполнения сроков задачи по умолчанию
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class ToDoList(models.Model):
    # задаем ограничение для поля title и делаем его уникальным
    title = models.CharField(max_length=100, unique=True)

    # эта функция возвращает URL-адрес конкретного элемента данных
    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    # задаем ограничение для поля title - 100 символов
    title = models.CharField(max_length=100)
    # поле description может быть пустым
    description = models.TextField(null=True, blank=True)
    # значение даты по умолчанию - текущая дата при первом сохранении объекта
    created_date = models.DateTimeField(auto_now_add=True)
    # устанавливаем срок выполнения задачи по умолчанию одну нделю, обращаясь к функции one_week_hence
    due_date = models.DateTimeField(default=one_week_hence)
    # эта команда связывает ToDoItem со своим ToDoList, так что у каждого ToDoItem должен быть ровно один ToDoList, которому он принадлежит.
    # ключевое слово on_delete в той же строке гарантирует, что при удалении списка дел все связанные с ним элементы дел также будут удалены.
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    # эта функция возвращает URL-адрес конкретного элемента данных
    def get_absolute_url(self):
        return reverse(
            'item-update', args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f'{self.title}: due {self.due_date}'

    class Meta:
        ordering = ['due_date']