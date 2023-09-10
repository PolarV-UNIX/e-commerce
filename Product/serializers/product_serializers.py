from ..models import Category, Product
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', 'discount')


class HomePageSerializer(serializers.ModelSerializer):
    discount: DiscountSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'rating', 'price', 'image', 'rating')


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'discount', 'rating', 'reviews', 'price', 'discription', 'image', 'rating')


class SearchSerializer(serializers.ModelSerializer):
    category: CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', 'rating', 'price', 'short_discription', 'rating')