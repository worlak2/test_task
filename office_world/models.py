from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Person(models.Model):
    fio = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    image = models.ImageField(upload_to='image_directory', verbose_name='Фото')
    age = models.IntegerField(verbose_name='Возраст')
    biography = models.TextField(verbose_name='Биография')

    def __str__(self):
        return f'{self.fio} {self.name} {self.patronymic}'

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'


class VoteModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата конца')
    persons = models.ManyToManyField(Person, verbose_name='Участники', through='VoteUser')
    max_vote = models.IntegerField(default=-1, blank=True, verbose_name='Максимальное число голосов')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Голосования'
        verbose_name = 'Голосование'


class VoteUser(models.Model):
    user = models.ForeignKey(Person, on_delete=CASCADE)
    vote = models.ForeignKey(VoteModel, on_delete=CASCADE)
    vote_count = models.IntegerField(default=0, verbose_name='Голосов')

    class Meta:
        verbose_name_plural = 'Голоса'
        verbose_name = 'Голос'
        ordering = ['-vote_count']
