from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.IndexApiView.as_view()),
    path('loans/', views.LoansApiView.as_view()),
    path("delete_loans/<int:loan_id>/", views.LoansApiView.as_view()),
    path("update_loans/<int:loan_id>/", views.LoansApiView.as_view()),
    # path("delete_loans/<int:loan_id>/", views.delete_loans, name="delete_loans"),
    # path("update_loans/<int:loan_id>/", views.update_loans, name="update_loans"),
    path("login/", views.UsersApiView.as_view()),
    # path("login/", views.login, name="login"),
    # path("loans/", views.loans, name="loans"),
    
    
    path("error/", views.error, name="error"),
    path("successful_loan/", views.successful_loan, name="successful_loan"),
    path("unsuccessful_loan/", views.unsuccessful_loan, name="unsuccessful_loan"),
    path("not_login/", views.not_login, name="not_login")
]