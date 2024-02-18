from django.urls import path

from .views import searchLawyer,lawyerData


urlpatterns = [
    path('import-lawyers/',lawyerData),
    path('search-lawyers',searchLawyer),
]
