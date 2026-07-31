from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from io import BytesIO
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from datetime import date
from django.http import HttpResponse
from .models import Student, Teacher, Attendance, Marks, Assignment, Notice

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from io import BytesIO
#marksheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from .models import Teacher

# =========================
# LOGIN VIEW
# =========================
def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # ADMIN LOGIN
        if role == 'Admin':
            user = authenticate(username=user_id, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/admin/')

        # TEACHER LOGIN
        if role == 'Teacher':
            teacher = Teacher.objects.filter(
                teacher_id=user_id,
                password=password
            ).first()
            if teacher:
                request.session['teacher_id'] = teacher.id
                return redirect('/teacher/dashboard/')

        # STUDENT LOGIN
        if role == 'Student':
            student = Student.objects.filter(
                student_id=user_id,
                password=password
            ).first()
            if student:
                request.session['student_id'] = student.id
                return redirect('/student/dashboard/')

    return render(request, 'auth/login.html')


# =========================
# TEACHER DASHBOARD
# =========================
def teacher_dashboard(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)
    return render(request, 'teacher/dashboard.html', {'teacher': teacher})


#teacher profile  

def teacher_profile(request):
    return render(request, "teacher/profile.html")


# =========================
# MARK ATTENDANCE (COURSE + DATE WISE)
# =========================
from datetime import date

from datetime import date

def mark_attendance(request):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)

    # Saare students
    students = Student.objects.all()

    # Default = today
    attendance_date = date.today()

    if request.method == 'POST':

        # Calendar se selected date
        selected_date = request.POST.get('attendance_date')

        if selected_date:
            attendance_date = selected_date

        for student in students:

            value = request.POST.get(
                f'attendance_{student.id}'
            )

            # Present = True
            # Absent = False
            status = value == 'present'

            Attendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                subject=teacher.subject,

                defaults={
                    'teacher': teacher,
                    'status': status
                }
            )

        return redirect('/teacher/attendance/history/')

    return render(
        request,
        'teacher/attendance.html',
        {
            'teacher': teacher,
            'students': students,
            'attendance_date': attendance_date
        }
    )

# =========================
# ATTENDANCE HISTORY
# =========================
def attendance_history(request):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)

    # Teacher ki attendance
    attendance = Attendance.objects.filter(
        teacher=teacher
    ).order_by('-date', 'student__roll_no')

    # Date filter
    selected_date = request.GET.get('date')

    if selected_date:
        attendance = attendance.filter(date=selected_date)

    # Counting
    total_records = attendance.count()
    present_count = attendance.filter(status=True).count()
    absent_count = attendance.filter(status=False).count()

    return render(request, 'teacher/attendance_history.html', {
        'attendance': attendance,
        'teacher': teacher,
        'selected_date': selected_date,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
    })

# =========================
# ADD MARKS
# =========================
def add_marks(request):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)

    # All students
    students = Student.objects.all().order_by('roll_no')

    if request.method == "POST":

        for student in students:

            internal = request.POST.get(
                f"internal_{student.id}"
            )

            external = request.POST.get(
                f"external_{student.id}"
            )

            # Dono marks filled hain tabhi save/update
            if internal != "" and external != "":

                internal = int(internal)
                external = int(external)

                Marks.objects.update_or_create(

                    student=student,
                    subject=teacher.subject,

                    defaults={
                        "teacher": teacher,
                        "internal_marks": internal,
                        "external_marks": external,
                    }
                )

        return redirect('/teacher/marks/history/')

    # Existing marks nikalna
    existing_marks = Marks.objects.filter(
        teacher=teacher,
        subject=teacher.subject
    )

    marks_dict = {
        mark.student_id: mark
        for mark in existing_marks
    }

    # Student object me existing marks attach
    for student in students:

        mark = marks_dict.get(student.id)

        if mark:
            student.saved_internal = mark.internal_marks
            student.saved_external = mark.external_marks
        else:
            student.saved_internal = ""
            student.saved_external = ""

    return render(request, 'teacher/add_marks.html', {
        'students': students,
        'teacher': teacher
    })

