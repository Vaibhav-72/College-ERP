from django.db import models


# =========================
# STUDENT MODEL
# =========================
class Student(models.Model):

    COURSE_CHOICES = [
        ('BSc IT', 'BSc IT'),
        ('BMS', 'BMS'),
    ]

    roll_no = models.CharField(max_length=20, unique=True)
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)

    # ✅ Course Dropdown + Default BSc IT
    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        default='BSc IT'
    )

    dob = models.DateField()
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"


# =========================
# TEACHER MODEL
# =========================
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# =========================
# ATTENDANCE MODEL
# =========================
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'date', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.date}"


# =========================
# MARKS MODEL
# =========================
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    internal_marks = models.IntegerField(default=0)
    external_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)

    class Meta:
        unique_together = ('student', 'subject')

    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.external_marks
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"


# =========================
# ASSIGNMENT MODEL
# =========================
class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='assignments/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# NOTICE BOARD MODEL
# =========================
class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

