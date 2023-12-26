import random

from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Subject
from datacenter.models import Lesson

COMMENDATIONS = [
    "Хвалю!",
    "Молодец!",
    "Хорошая работа на уроке",
    "Отличная домашняя работа"
]


def get_student(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        print("Имя недостаточно однозначно")
    except Schoolkid.DoesNotExist:
        print("Студент не найден!")
    return None


def fix_marks(schoolkid):
    student = get_student(schoolkid)
    Mark.objects.filter(
        points__lt=4,
        schoolkid=student,
    ).update(points=5)


def remove_chastisements(schoolkid):
    student = get_student(schoolkid)
    Chastisement.objects.filter(
        schoolkid=student,
    ).delete()


def create_commendation(schoolkid_name, subject_name):
    student = get_student(schoolkid_name)
    if not student:
        return
    try:
        subject = Subject.objects.get(
            title__contains=subject_name,
            year_of_study=student.year_of_study
        )
    except Subject.MultipleObjectsReturned:
        print("Предмет недостаточно однозначный")
        return
    except Subject.DoesNotExist:
        print("Предмет не найден!")
        return

    lesson_query = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_name,
    ).order_by('date').last()

    if not lesson_query:
        print("Урок не найден!")
        return
    date = lesson_query.date
    teacher = lesson_query.teacher

    Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=date,
        schoolkid=student,
        subject=subject,
        teacher=teacher
    )
