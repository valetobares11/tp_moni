from .models import Loans
from django.conf import settings
import requests
from .serializers import LoansSerializer

def loan_application_accepted(dni):
    url = settings.URL_MONI.format(dni)
    response = requests.get(url)
    
    return response.json().get('status')=='approve'

def get_fields_loans(loan):
    fields_model_loans = [field.name for field in Loans._meta.get_fields()]
    data = {}
    
    for field in fields_model_loans:
        data[field] = (getattr(loan, field, None))

    return data

def all_loans():
    loans = Loans.objects.all()
    serializer = LoansSerializer(loans, many=True)

    return serializer.data