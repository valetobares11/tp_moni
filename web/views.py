from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Users, Loans
from .forms import LoanForm,UserLoginForm

from .serializers import LoansSerializer, UsersSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.renderers import TemplateHTMLRenderer

from .utils import loan_application_accepted, get_fields_loans, all_loans

class IndexApiView(APIView):
    
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, format=None):
        form = LoanForm()        
        formlogin = UserLoginForm()
        return Response({'form': form, 'formlogin': formlogin}, template_name='web/form_loan.html')


class LoansApiView(APIView):
    """
    
    """
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, loan_id = None, format=None):
        if loan_id == None:
            data = all_loans()
            return Response({'loans': data}, template_name='web/loans_list.html')
        loan = Loans.objects.filter(id=loan_id).first()
        form = LoanForm(initial=get_fields_loans(loan))
        return render(request, 'web/form_loan_update.html', {'form': form, 'id_loan': loan.id})
    
    def post(self, request, loan_id=None, format=None):
        serializer = LoansSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if loan_id == None:
                if loan_application_accepted(data['dni']):
                    serializer.save()
                    return redirect('successful_loan')
                else:
                    return redirect('unsuccessful_loan')
            else:
                try:
                    loan = Loans.objects.filter(id=loan_id).first()
                    loan.dni = data['dni']
                    loan.name_and_last_name = data['name_and_last_name']
                    loan.genre = data['genre']
                    loan.email = data['email']
                    loan.requested_amount = data['requested_amount'] 
                    loan.save()
                    return Response({'loans': all_loans()}, template_name='web/loans_list.html')
                except:
                    return redirect('error')
        return redirect('error')
    
    
    def delete(self, request, loan_id, format=None):
        try:
            loan = Loans.objects.filter(id=loan_id).first()
            loan.delete()
            return Response({'loans': all_loans()}, template_name='web/loans_list.html')
        except:
            return redirect('error')

    # def put(self, request, loan_id ,format=None):
    #     print("esta entrando aca o no ???")
    #     serializer = LoansSerializer(data=request.data)
    #     if serializer.is_valid():
    #         data = serializer.validated_data
    #         loan = Loans.objects.filter(id=loan_id).first()
    #         loan.dni = data['dni']
    #         loan.name_and_last_name = data['name_and_last_name']
    #         loan.genre = data['genre']
    #         loan.email = data['email']
    #         loan.requested_amount = data['requested_amount'] 
    #         loan.save()
    #         return Response({'loans': all_loans()}, template_name='web/loans_list.html')
    #     return redirect('error')


# def update_loans(request, loan_id):
#     """

#     """
#     loan = Loans.objects.filter(id=loan_id).first()
#     if request.method == 'POST':
#         form = LoanForm(request.POST)
#         if form.is_valid() or loan is not None:
#             try:
#                 loan.dni = form.cleaned_data['dni']
#                 loan.name_and_last_name = form.cleaned_data['name_and_last_name']
#                 loan.genre = form.cleaned_data['genre']
#                 loan.email = form.cleaned_data['email']
#                 loan.requested_amount = form.cleaned_data['requested_amount'] 
#                 loan.save()
#                 return redirect('loans')
#             except Exception as e:
#                 print(f"Error while trying to save the loan {e}")
#                 return redirect('error')
#         else:
#             print(f"Error with form, invalid LoanForm")
#             return redirect('error')

    
     
class UsersApiView(APIView):
    """
    
    """
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email', None)
            password = serializer.data.get('password', None)
            user = Users.objects.filter(email=email , password=password).first()
            if user is not None and user.is_admin==True:
                return Response({'loans': all_loans()}, template_name='web/loans_list.html')
            else:
                return redirect('not_login')    
        return redirect('error')



def error(request):
    """
    This method returns a render to the error page.
    """
    return render(request,'web/pag_error.html')

def successful_loan(request):
    """
    This method returns render the 'Loan Accepted' page.
    """
    return render(request,'web/page_accepted_loans.html')

def unsuccessful_loan(request):
    """
    This method returns render the 'Loan not accepted' page.
    """
    return render(request,'web/page_not_accepted_loans.html')

def not_login(request):
    """
    This method returns the Login Failure page.
    """
    return render(request,'web/page_not_login.html')

