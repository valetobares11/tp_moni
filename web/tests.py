from django.test import TestCase, Client
import json
from .models import Users,Loans


class LoansTestCase(TestCase):
    def setUp(self):
        Loans.objects.create(id=1,
                             dni="41018624", 
                             name_and_last_name="valentin tobares",
                             email="valetobares11@gmail.com",
                             genre="M",
                             requested_amount=800)

    
    def test_loan_update_dni(self):
        client = Client()
        loan = Loans.objects.filter(id="1").first()
        loan_data = loan.to_dict()
        old_dni = loan.dni
        email = loan.email
        new_dni = '11111111'
        loan_data['dni'] = new_dni
        response = client.post('/update_loans/1/', loan_data)
        self.assertEqual(response.status_code, 302)
        loan = Loans.objects.filter(id="1").first()
        self.assertFalse(loan.dni == old_dni)
        self.assertTrue(loan.email == email)

    def test_loan_update_email(self):
        client = Client()
        loan = Loans.objects.filter(id="1").first()
        email_old = loan.email
        dni = loan.dni
        loan_data = loan.to_dict()
        new_email = 'valetobares@gmail.com'
        loan_data['email'] =  new_email
        response = client.post('/update_loans/1/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/loans/")
        loan = Loans.objects.filter(id="1").first()
        self.assertFalse(loan.email == email_old)
        self.assertTrue(loan.dni == dni)

    def test_loan_update_error_incomplete_form(self):
        client = Client()
        loan = Loans.objects.filter(id="1").first()
        loan_data = {
            'id':1,
            'dni':'11111111'
        }
        response = client.post('/update_loans/1/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/error/")


    def test_loan_update_error_incomplete_form(self):
        client = Client()
        loan_data = {
            'id':1,
            'dni':'11111111',
            'name_and_last_name':'valentin tobares',
            'email':'valetobares11@gmail.com',
            'genre':'M',
            'requested_amount':'8000'
        }
        response = client.post('/update_loans/99/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/error/")

    def test_index_error_incomplete_form(self):
        client = Client()
        loan_data = {
            'dni':'11111111',
            'name_and_last_name':'valentin tobares'
        }
        response = client.post('/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/error/")

  

    def test_loan_delete(self):
        client = Client()
        response = client.get('/delete_loans/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/loans/")
        loan = Loans.objects.filter(id=1).first()
        self.assertEquals(loan, None)


    def test_loan_delete_not_found(self):
        client = Client()
        response = client.get('/delete_loans/99/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/error/")


class UsersTestCase(TestCase):
    def setUp(self):
        Users.objects.create(id=1,
                             email="valetobares11@gmail.com",
                             password="123",
                             is_admin=True)

    def test_login_user_error(self):
        client = Client()
        loan_data = {
            'email':'valetobares11@gmail.com'
        }
        response = client.post('/login/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/error/")
    
    def test_login_user_not_login(self):
        client = Client()
        loan_data = {
            'email':'valetobares11@gmail.com',
            'password':'123456789'
        }
        response = client.post('/login/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/not_login/")
    
    def test_login_user_login(self):
        client = Client()
        loan_data = {
            'email':'valetobares11@gmail.com',
            'password':'123'
        }
        response = client.post('/login/', loan_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url=="/loans/")