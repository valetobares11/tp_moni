from django.test import TestCase, Client
import json
from .models import Users,Loans
from .serializers import LoansSerializer


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
        serializer = LoansSerializer(loan)
        old_dni = serializer.data['dni']
        data_loan = serializer.data;
        data_loan['dni'] = '11111111'
        print(data_loan)
        response = client.put('/update_loans/1/', data_loan)
        print(response)
        # self.assertEqual(response.status_code, 200)
        loan = Loans.objects.filter(id="1").first()
        print(loan)
        self.assertTrue(loan.dni != old_dni and loan.dni=='11111111')

    def test_loan_update_email(self):
        client = Client()
        loan = Loans.objects.filter(id="1").first()
        serializer = LoansSerializer(loan)
        email_old = serializer.data['email']
        data_loan = serializer.data
        data_loan['email'] = 'valetobares@gmail.com'
        response = client.put('/update_loans/1/', data_loan)
        # self.assertEqual(response.status_code, 200)
        loan = Loans.objects.filter(id="1").first()
        self.assertFalse(loan.email == email_old)

    # def test_loan_update_error_incomplete_form(self):
    #     client = Client()
    #     loan = Loans.objects.filter(id="1").first()
    #     loan_data = {
    #         'id':1,
    #         'dni':'11111111'
    #     }
    #     response = client.post('/update_loans/1/', loan_data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response.url=="/error/")


    # def test_loan_update_error_id_not_exist(self):
    #     client = Client()
    #     loan_data = {
    #         'id':1,
    #         'dni':'11111111',
    #         'name_and_last_name':'valentin tobares',
    #         'email':'valetobares11@gmail.com',
    #         'genre':'M',
    #         'requested_amount':'8000'
    #     }
    #     response = client.post('/update_loans/99/', loan_data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response.url=="/error/")

    # def test_index_error_incomplete_form(self):
    #     client = Client()
    #     loan_data = {
    #         'dni':'11111111',
    #         'name_and_last_name':'valentin tobares'
    #     }
    #     response = client.post('/update_loans/1/', loan_data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response.url=="/error/")

  

    # def test_loan_delete(self):
    #     client = Client()
    #     response = client.delete('/delete_loans/1/')
    #     self.assertEqual(response.status_code, 200)
    #     loan = Loans.objects.filter(id=1).first()
    #     self.assertEquals(loan, None)


    # def test_loan_delete_not_found(self):
    #     client = Client()
    #     response = client.delete('/delete_loans/99/')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response.url=="/error/")


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
        self.assertEqual(response.status_code, 200)