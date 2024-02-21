from django.urls import path
from .views import searchLawyer,lawyerData,lawyerDetail


urlpatterns = [
    path('import-lawyers/',lawyerData),
    path('search-lawyers',searchLawyer),
    path('lawyer-detail/<int:id>/', lawyerDetail),
]
