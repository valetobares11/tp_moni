from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .models import Users,Loans
from .forms import LoanForm,UserLoginForm
from django.conf import settings


def index(request):
    """
    This method, in case the request is a POST type, will check that the form is complete, that is to say that it is valid to insert the loan.
    that is to say that it is valid to insert the loan, in case that the form is not valid, it is going to 
    redirect to an error page. Before saving in the database, a request will be made to the URI_MONI 
    passing as parameter the person's ID, if the loan is approved, it will be saved in the database.
    In case the loan is not approved it will redirect to a page of NOT accepted the loan. 
    
    """
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            url = settings.URL_MONI.format(dni)
            response = requests.get(url)
            if response.status_code == 200:
                if (response.json().get('status')=='approve'):
                    try:
                        form.save()
                        return redirect('successful_loan')
                    except Exception as e:
                        print(f"Error while trying to save the loan {e}")
                        return redirect('error')
                else:
                    return redirect('unsuccessful_loan')
            else:
                print(f"Error in request. Status code: {response.status_code}")
                return redirect('error')
        else:
            print(f"Error form invalid LoanForm")
            return redirect('error')
    else:
        form = LoanForm()        
        formlogin = UserLoginForm()
    return render(request, 'web/form_loan.html', {'form': form, 'formlogin': formlogin})

def login(request):
    """
    This method will be used when the user tries to log in, in case the user is an admin user it will 
    If the user is admin it will login and redirect to the loans that are found. In case the user
    user is not admin or the credentials fail, it will redirect to a page of Could not log in because the user is not in the database.
    the user is not in the database.
    
    """
    form = UserLoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = Users.objects.filter(email=email , password=password).first()
        if user is not None and user.is_admin==True:
            return redirect('loans')
        else:
            print(f"This user is not in the BD")
            return redirect('not_login')    
    else:
        print(f"Error with form, invalid UserLoginForm")
        return redirect('error')

def loans(request):
    """
    This method will basically render the page with all the loans in the system.
    """
    loans = Loans.objects.all()
    return render(request, 'web/loans_list.html', {'loans': loans})

def update_loans(request, loan_id):
    """
    This method is used when the 'admin' user tries to modify a loan, or when rendering to the loan modification view.
    rendering to the loan modification view.
    In case the user is not in the system or the form is incomplete it will redirect to the /error/ page.
    :parameter 'loan_id': id of the loan.
    return: returns a redirect to an error page in case some invariant is not met or to /loans/ or to the form_loan_template. 
    to the form_loan_update template to modify the loan.
    """
    loan = Loans.objects.filter(id=loan_id).first()
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid() or loan is not None:
            try:
                loan.dni = form.cleaned_data['dni']
                loan.name_and_last_name = form.cleaned_data['name_and_last_name']
                loan.genre = form.cleaned_data['genre']
                loan.email = form.cleaned_data['email']
                loan.requested_amount = form.cleaned_data['requested_amount'] 
                loan.save()
                return redirect('loans')
            except Exception as e:
                print(f"Error while trying to save the loan {e}")
                return redirect('error')
        else:
            print(f"Error with form, invalid LoanForm")
            return redirect('error')
    else:
        fields_model_loans = [field.name for field in Loans._meta.get_fields()]
        data = {}
        for field in fields_model_loans:
            data[field] = (getattr(loan, field, None))
        form = LoanForm(initial=data)
        return render(request, 'web/form_loan_update.html', {'form': form, 'id_loan': loan.id})
    

def delete_loans(request, loan_id):
    """
    This method deletes a loan
    :parameter 'loan_id': id of the loan
    return: returns a redirect to /error/ in case of error or /loan/ on success
    """
    try:
        loan = Loans.objects.filter(id=loan_id).first()
        loan.delete()
        return redirect('loans')
    except Exception as e:
        print(f"Error when trying to delete a loan {e}")
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