# =========================
# MARKS HISTORY
# =========================
def marks_history(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)
    marks = Marks.objects.filter(teacher=teacher)

    return render(request, 'teacher/marks_history.html', {
        'marks': marks,
        'teacher': teacher
    })


def delete_marks(request, id):
    Marks.objects.filter(id=id).delete()
    return redirect('/teacher/marks/history/')


# =========================
# VIEW STUDENTS
# =========================
def view_students(request):
    
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)

    students = Student.objects.all()

    return render(request, 'teacher/students.html', {
        'teacher': teacher,
        'students': students
    })


# =========================
# STUDENT DASHBOARD
# =========================
from django.db.models import Count
from core.models import Attendance, Assignment, Notice


def student_dashboard(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('/')

    student = Student.objects.get(id=student_id)

    total_classes = Attendance.objects.filter(student=student).count()

    present_classes = Attendance.objects.filter(
        student=student,
        status=True
    ).count()

    attendance_percentage = 0

    if total_classes > 0:
        attendance_percentage = round(
            (present_classes / total_classes) * 100
        )

    total_subjects = Attendance.objects.filter(
        student=student
    ).values(
        'subject'
    ).distinct().count()

    assignment_count = Assignment.objects.count()

    notice_count = Notice.objects.count()

    latest_assignments = Assignment.objects.order_by(
        '-upload_date'
    )[:5]

    latest_notices = Notice.objects.order_by(
        '-created_at'
    )[:5]

    context = {

        "student": student,

        "attendance_percentage": attendance_percentage,

        "total_subjects": total_subjects,

        "assignment_count": assignment_count,

        "notice_count": notice_count,

        "latest_assignments": latest_assignments,

        "latest_notices": latest_notices,

    }

    return render(
        request,
        "student/dashboard.html",
        context
    )
# =========================
# STUDENT ATTENDANCE
# =========================
def student_attendance(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('/')

    student = Student.objects.get(id=student_id)
    attendance = Attendance.objects.filter(student=student)

    total = attendance.count()
    present = attendance.filter(status=True).count()
    percent = int((present / total) * 100) if total else 0

    return render(request, 'student/attendance.html', {
        'student': student,
        'attendance': attendance,
        'percent': percent
    })

#=========================
# STUDENT MARKS
# =========================
def student_marks(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('/')

    student = Student.objects.get(id=student_id)
    marks = Marks.objects.filter(student=student)

    total_marks = sum(m.total_marks for m in marks)
    max_marks = len(marks) * 50
    percentage = round((total_marks / max_marks) * 100, 2) if max_marks else 0

    return render(request, 'student/marks.html', {
        'student': student,
        'marks': marks,
        'total_marks': total_marks,
        'percentage': percentage,
    })

# =========================
# STUDENT MARKSHEET
# =========================
def student_marksheet(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('/')

    student = Student.objects.get(id=student_id)
    marks = Marks.objects.filter(student=student)

    total_marks = sum(m.total_marks for m in marks)
    max_marks = len(marks) * 50
    percentage = round((total_marks / max_marks) * 100, 2) if max_marks else 0
    result = "PASS" if percentage >= 40 else "FAIL"

    return render(request, 'student/mu_marksheet.html', {
        'student': student,
        'marks': marks,
        'total_marks': total_marks,
        'percentage': percentage,
        'result': result
    })

# =========================
# DOWNLOAD MARKSHEET
# =========================    
def download_marksheet(request):
    
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("/")

    student = Student.objects.get(id=student_id)
    marks = Marks.objects.filter(student=student)

    total_marks = sum(m.total_marks for m in marks)
    max_marks = len(marks) * 50

    percentage = round(
        (total_marks / max_marks) * 100,
        2
    ) if max_marks else 0

    result = "PASS" if percentage >= 40 else "FAIL"

    buffer = BytesIO()

    doc = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,

    )

    elements=[]

    title = ParagraphStyle(

        "Title",

        fontSize=21,

        alignment=TA_CENTER,

        textColor=colors.darkblue,

        spaceAfter=5,

    )

    sub = ParagraphStyle(

        "Sub",

        fontSize=10,

        alignment=TA_CENTER,

        spaceAfter=2,

    )

    elements.append(
        Paragraph(
            "<b>मुंबई विश्वविद्यालय</b>",
            title
        )
    )

    elements.append(
        Paragraph(
            "<b>University of Mumbai</b>",
            title
        )
    )

    elements.append(
        Paragraph(
            "Re-accredited with A++ Grade (CGPA 3.65)",
            sub
        )
    )

    elements.append(
        Paragraph(
            "<b>GRADE CARD</b>",
            title
        )
    )

    elements.append(
        Paragraph(
            "Bachelor of Science (Information Technology)",
            sub
        )
    )

    elements.append(
        Paragraph(
            "Semester Examination",
            sub
        )
    )

    elements.append(
        Spacer(1,0.5*cm)
    )
    # ==========================
# STUDENT DETAILS
# ==========================

    info_data = [

    ["Name", student.name,
     "Mother's Name", getattr(student, "mother_name", "-")],

    ["ERN", student.roll_no,
     "Seat Number", student.roll_no],

    ["College",
     "Reena Mehta College of Arts Science Commerce & Management Studies",
     "Batch", "2026"],

    ["ABC ID",
     getattr(student, "abc_id", "-"),
     "Course",
     "B.Sc Information Technology"],

]

    info_table = Table(
    info_data,
    colWidths=[2.8*cm, 7.2*cm, 3*cm, 5*cm]
)

    info_table.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),0.7,colors.black),

    ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF2F8")),
    ("BACKGROUND",(2,0),(2,-1),colors.HexColor("#EAF2F8")),

    ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

    ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
    ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),

    ("FONTSIZE",(0,0),(-1,-1),9),

    ("BOTTOMPADDING",(0,0),(-1,-1),7),

    ("TOPPADDING",(0,0),(-1,-1),7),

]))

    elements.append(info_table)

    elements.append(
    Spacer(1,0.5*cm)
)

