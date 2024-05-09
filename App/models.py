from django.db import models


GENDER = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]

Klass = [
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("6","6"),
    ("7","7"),
    ("8","8"),
    ("9","9"),
    ("10","10"),
    ("11","11"),
    ("12","12"),
]

# Create your models here.
class Activities(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class TimeSlots(models.Model):
    for_girls = models.BooleanField(default=False)
    start = models.TimeField()
    end  = models.TimeField()
    def __str__(self):
        return self.start.strftime("%I:%M %p") + " - " + self.end.strftime("%I:%M %p")

class Student(models.Model):
    student_id = models.CharField(max_length=100)
    school_name = models.CharField(max_length=200, null=True, blank=True)
    other_school_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/student/")
    student_name = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=20,choices=GENDER)
    Class = models.CharField(max_length=10, choices=Klass)
    guradian_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)

    def __str__(self):
        return self.student_name


class Participations(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE)
    time = models.ForeignKey(TimeSlots, on_delete=models.CASCADE)
    def __str__(self):
        return self.student.student_name

class IdMonitor(models.Model):
    current  = models.IntegerField(default=100)
    def __str__(self):
        return str(self.current)