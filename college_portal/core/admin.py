from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Student, Teacher, Attendance, Marks, Assignment, Notice
from .models import Teacher

# =========================
# STUDENT FORM (DOB Year Dropdown)
# =========================
class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            # Year dropdown 1980 se 2030 tak
            "dob": SelectDateWidget(years=range(1980, 2031))
        }


# =========================
# STUDENT ADMIN
# =========================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm

    list_display = (
        'id',
        'name',
        'course',
        'email',
        'mobile',
        'id_card_buttons'
    )

    list_filter = ('course',)
    search_fields = ('name', 'roll_no', 'student_id')

    def id_card_buttons(self, obj):
        vertical_url = reverse('student_id_card', args=[obj.id, 'vertical'])
        horizontal_url = reverse('student_id_card', args=[obj.id, 'horizontal'])

        return format_html(
            '<a style="padding:4px 8px;background:#1f4e9d;color:white;border-radius:4px;text-decoration:none;" target="_blank" href="{}">Vertical</a>&nbsp;'
            '<a style="padding:4px 8px;background:#28a745;color:white;border-radius:4px;text-decoration:none;" target="_blank" href="{}">Horizontal</a>',
            vertical_url,
            horizontal_url
        )

    id_card_buttons.short_description = "ID Card"


# =========================
# TEACHER ADMIN
# =========================


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "teacher_id",
        "name",
        "subject",
        "email",
        "mobile",
    )

    search_fields = (
        "teacher_id",
        "name",
        "subject",
        "email",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "teacher_id",
                "name",
                "photo",
                "email",
                "mobile",
                "subject",
                "password",
            )
        }),

        ("Additional Information", {
            "fields": (
                "qualification",
                "experience",
                "gender",
                "dob",
                "joining_date",
                "address",
            )
        }),
    )

# =========================
# ATTENDANCE FORM (Date Dropdown Fix)
# =========================
class AttendanceAdminForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
        widgets = {
            "date": SelectDateWidget(years=range(2020, 2031))
        }


# =========================
# ATTENDANCE ADMIN
# =========================
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm
    list_display = ('student', 'teacher', 'date', 'status')
    list_filter = ('date', 'teacher')
    search_fields = ('student__name',)


# =========================
# MARKS ADMIN
# =========================
@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject',
        'internal_marks',
        'external_marks',
        'total_marks'
    )
    search_fields = ('student__name', 'subject')


# =========================
# ASSIGNMENT ADMIN
# =========================
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'upload_date')
    list_filter = ('subject', 'teacher')
    search_fields = ('title',)


# =========================
# NOTICE ADMIN
# =========================
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


