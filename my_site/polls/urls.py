from django.urls import path, re_path
from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index, name="index"),    # handle request for 127.0.0.1/polls/ with index function in views.py
    path('<int:question_id>/', views.detail, name="detail"),            # 127.0.0.1/polls/1 (last int is question_id)
    path('<int:question_id>/results/', views.results, name="results"),  # 127.0.0.1/polls/1/results
    # path('<int:question_id>/vote/', views.vote, name="vote"),           # 127.0.0.1/polls/1/vote
    # or using re_path with regular expression: r'^(?P<question_id>[0-9]+)/vote/$'
    re_path(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name="vote"),
]
