from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
import json
from django.http import HttpResponse
import random
import string
import razorpay
client = razorpay.Client(auth=("rzp_test_mp6FNCpzegnAZh", "rhclOvFrgFHEGSbK0YRwvXTN"))
# class UserListView(generics.ListAPIView):
#     queryset = models.CustomUser.objects.all()
#     serializer_class = serializers.UserSerializer
    

class UserView(generics.CreateAPIView,generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    def get(self, request, uid,format=None):
        if uid is "0":
            getqueryset = models.CustomUser.objects.all()
            getserializer = serializers.UserSerializer(getqueryset, many=True)
            return Response(data=getserializer.data, status=status.HTTP_200_OK)
        else:
            getqueryset = models.CustomUser.objects.filter(userName=uid) ##GET request for a specific email
            if getqueryset.exists():
                getqueryset = getqueryset[0]
                getserializer = serializers.UserSerializer(getqueryset, many=False)
                return Response(data=getserializer.data, status=status.HTTP_200_OK)
            return Response(data="NO", status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        putqueryset = models.CustomUser.objects.get(userName=request.data['email'])
        putserializer = serializers.UserSerializer(putqueryset, data=request.data)
        if putserializer.is_valid():
            putserializer.save()
            return Response(data=putserializer.data, status=status.HTTP_202_ACCEPTED)


class ProductView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, uid, format=None):
        if uid is 0:
            getqueryset = models.ProductModel.objects.all()
            filter_word = request.query_params.get('search', '') #search
            if filter_word: #search filter
                getqueryset_productcategory = getqueryset.filter(productCategory__name__icontains=filter_word) #search by product category
                getqueryset_productname = getqueryset.filter(productName__icontains=filter_word) #search by product name
                getqueryset_productdescription = getqueryset.filter(productDescription__icontains=filter_word) #search by product Description
                getqueryset = getqueryset_productname | getqueryset_productcategory | getqueryset_productdescription
                
            getserializer = serializers.ProductSerializer(getqueryset, many=True)
        else:
            getqueryset = models.ProductModel.objects.filter(productID = uid) ##GET request for a specific ProductID
            if getqueryset.exists():
                getqueryset = getqueryset[0]
                getserializer = serializers.ProductSerializer(getqueryset, many=False)
            else:
                return Response(data="No", status=status.HTTP_204_NO_CONTENT)
        return Response(data=getserializer.data, status=status.HTTP_200_OK)

class CartView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    def get(self, request, uid,format=None):
        if uid is "0":
            getqueryset = models.Cart.objects.all()
            getserializer = serializers.CartSerializer(getqueryset, many=True)
        else:
            print(uid)
            currentUser = models.CustomUser.objects.get(userName__id=int(uid))
            print(currentUser.userName)
            getqueryset = models.Cart.objects.filter(user=currentUser, paymentDone=False)##GET request for a specific orderdedUserID
            if not getqueryset.exists():
                temp = models.Cart.objects.create(user=currentUser,price=0)
                temp.save()
                getqueryset = models.Cart.objects.filter(user=uid, paymentDone=False)##GET request for a specific orderdedUserID
            getserializer = serializers.CartSerializer(getqueryset, many=True)
        return Response(data=getserializer.data, status=status.HTTP_200_OK)

class AddToCart(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductsSerializer

    def post(self, request, format=None):
        print(request, request.data)
        currentUser = models.CustomUser.objects.get(userName__id=int(request.data['user']))
        product = models.Products.objects.filter(product=models.ProductModel.objects.filter(productID=request.data['productId'])[0], user=currentUser, ordered=False)
        if product.exists():
            product = product[0]
        else:
            product = models.Products.objects.create(product=models.ProductModel.objects.filter(productID=request.data['productId'])[0], quantity=1, user=currentUser)
            product.save()

        cart = models.Cart.objects.filter(user=currentUser, paymentDone=False)
        print(cart, product, currentUser)
        if cart.exists():
            cart = cart[0]
            print("cart exists")
            for pro in cart.products.all():
                print("cart loop in")
                if pro.product.productID == product.product.productID and cart.user == currentUser:
                    product.quantity += 1
                    print("cart loop in for")
                    cart.price = cart.price + product.product.productPrice
                    product.save()
                    cart.save()
                    break
            else:
                print("else")
                cart.products.add(product)
                cart.price = cart.price + product.product.productPrice
                cart.save()
        # else:
        #     print("outer lese")
        #     cart = models.Cart.objects.create(user=currentUser)
        #     cart.products.add(product)
        #     cart.price = product.product.productPrice
        #     cart.save()
        return Response(data="yes", status=status.HTTP_200_OK)

class DeleteFromCart(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductsSerializer

    def delete(self, request, uid, cartId, userId):
        currentUser = models.CustomUser.objects.get(userName__id=int(userId))
        cart = models.Cart.objects.get(cartId=int(cartId))
        product = models.ProductModel.objects.get(productID=int(uid))
        print(product)
        products = models.Products.objects.get(product=product, user=currentUser, ordered=False)
        for pro in cart.products.all():
            if pro.product.productID == product.productID:
                cart.products.remove(products)
                
                cart.price = cart.price - product.productPrice * pro.quantity
                cart.save()
                models.Products.objects.get(product=product, user=currentUser, ordered=False).delete()
                return Response(data="yes", status=status.HTTP_200_OK)
        return Response(data="No", status=status.HTTP_404_NOT_FOUND)

class DecreaseFromCart(generics.UpdateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductsSerializer

    def put(self, request, uid, cartId, userId):
        currentUser = models.CustomUser.objects.get(userName__id=int(userId))
        cart = models.Cart.objects.get(cartId=int(cartId))
        product = models.Products.objects.get(productsId=int(uid), user=currentUser, ordered=False)
        for pro in cart.products.all():
            if pro.product.productID == product.product.productID:
                cart.price = cart.price - product.product.productPrice
                cart.save()
                if product.quantity > 1:
                    product.quantity = product.quantity - 1 
                    product.save()
                else:
                    cart.products.remove(product)
                    models.Products.objects.get(product=int(uid), user=currentUser, ordered=False).delete()
                cart.save()
                return Response(data="yes", status=status.HTTP_200_OK)
        return Response(data="No", status=status.HTTP_404_NOT_FOUND)

class GetCategory(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request, format=None):
        getqueryset = models.Category.objects.all()
        getserializer = serializers.CategorySerializer(getqueryset, many=True)
        return Response(data=getserializer.data, status=status.HTTP_200_OK)

class UserId(APIView):
  authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    print("hello >>>", request.data['headers']['Authorization'].split(' ')[1])
    queryset = Token.objects.filter(key=request.data['headers']['Authorization'].split(' ')[1])
    serializer = serializers.UseridSerializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

class CartProducts(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, format=None):
        print(request.query_params.get('products', ''))
        products_nums = str(request.query_params.get('products', ''))
        products = products_nums.split(',')
        response_data = []
        for i in products:
            temp = {}
            cart_product = models.Products.objects.filter(productsId=i, ordered=False)
            if cart_product.exists():
                cart_product = cart_product[0]
                temp['productsId'] = cart_product.productsId
                temp['productid'] = cart_product.product.productID
                temp['productName'] = cart_product.product.productName
                temp['productPrice'] = cart_product.product.productPrice
                temp['productImage'] = "/media/" +str(cart_product.product.productImage)
                print(str(cart_product.product.productImage))
                temp['quantity'] = cart_product.quantity
                response_data.append(temp)
        print(response_data)
        return Response(data=response_data, status=status.HTTP_200_OK)

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class CheckOutView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def post(self, request, format=None):
        amount = request.data['amount']
        razorpayResponse = client.order.create(dict(amount=amount*100, currency="INR", receipt=create_ref_code()))
        order_id = razorpayResponse['id']
        order_status = razorpayResponse['status']
        if order_status=='created':
            return Response(data=razorpayResponse, status=status.HTTP_200_OK)
        return Response(data=0, status=status.HTTP_200_OK)

class CheckPaymentStatus(APIView):

    def post(self, request, format=None):
        print(request.data)
        cart_id = int(request.data['cartID'])
        params_dict = {
            'razorpay_payment_id' : request.data['razorpay_payment_id'],
            'razorpay_order_id' : request.data['razorpay_order_id'],
            'razorpay_signature' : request.data['razorpay_signature']
        }
        try:
            response = client.order.fetch(params_dict['razorpay_order_id'])
            print("status", response)
            if response['status'] == "paid" and response['amount_due'] == 0:
                cart = models.Cart.objects.get(cartId=cart_id)
                cart.paymentMethod = "Online"
                cart.paymentDone = True
                cart.save()
                for pro in cart.products.all():
                    pro.ordered = True
                    pro.save()
                # cart.save()
                return Response(data=1, status=status.HTTP_200_OK)
            return Response(data=0, status=status.HTTP_200_OK)
        except:
            return Response(data=0, status=status.HTTP_200_OK)

class OrderedProducts(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        currentUser = models.CustomUser.objects.get(userName__id=int(user_id))
        response = []
        carts = models.Cart.objects.filter(user=currentUser, paymentDone=True)
        if carts.exists():
            for cart in carts:
                temp = {}
                temp['cartId'] = cart.cartId
                temp['price'] = cart.price
                temp['paymentMethod'] = cart.paymentMethod
                temp_list = []
                for pro in cart.products.all():
                    temp_dict = {}
                    product = models.Products.objects.get(productsId=pro.productsId)
                    temp_dict['productID'] = product.product.productID
                    temp_dict['productName'] = product.product.productName
                    temp_dict['productPrice'] = product.product.productPrice
                    temp_dict['quantity'] = product.quantity
                    temp_dict['productImage'] = "/media/" +str(product.product.productImage)
                    temp_list.append(temp_dict)
                temp['products'] = temp_list
                response.append(temp)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=0, status=status.HTTP_200_OK)