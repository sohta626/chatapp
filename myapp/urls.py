from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.UserCreate.as_view(), name='signup_view'),
    path('login', views.UserLogin.as_view(), name='login_view'),
    path('friends', views.friends_next, name='friends'),
    path('talk_room/<int:your_id>/<int:the_other_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('name_change/<int:pk>/', views.NameChange.as_view(), name='name_change'),
    path('email_change/<int:pk>/', views.EmailChange.as_view(), name='email_change'),
    path('icon_change/<int:pk>/', views.IconChange.as_view(), name='icon_change'),
    path('pass_change', views.PassChange.as_view(), name='pass_change'),
    path('pass_change_success', views.pass_change_success, name='pass_change_success'),
    path('logout', views.logout, name="logout_view"),
    path('logout2', views.UserLogout.as_view(), name='logout_view2')
]
