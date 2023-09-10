from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from Payment.models import *



class PaymentViewSet(ViewSet):
    @action(methods=['post'], detail=False, url_path=r'paymentviews', url_name='paymentviews')
    def PaymentViews(self, request):
        pass