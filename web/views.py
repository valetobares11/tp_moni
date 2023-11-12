from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Users, Loans
from .forms import LoanForm,UserLoginForm

from .serializers import LoansSerializer, UsersSerializer
# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status 
from rest_framework.renderers import TemplateHTMLRenderer
from .utils import loan_application_accepted, get_fields_loans, all_loans
from rest_framework import viewsets


class LoansModelViewSet(viewsets.ModelViewSet):
    """
    List all loans, delete or create a new one
    """
    queryset = Loans.objects.all()
    serializer_class = LoansSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, pk=None, *args, **kwargs):
        if pk is None:
            queryset = all_loans()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'loans': serializer.data}, template_name='web/loans_list.html')
        loan = self.get_object()
        form = LoanForm(initial=get_fields_loans(loan))
        return render(request, 'web/form_loan_update.html', {'form': form, 'id_loan': loan.id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if loan_application_accepted(data['dni']):
                serializer.save()
                return redirect('successful_loan')
            else:
                return redirect('unsuccessful_loan')
        return redirect('error')

    def update(self, request, *args, **kwargs):
        loan = self.get_object()
        serializer = self.get_serializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'loans': all_loans()}, template_name='web/loans_list.html')
        return redirect('error')

    def destroy(self, request, *args, **kwargs):
        loan = self.get_object()
        loan.delete()
        return Response({'loans': all_loans()}, template_name='web/loans_list.html')
    



class UsersModelViewSet(ModelViewSet):
    """
    Create a new user
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def login(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email', None)
            password = serializer.data.get('password', None)
            user = Users.objects.filter(email=email, password=password).first()
            if user is not None and user.is_admin:
                return Response({'loans': all_loans()}, template_name='web/loans_list.html')
            else:
                return redirect('not_login')
        return redirect('error')
    
    def list(self, request, *args, **kwargs):
        form = LoanForm()
        formlogin = UserLoginForm()
        return Response({'form': form, 'formlogin': formlogin}, template_name='web/form_loan.html')


def error(request):
    """
    Returns a render to the error page.
    """
    return render(request,'web/pag_error.html')

def successful_loan(request):
    """
    Returns render the 'Loan Accepted' page.
    """
    return render(request,'web/page_accepted_loans.html')

def unsuccessful_loan(request):
    """
    Returns render the 'Loan not accepted' page.
    """
    return render(request,'web/page_not_accepted_loans.html')

def not_login(request):
    """
    Returns the Login Failure page.
    """
    return render(request,'web/page_not_login.html')

