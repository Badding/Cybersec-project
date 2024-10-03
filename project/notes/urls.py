from django.urls import path
#from .views import registerView, notesView, loginView
from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('notes/', views.notesView, name='notes'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('deleteNote/<int:note_id>/', views.deleteNote, name='deleteNote'),
]