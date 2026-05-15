from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('create-task/', views.create_task, name='create_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('results/', views.results, name='results'),
    path('profile/', views.profile_view, name='profile'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('tasks/', views.all_tasks_view, name='all_tasks'),
    # Parolni tiklash yo'llari
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('videos/', views.video_list_view, name='video_list'),
    path('video/<int:pk>/', views.video_detail_view, name='video_detail'),
    path('quizzes/', views.quiz_list_view, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail_view, name='quiz_detail'),
]