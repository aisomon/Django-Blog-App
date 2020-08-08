from django.urls import path
from . import views

app_name="blog"

urlpatterns = [
    path('', views.home, name = 'index'),
    path('author/<name>',views.getauthor, name="author"),
    path('article/<int:id>', views.getsingle, name="single_post"),
    path('topic/<name>', views.getTopic, name="topic"),
    path('login/', views.getLogin, name="login"),
    path('logout/', views.getLogout, name="logout"),
    path('create/', views.getCreate, name="create"),
    path('profile/', views.getProfile, name="profile"),
    path('update/<int:pid>', views.getUpdate, name="update"),
    path('delete/<int:pid>', views.getDelete, name="delete"),
    path('register/', views.getRegister, name="register"),
    path('category/', views.getCategory, name="category"),
    path('create/category/', views.getCreateCategory, name="createCategory"),
]
