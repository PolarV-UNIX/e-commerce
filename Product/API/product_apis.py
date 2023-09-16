from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
#CSRF
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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
    ProductForUserSerializer,
    AddSimpleProductSerializer,
    VoteUserSerializer,
    VoteUpdateUserSerializer
)
from User.jwt import checkToken, genrateJWTToken
from User.models import User



class ProductViewSet(ViewSet):
    """ DEFINE DELETE METHOD """
    def delete(self, request):
        pass
    
    """ ADD PRODUCT SIMPLE"""
    @action(methods=['post'], detail=False,url_path=r'addsimpleproduct', url_name='addsimpleproduct')
    def addSimpleProduct(self, request):
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = request.data
        serializer = AddSimpleProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
        return response(
            data=serializer.data,
            status=201,
            message="product successfully created"
        )
        

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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        products = Product.objects.order_by('-created_at')[:60]
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
        user = User.objects.filter(id=check_token['user_id']).first()
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
    @action(methods=['get'], detail=False, url_path=r'addfavorits', url_name='addfavorits')
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
            
        data = convertParam(request)
        if 'product_id' not in data:
            return response(
                data=None,
                status=400,
                message="favorits not sent!"
            )
        if not data['product_id'].isnumeric():
            return response(
                data=None,
                status=400,
                message="tou send an invalid str must and number id"
            )
        product_id = int(data['product_id'])
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return response(
                data=None,
                status=404,
                message="product was not found"
            )
        favorits = user.favorits.all()
        
        favorit_list = []
        for favorit in favorits:
            if favorit == product:
                favorit_list.append(favorit)
            else:
                continue
        
        if product in favorit_list:
            return response(
                    data=None,
                    status=400,
                    message=f"this product {product_id} added before by user {check_token['user_id']}"
                    )
        
        user.favorits.add(product)
        user.save()
        return response(
            data={
                "added_product": product_id,
                "added_by_user": check_token['user_id']
                },
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = convertParam(request)
        if 'product_id' not in data:
            return response(
                data=None,
                status=400,
                message="favorits not sent!"
            )
        if not data['product_id'].isnumeric():
            return response(
                data=None,
                status=400,
                message="tou send an invalid str must and number id"
            )
        product_id = int(data['product_id'])
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return response(
                data=None,
                status=404,
                message="product was not found"
            )
        favorits = user.favorits.all()
        
        favorit_list = []
        for favorit in favorits:
            if favorit == product:
                favorit_list.append(favorit)
            else:
                continue
        
        if product not in favorit_list:
            return response(
                    data=None,
                    status=400,
                    message=f"this product {product_id} deleted before by user {check_token['user_id']}"
                    )
        
        user.favorits.remove(product)
        user.save()
        return response(
            data={
                "deleted_product": product_id,
                "deleted_by_user": check_token['user_id']
                },
            status=200,
            message="add to favorits"
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        favorits = user.favorits.all()  
        if favorits is None:
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
        query = Q()
        for favorit in favorits:
            query |= Q(title__icontains=favorit.title)
            
        products = Product.objects.filter(query)
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
        user = User.objects.filter(id=check_token['user_id']).first()
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
    
        categories = Category.objects.filter(name=data['category']).first()
        if not categories:
            return response(
                data=None,
                status=404,
                message="category not found"
            )
            
        products_by_category = categories.category_by.all()[:20]
        if not products_by_category:
            return response(
                data=None,
                status=404,
                message="'there is not any products by this categories"
            )
        
        serializer = ProductForUserSerializer(products_by_category, many=True)
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        products = Product.objects.order_by('-rate_id__rate')[:15]
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
        user = User.objects.filter(id=check_token['user_id']).first()
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
        
    """ VOTE USER FOR PRODUCT """
    @action(methods=['get'], detail=False, url_path=r'voteuserforproduct', url_name="voteuserforproduct")
    def voteUserForProduct(self, request):
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = convertParam(request)
        if {'product_id', 'rate'}.issubset(data):
            product = Product.objects.filter(id=data['product_id']).first()
            if not product:
                return response(
                    data=None,
                    status=404,
                    message="product not found"
                )
                
            try:
                rate = float(data['rate'])
            except:
                return response(
                    data=None,
                    status=400,
                    message="send the float number"
                )
            if rate is not None and (rate <= 5.0 and rate >= 0.0):
                serializer = VoteUserSerializer(data={
                    'user_id': check_token['user_id'],
                    'rate': data['rate'],
                    'product_id': data['product_id']
                })
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response(
                    data=serializer.data,
                    status=201,
                    message="user's rate accepted"
                )
            
        return response(
                data=None,
                status=400,
                message="Bad request"
            )
        
    """ VOTE USER FOR PRODUCT (update) """
    @action(methods=['get'], detail=False, url_path=r'voteuserforproduct_update', url_name="voteuserforproduct")
    def voteUserForProductUpdate(self, request):
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
        user = User.objects.filter(id=check_token['user_id']).first()
        if not user:
            return response(
                data=None,
                status=404,
                message="user not found"
            )
        data = convertParam(request)
        if {'product_id', 'rate'}.issubset(data):
            product = Product.objects.filter(id=data['product_id']).first()
            if not product:
                return response(
                    data=None,
                    status=404,
                    message="product not found"
                )
            rating = Rating.objects.filter(user_id=check_token['user_id'],product_id=product).first()
            if not rating:
                return response(
                    data=None,
                    status=404,
                    message="there is no rating for this product by this user"
                )
            try:
                rate = float(data['rate'])
            except:
                return response(
                    data=None,
                    status=400,
                    message="send the float number"
                )
            
            if rate is not None and (rate <= 5.0 and rate >= 0.0):
                serializer = VoteUpdateUserSerializer(rating, data={
                    'rate': data['rate'],
                    'product_id': data['product_id']
                })
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response(
                    data=serializer.data,
                    status=201,
                    message="user's rate accepted"
                )
            
        return response(
                data=None,
                status=400,
                message="Bad request"
            )
    