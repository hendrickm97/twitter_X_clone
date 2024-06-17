from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name="register"),
    path('tweet_like/<int:pk>', views.tweet_like, name="tweet_like"),
    path('delete_tweet/<int:pk>', views.delete_tweet, name="delete_tweet"),
    path('update_tweet/<int:pk>', views.update_tweet, name="update_tweet")
]
