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
                getqueryset = getqueryset.filter(productCategory__name=filter_word) #search by productname
                # getqueryset_productdescription = getqueryset.filter(productDescription__icontains=filter_word) #search by productdescription
                # getqueryset = getqueryset_productname | getqueryset_productdescription
                
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
            getqueryset = models.Cart.objects.filter(user=uid)##GET request for a specific orderdedUserID
            if not getqueryset.exists():
                temp = models.Cart.objects.create(user=currentUser,price=0)
                temp.save()
                getqueryset = models.Cart.objects.filter(user=uid)##GET request for a specific orderdedUserID
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
        product = models.Products.objects.filter(product=models.ProductModel.objects.filter(productID=request.data['productId'])[0], user=currentUser)
        if product.exists():
            product = product[0]
        else:
            product = models.Products.objects.create(product=models.ProductModel.objects.filter(productID=request.data['productId'])[0], quantity=1, user=currentUser)
            product.save()

        cart = models.Cart.objects.filter(user=currentUser)
        if cart.exists():
            cart = cart[0]
            for pro in cart.products.all():

                if pro.product.productID == product.product.productID and cart.user == currentUser:
                    product.quantity += 1
                    cart.price = cart.price + product.product.productPrice
                    product.save()
                    cart.save()
                    break
            else:
                cart.products.add(product)
                cart.price = cart.price + product.product.productPrice
                cart.save()
        else:
            cart = models.Cart.objects.create(user=currentUser)
            cart.products.add(product)
            cart.price = product.product.productPrice
            cart.save()
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
        products = models.Products.objects.get(product=product, user=currentUser)
        for pro in cart.products.all():
            if pro.product.productID == product.productID:
                cart.products.remove(products)
                
                cart.price = cart.price - product.productPrice * pro.quantity
                cart.save()
                models.Products.objects.get(product=product, user=currentUser).delete()
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
        product = models.Products.objects.get(productsId=int(uid), user=currentUser)
        for pro in cart.products.all():
            if pro.product.productID == product.product.productID:
                cart.price = cart.price - product.product.productPrice
                cart.save()
                if product.quantity > 1:
                    product.quantity = product.quantity - 1 
                    product.save()
                else:
                    cart.products.remove(product)
                    models.Products.objects.get(product=int(uid), user=currentUser).delete()
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