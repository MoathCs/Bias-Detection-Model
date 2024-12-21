from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('ViewSessions/', views.ViewSessions, name='ViewSessions'),

    path('register/', views.register, name='register'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('main-page/', views.dashboard, name='main-page'),

    path('model/', views.model, name='model'),

    path('ClickEvaluate/', views.ClickEvaluate, name='ClickEvaluate'),

    path('display_predictions/', views.display_predictions, name='display_predictions'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="custom_user/password_reset.html") ,name="reset_password"),

    # path('reset_password/', auth_views.PasswordResetView.as_view() ,name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="custom_user/password_reset_sent.html") ,name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="custom_user/password_reset_form.html") ,name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="custom_user/password_reset_done.html") ,name="password_reset_complete"),
]


