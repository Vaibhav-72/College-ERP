from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
urlpatterns = [

    # ================= ID CARD (IMPORTANT: ADMIN SE UPAR) =================
    path('admin/student/id-card/<int:id>/<str:type>/',
         views.student_id_card,
         name='student_id_card'),

    # ================= AUTH =================
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),

    # ================= TEACHER =================]



    # ==========================
    # Teacher Dashboard
    # ==========================

    path("teacher/dashboard/",views.teacher_dashboard,name="teacher_dashboard"),
    path("teacher/profile/",views.teacher_profile,name="teacher_profile"),
    path("teacher/students/",views.view_students,name="view_students"),
    path("teacher/attendance/", views.mark_attendance, name="teacher_attendance"),

    path("teacher/attendance/history/",views.attendance_history,name="attendance_history"),
    path("teacher/marks/", views.add_marks, name="teacher_marks"),
    path("teacher/assignments/", views.teacher_upload_assignment, name="teacher_assignments"),
    path("teacher/notice-board/",views.teacher_notice_board,name="teacher_notice_board"),
    path("teacher/notice-board/<int:id>/",views.teacher_notice_detail,name="teacher_notice_detail"),
    path("teacher/settings/",views.teacher_settings,name="teacher_settings"),

    path("teacher/logout/",views.teacher_logout,name="teacher_logout"),
    path("teacher/study-materials/",views.teacher_study_materials,name="teacher_study_materials"
),

    # ================= STUDENT =================
    path('student/dashboard/', views.student_dashboard),
    path('student/attendance/', views.student_attendance),
    path('student/subjects/', views.student_subjects, name='student_subjects'),
    path('student/marks/', views.student_marks, name='student_marks'),
    path('student/assignments/', views.student_assignments),
    path('student/mu-marksheet/', views.student_marksheet, name='mu_marksheet'),
    path('student/download-marksheet/', views.download_marksheet, name='download_marksheet'),
    path("student/profile/",views.student_profile,name="student_profile"),
    path("notice-board/", views.notice_board, name="notice_board"),
    path("notice-board/<int:id>/", views.notice_detail, name="notice_detail"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
