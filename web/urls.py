from django.urls import path
from . import views
from .views import UsersModelViewSet,LoansModelViewSet

urlpatterns = [
    path('', UsersModelViewSet.as_view({'get': 'list'}), name='users-list'),
    path('login/', UsersModelViewSet.as_view({'post': 'login'}), name='users-login'),
    path('loans/', LoansModelViewSet.as_view({'get': 'list', 'post':'create'}), name='loans-create-list'),
    path('delete_loans/<int:pk>/', LoansModelViewSet.as_view({'delete': 'destroy'}), name='loans-destroy'),
    path('update_loans/<int:pk>/', LoansModelViewSet.as_view({'get': 'list', 'put': 'update'}), name='loans-update'),
    path("error/", views.error, name="error"),
    path("successful_loan/", views.successful_loan, name="successful_loan"),
    path("unsuccessful_loan/", views.unsuccessful_loan, name="unsuccessful_loan"),
    path("not_login/", views.not_login, name="not_login")
]