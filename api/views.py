from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Products,carts,Reviews
from api.serializers import ProductModelSerializer,Userserializer, cartserializer,Reviewserializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions



class Productsview(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        serializer=ProductModelSerializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=ProductModelSerializer(data=request.data)

        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class ProductsDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        serializer=ProductModelSerializer(qs,many=False)
        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        id=kwargs.get("id")
        Products.objects.filter(id=id).update(**request.data)
        qs=Products.objects.get(id=id)
        serializer=ProductModelSerializer(qs,many=False)
        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        id=kwargs.get("id")
        Products.objects.filter(id=id).delete()
        return Response(data="object deleted")



class ProductViewsetView(viewsets.ModelViewSet):
    serializer_class =ProductModelSerializer
    queryset = Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #     def list(self,request,*args,**kwargs):
#         qs=Products.objects.all()
#         serializer=ProductModelSerializer(qs,many=True)
#         return Response(data=serializer.data)
#
#     def create(self,request,*args,**kwargs):
#         serializer=ProductModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
#
#     def retrieve(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         qs=Products.objects.get(id=id)
#         serializer=ProductModelSerializer(qs,many=False)
#         return Response(data=serializer.data)
#      def destroy(self,request,*args,**kwargs):
#          id=kwargs.get("pk")
#          Products.objects.filter(id=id).delete()
#          return Response(data="deleted")
#
#
# def update(self, request, *args, **kwargs):
#     id = kwargs.get("pk")
#     obj = Products.objects.get(id=id)
#     serializer = ProductModelSerializer(data=request.data, instance=obj)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(data=serializer.data)
#     else:
#         return Response(data=serializer.errors)
#     def destroy(self,request,*args,**kwargs):
#         id=kwargs.get("pk")

    @action(methods=["GET"],detail=False)
    def categories(self,request,*args,**kwargs):
        res=Products.objects.values_list("category",flat=True).distinct()
        return Response(data=res)

    @action(methods=["POST"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        item = Products.objects.get(id=id)
        user = request.user
        user.carts_set.create(product=item)
        return Response(data="item added to cart")

#review add cheyan
    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get("pk")
        object=Products.objects.get(id=id)
        serializer=Reviewserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=object,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
#review
    @action(methods=["GET"],detail=True)
    def review(self,request,*args,**kwargs):
        product=self.get_object()
        qs=product.reviews_set.all()
        serializer=Reviewserializer(qs,many=True)
        return Response(data=serializer.data)




class cartsView(viewsets.ModelViewSet):
    serializer_class =cartserializer
    queryset = carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def list(self, request, *args, **kwargs):
        qs=request.user.carts_set.all()
        serializer=cartserializer(qs,many=True)
        return Response(data=serializer.data)



class UsersView(viewsets.ModelViewSet):
    serializer_class = Userserializer
    queryset = User.objects.all()



    # def create(self,request,*args,**kwargs):
    #     serializer=Userserializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)




