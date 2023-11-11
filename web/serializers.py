from .models import Loans, Users
from rest_framework import serializers


class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['id','dni', 'name_and_last_name', 'genre', 'email', 'requested_amount']


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [ 'email', 'password', 'is_admin']