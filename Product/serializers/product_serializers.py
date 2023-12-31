from ..models import Category, Product, Rating
from rest_framework import serializers
from User.models import User




""" ADD PRODUCT SERIALIZER """
class AddSimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'price']
        
    def create(self, validated_data):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$", validated_data)
        if {'title', 'price'}.issubset(validated_data): 
            if validated_data['title'] is None and validated_data['price'] is None:
                raise serializers.ValidationError(
                    "can't send empety value"
                ) 
            product = Product.objects.create(
                title=validated_data['title'],
                price=validated_data['price']
            )
            return product
        else:
            raise serializers.ValidationError(
                "send the fields title and price"
            )



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', 'discount')


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'rate_id', 'price', 'image_id', 'discount')


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'discount', 'rate_id', 'price', 'discription', 'image_id')


class SearchSerializer(serializers.ModelSerializer):
    category: CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', 'rating', 'price', 'short_discription', 'rating')
        

""" FAVORITS SERIAZLIER """
class FavoritsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['favorits']
        
    def update(self, instance, validated_data):
        print("$$$$$$$$$$$$$$$$$$$$$$", validated_data)
        instance.favorits = validated_data['favorits']
        instance.save()
        return instance
    
    
class ProductForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'rate_id']
        

""" VOTE SERIAIZER """
class VoteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user_id', 'rate', 'product_id']
        
    def create(self, validated_data):
        rate_object = Rating.objects.create(
            user_id=validated_data['user_id'],
            rate=validated_data['rate'],
            product_id=validated_data['product_id']
        )
        return rate_object
    
    def update(self, instance, validated_data):
        instance.rate = validated_data['rate']
        instance.save()
        return instance
    
class VoteUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'product_id']
        
    def update(self, instance, validated_data):
        instance.rate = validated_data['rate']
        instance.save()
        return instance