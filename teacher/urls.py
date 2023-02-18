from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('home/', views.TeacherListView.as_view(), name="home"),
    path('teachers/', views.TeacherListView.as_view(), name="teachers"),
    path('add_teacher/', views.TeacherCreateView.as_view(), name="add_teacher"),
    path('update_teacher/<int:pk>/', views.TeacherUpdateView.as_view(), name="update_teacher"),
    path('delete_teacher/<int:pk>/', views.TeacherDestroyView.as_view(), name="delete_teacher"),

    path('upload_teachers/', views.TeacherUploadView.as_view(), name="upload_teachers"),
    path('teacher_subjects/<int:pk>/', views.TeacherSubjectsListView.as_view(), name="teacher_subjects"),

    path('subjects/', views.SubjectsListView.as_view(), name="subjects"),
    path('create_subject/', views.CreateSubjectsView.as_view(), name="create_subject"),
    path('update_subject/<int:pk>', views.SubjectUpdateView.as_view(), name="update_subject"),
    path('delete_subject/<int:pk>', views.SubjectsDestoryView.as_view(), name="delete_subject"),

    path("signin/", views.SignIntView.as_view(), name="signin"),
    path("signout/", views.SignoutAPIView.as_view(), name="signout"),
] \
    + static("/static/", document_root=settings.STATIC_ROOT) \
    + static("/media/",document_root=settings.MEDIA_ROOT)

