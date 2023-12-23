from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Subject
from datacenter.models import Lesson


def fix_marks(schoolkid):
    Mark.objects.filter(
        points__lt=4,
        schoolkid__full_name__contains=schoolkid
    ).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(
        schoolkid__full_name__contains=schoolkid
    ).delete()


def create_commendation(schoolkid_name, subject_name):
    student = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    subject = Subject.objects.get(
        title__contains=subject_name,
        year_of_study=student.year_of_study
    )
    date = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_name
    ).last().date
    teacher = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_name
    ).last().teacher

    Commendation.objects.create(
        text="Хвалю!",
        created=date,
        schoolkid=student,
        subject=subject,
        teacher=teacher
    )
