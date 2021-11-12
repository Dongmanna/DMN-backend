# main/urls.py
from django.urls import path
from .views import CommentListView, DoneRegisterView, DoneView, PostJoinView


urlpatterns = [
    path('<int:id>/comments/', CommentListView.as_view()),
    path('<int:id>/join/', PostJoinView.as_view()),
    path('<int:id>/doneregister/', DoneRegisterView.as_view()),
    path('<int:id>/done/', DoneView.as_view()),
]