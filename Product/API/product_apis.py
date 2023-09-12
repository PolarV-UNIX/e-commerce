from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
#CSRF
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from common.utils.common import(
    response,
    getClientIP,
    convertParam
)
from User.models import *
from Product.models import *
from Product.serializers.product_serializers import (
    ProductViewSerializer,
    DetailSerializer,
    FavoritsSerailizer,
    ProductForUserSerializer
)
from User.jwt import checkToken, genrateJWTToken
from User.models import User



class ProductViewSet(ViewSet):
    """ PRODUCT VIEW """
    @action(methods=['get'], detail=False, url_path=r'productview', url_name='productview')
    def productView(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        products = Product.objects.all().order_by('-created_at')[:60]
        serializer = ProductViewSerializer(products, many=True)
        if not serializer:
            return response(
                data=serializer.errors,
                status=400,
                message="the error about serialize the data"
            )
        return response(
            data=serializer.data,
            status=200,
            message="product list successfully returned"
        )
    
    """ PRODUCT DETAILS """
    @action(methods=['get'], detail=False, url_path=r'productdetail', url_name='productdetail')
    def productDetailView(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = convertParam(request)
        pk = data['id']
        product = Product.objects.filter(id=pk).first()
        if not product:
            return response(
                data=None,
                status=404,
                message="product not found"
            )
        serializer = DetailSerializer(product)
        return response(
            data=serializer.data,
            status=200,
            message="product found successfully"
        )
        
    """ ADD FAVORITS """
    @action(methods=['post'], detail=False, url_path=r'addfavorits', url_name='addfavorits')
    def addFavorits(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        data = convertParam(request)
        if not {'favorits'}.issubset(data):
            return response(
                data=None,
                status=400,
                message="favorits not sent!"
            )
        
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        serializer = FavoritsSerailizer(user, data)
        if not serializer:
            return response(
                data=serializer.errors,
                status=400,
                message="invalid fields sent"
            )
        return response(
                data=serializer.data,
                status=200,
                message="add to favorits"
            )
    
    """ REMOVE FAVORITS """
    @action(methods=['delete'], detail=False, url_path=r'removefavorits', url_name='removefavorits')
    def removeFavorits(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        data = convertParam(request)
        if not {'favorits'}.issubset(data):
            return response(
                data=None,
                status=400,
                message="favorits not sent!"
            )
        
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        serializer = FavoritsSerailizer(user, data)
        if not serializer:
            return response(
                data=serializer.errors,
                status=400,
                message="invalid fields sent"
            )
        return response(
                data=serializer.data,
                status=200,
                message="remove from favorits"
            )
    
    """ PROUCT FOR USER """
    @action(methods=['get'], detail=False, url_path=r'productforuser', url_name='productforuser')
    def productForUser(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        if user.favorits is None:
            products = Product.objects.all().order_by('-created_at')[:20]
            if not products:
                return response(
                data=None,
                status=404,
                message="products not found"
            )
            serializer = ProductForUserSerializer(products, many=True)
            if not serializer:
                return response(
                data=serializer.errors,
                status=400,
                message="invalid fields sent"
            )
            return response(
                data=serializer.data,
                status=200,
                message="successfully"
            )

        products = Product.objects.filter(title__icontains=user.favorits.title)
        if not products:
            return response(
                data=None,
                status=404,
                message="products by favorits not found"
            )
        serializer = ProductForUserSerializer(products, many=True)
        if not serializer:
                return response(
                data=serializer.errors,
                status=400,
                message="invalid fields sent"
            )
        return response(
            data=serializer.data,
            status=200,
            message="successfully"
        )
    
    """ PRODUCT BY CATEGORY """
    @action(methods=['get'], detail=False, url_path=r'productbycategory', url_name='productbycategory')
    def productByCategory(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = convertParam(request)
        if 'category' not in data:
            return response(
                data=None,
                status=400,
                message="'category' field was not sent"
            )
        products = Product.objects.filter(category=data['category'])[:30]
        if not products:
            return response(
                data=None,
                status=404,
                message="'there is not any products by this categories"
            )
        serializer = ProductForUserSerializer(products, many=True)
        if not serializer:
            return response(
                data=serializer.errors,
                status=300,
                message="invalid fields was sent"
            )
        return response(
                data=serializer.data,
                status=200,
                message="success"
            )   
            
    """ TOP RATE """
    @action(methods=['get'], detail=False, url_path=r'producttopsell', url_name='producttopsell')
    def productTopRating(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        products = Product.objects.order_by('-rating')[:15]
        if not products:
            return response(
                data=None,
                status=404,
                message="'there is not any products by this categories"
            )
        serializer = ProductForUserSerializer(products, many=True)
        if not serializer:
            return response(
                data=serializer.errors,
                status=300,
                message="invalid fields was sent"
            )
        return response(
                data=serializer.data,
                status=200,
                message="success"
            )   
    
    """ SEARCH PRODUCT """
    @action(methods=['post'], detail=False, url_path=r'searchproduct', url_name='searchproduct')
    def searchProduct(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except:
            return response(
                data=None,
                status=400,
                message="there is no token add in header request"
            )
        check_token = checkToken(token)
        if check_token is False:
            return response(
                data=None,
                status=500,
                message="there is a problem token"
            )
        user = User.objects.filter(id=check_token['id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = request.data
        if 'search_title' not in data:
            return response(
                data=None,
                status=400,
                message="search_title bar was not sent"
            )
        products = Product.objects.filter(title__icontains=data['search_title'])[:20]
        if not products:
            return response(
                data=None,
                status=404,
                message="there is no products the match with this search box"
            )
        serializer = ProductForUserSerializer(products, many=True)
        if not serializer:
            return response(
                data=serializer.errors,
                status=300,
                message="invalid fields was sent"
            )
        return response(
                data=serializer.data,
                status=200,
                message="success"
            )    
        