import random

from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Subject
from datacenter.models import Lesson
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

COMMENDATIONS = ["Хвалю!"]


def fix_marks(schoolkid):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        Mark.objects.filter(
            points__lt=4,
            schoolkid=student,
        ).update(points=5)
    except MultipleObjectsReturned:
        print("Имя недостаточно однозначно")
    except ObjectDoesNotExist:
        print("Студент не найден!")


def remove_chastisements(schoolkid):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        Chastisement.objects.filter(
            schoolkid=student,
        ).delete()
    except MultipleObjectsReturned:
        print("Имя недостаточно однозначно")
    except ObjectDoesNotExist:
        print("Студент не найден!")


def create_commendation(schoolkid_name, subject_name):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except MultipleObjectsReturned:
        print("Имя недостаточно однозначно")
        return
    except ObjectDoesNotExist:
        print("Студент не найден!")
        return
    try:
        subject = Subject.objects.get(
            title__contains=subject_name,
            year_of_study=student.year_of_study
        )
    except MultipleObjectsReturned:
        print("Предмет недостаточно однозначный")
        return
    except ObjectDoesNotExist:
        print("Предмет не найден!")
        return

    date_query = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_name,
    ).order_by('date').last()
    if not date_query:
        print("Урок не найден!")
        return
    date = date_query.date

    teacher_query = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_name
    ).last()
    if not teacher_query:
        print("Преподаватель не найден!")
        return
    teacher = date_query.teacher

    Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=date,
        schoolkid=student,
        subject=subject,
        teacher=teacher
    )
