from rest_framework import serializers
from .models import User, Publisher, Book, Customer, Cart, Order, Payment,Company

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} 

class UsercreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} 


    class Meta:
        model = Publisher 
        fields ='__all__'

class PublishercreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher 
        fields ='__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ='__all__'

class PublisherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company= CompanySerializer()

    class Meta:
        model = Publisher 
        fields ='__all__'

class BookSerializer(serializers.ModelSerializer):
    publisher=PublisherSerializer()
    class Meta:
        model = Book
        fields = '__all__'

class BookcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

class CustomercreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

        
class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    books = BookSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
     
        
class CartcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = '__all__'

class OrdercreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentcreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Payment
        fields = '__all__'
        
