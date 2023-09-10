from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from Product.models import *
from Product.serializers.product_serializers import *
from rest_framework.response import Response



class ProductViewSet(ViewSet):
    @action(methods=['post'], detail=False, url_path=r'productviews', url_name='productviews')
    def CategoryViews(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context= {'request': request})
        return Response(data=serializer.data)