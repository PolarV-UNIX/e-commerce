from ..models import Category, Product
from rest_framework import serializers
from User.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', 'discount')


class ProductViewSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'rating', 'price', 'image', 'rating', 'discount')


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'discount', 'rating', 'reviews', 'price', 'discription', 'image')


class SearchSerializer(serializers.ModelSerializer):
    category: CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', 'rating', 'price', 'short_discription', 'rating')
        

class FavoritsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['favorits']
        
    def update(self, instance, validated_data):
        instance.favorits = validated_data['favorits']
        instance.save()
        return instance
    
    
class ProductForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'