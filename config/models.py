from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'student':
        Student.objects.create(user=instance)

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Module(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ClassModule(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_obj} - {self.module}"

class Seance(models.Model):
    classmodule = models.ForeignKey(ClassModule, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.classmodule} - {self.date}"

class AbsencePresence(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Seance, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'session')

    def __str__(self):
        return f"{self.student} - {self.session} - {self.status}"