# ==========================
# MARKS TABLE
# ==========================

    table_data = [[
    "Subject",
    "Internal",
    "External",
    "Total",
    "Grade",
    "Remark"
]]

    for m in marks:

        if m.total_marks >= 90:
            grade = "O"

        elif m.total_marks >= 80:
            grade = "A+"

        elif m.total_marks >= 70:
            grade = "A"

        elif m.total_marks >= 60:
            grade = "B+"

        elif m.total_marks >= 55:
            grade = "B"

        elif m.total_marks >= 50:
            grade = "C"

        elif m.total_marks >= 40:
            grade = "D"

        else:
            grade = "F"

    remark = "PASS" if m.total_marks >= 20 else "FAIL"

    table_data.append([
        str(m.subject),
        str(m.internal_marks),
        str(m.external_marks),
        str(m.total_marks),
        grade,
        remark
    ])

    marks_table = Table(
table_data,
    colWidths=[
        8*cm,
        2.2*cm,
        2.2*cm,
        2*cm,
        2*cm,
        2.5*cm
    ]
)

    marks_table.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),0.7,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#003366")),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),

    ("ALIGN",(1,1),(-1,-1),"CENTER"),

    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

    ("FONTSIZE",(0,0),(-1,-1),9),

    ("BOTTOMPADDING",(0,0),(-1,0),8),

]))

    elements.append(marks_table)

    elements.append(Spacer(1,0.5*cm))

    # ==========================
# RESULT SUMMARY
# ==========================

    summary_data = [

    ["Grand Total", f"{total_marks} / {max_marks}"],

    ["Percentage", f"{percentage}%"],

    ["Result", result],

]

    summary_table = Table(
    summary_data,
    colWidths=[5*cm, 5*cm]
)

    summary_table.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),0.7,colors.black),

    ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF2F8")),

    ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

    ("FONTSIZE",(0,0),(-1,-1),10),

    ("BOTTOMPADDING",(0,0),(-1,-1),8),

    ("TOPPADDING",(0,0),(-1,-1),8),

]))

    elements.append(summary_table)

    elements.append(Spacer(1,1*cm))

    elements.append(
    Paragraph(
        "<para align='right'><b>Controller of Examination</b></para>",
        getSampleStyleSheet()["Normal"]
    )
)

