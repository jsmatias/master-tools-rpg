from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from mastertools import views


urlpatterns = [
    path('player/', views.PlayersList.as_view()),
    path('player/<str:pk>', views.PlayersDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)