from rest_framework import serializers
from Payment.models import Gateway, Payment

class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('id', 'title', 'description', 'avatar')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'gateway', 'price', 'status', 'phone_number', 'token', 'device_uuid')