# ==========================
# BUILD PDF
# ==========================

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
    f'attachment; filename="MU_GradeCard_{student.roll_no}.pdf"'
)

    response.write(pdf)

    return response

# STUDENT PROFILE

def student_profile(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("/")

    student = Student.objects.get(id=student_id)

    return render(
        request,
        "student/profile.html",
        {
            "student": student
        }
    )

# =========================
# STUDENT SUBJECTS
# =========================


def student_subjects(request):
    teachers = Teacher.objects.all()

    return render(request, 'student/subjects.html', {
        'subjects': teachers
    })
    

# =========================
# TEACHER ASSIGNMENT UPLOAD
# =========================
def teacher_upload_assignment(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('/')

    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if title and file:
            Assignment.objects.create(
                teacher=teacher,
                title=title,
                subject=teacher.subject,
                pdf=file
            )

        return redirect('/teacher/assignments/')

    assignments = Assignment.objects.filter(teacher=teacher).order_by('-upload_date')

    return render(request, 'teacher/upload_assignment.html', {
        'assignments': assignments,
        'teacher': teacher
    })


# =========================
# STUDENT ASSIGNMENTS
# =========================
def student_assignments(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('/')

    student = Student.objects.get(id=student_id)
    assignments = Assignment.objects.all().order_by('-upload_date')

    return render(request, 'student/assignments.html', {
        'student': student,
        'assignments': assignments
    })


# =========================
# DELETE ASSIGNMENT
# =========================
def delete_assignment(request, id):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('/')

    assignment = Assignment.objects.get(id=id)

    if assignment.teacher.id == teacher_id:
        assignment.delete()

    return redirect('/teacher/assignments/')


# =========================
# NOTICE BOARD
# =========================
def notice_board(request):
    notices = Notice.objects.all().order_by('-created_at')

    return render(request, 'notice_board.html', {
        'notices': notices
    })
    
    # =========================
# LOGOUT
# =========================
def logout_view(request):
    request.session.flush()
    return redirect('/')  

 # =========================
# IDCARD
# =========================

from django.shortcuts import render, get_object_or_404
from .models import Student

def student_id_card(request, id, type):
    student = get_object_or_404(Student, id=id)

    if type == "horizontal":
        template = "id_card_horizontal.html"
    else:
        template = "id_card_vertical.html"

    return render(request, template, {
        "student": student
    })


#NOTICE  

from .models import Notice

def notice_board(request):
    notices = Notice.objects.order_by("-created_at")

    return render(
        request,
        "student/notice_board.html",
        {
            "notices": notices
        }
    )


def notice_detail(request, id):
    notice = Notice.objects.get(id=id)

    return render(
        request,
        "student/notice_detail.html",
        {
            "notice": notice
        }
    )
    
    
    # ==========================
# TEACHER SUBJECTS
# ==========================
def teacher_subjects(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("/")

    teacher = Teacher.objects.get(id=teacher_id)

    return render(request, "teacher/subjects.html", {
        "teacher": teacher
    })


# ==========================
# TEACHER NOTICE BOARD
# ==========================
def teacher_notice_board(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("/")

    teacher = Teacher.objects.get(id=teacher_id)
    notices = Notice.objects.order_by("-created_at")

    return render(request, "teacher/notice_board.html", {
        "teacher": teacher,
        "notices": notices
    })


# ==========================
# TEACHER NOTICE DETAIL
# ==========================
def teacher_notice_detail(request, id):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("/")

    teacher = Teacher.objects.get(id=teacher_id)
    notice = Notice.objects.get(id=id)

    return render(request, "teacher/notice_detail.html", {
        "teacher": teacher,
        "notice": notice
    })


# ==========================
# TEACHER SETTINGS
# ==========================
def teacher_settings(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("/")

    teacher = Teacher.objects.get(id=teacher_id)

    return render(request, "teacher/settings.html", {
        "teacher": teacher
    })


# ==========================
# TEACHER LOGOUT
# ==========================
def teacher_logout(request):
    request.session.flush()
    return redirect("/")