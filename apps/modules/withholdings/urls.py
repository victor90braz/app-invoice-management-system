from django.urls import path
from .views import withholding_list

urlpatterns = [
    path('', withholding_list, name='withholding_list'),
]
