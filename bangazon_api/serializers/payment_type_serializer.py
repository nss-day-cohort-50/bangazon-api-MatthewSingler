from rest_framework import serializers
from bangazon_api.models import PaymentType
class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'

class CreatePaymentType(serializers.Serializer):
    acctNumber = serializers.CharField()
    merchant = serializers.CharField()
