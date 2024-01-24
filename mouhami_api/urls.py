from django.urls import path
from .views import LawyerViewSet,booking,lawyerapi,lawyerData

urlpatterns = [
    path('lawyers/', LawyerViewSet.as_view()),
    path('lawyers/<int:id>', lawyerapi),
    path('lawyers/<int:id>/bookings/',booking),
    path('import-lawyers/',lawyerData),

]
