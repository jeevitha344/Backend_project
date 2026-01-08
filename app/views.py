from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import  TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.urls import reverse
import json

# Create your views here.

#---------------signup------------------------------------------------------
def signup_page(request):
    return render(request,'signup.html')

#------------------------------------------login--------------------------------------

def login_page(request):
    return render(request,'login.html')
        
#------------------------------------------logout--------------------------------------

def logout_handler(request):

    logout(request)
    return redirect('login')

#------------------------------------------userpanal--------------------------------------

def home_page(request):
    return render(request,'home.html')

def order_page(request):
    return render(request,'order.html')

def products(request):
    product=product_details.objects.all()
    category=products_category.objects.all()
    return render(request,'product.html',{'product':product,"category":category})

def about_page(request):
    return render(request,'about.html')

def contact_page(request):
    return render(request,'contact.html')
#------------------------------------------adminpanal get --------------------------------------

def admin_page(request):
    return render(request,'base.html')

def product_form_page(request):
    return render(request,'product_form.html')

# #------------------------------------------apiview-----------------------------------
# class signupapi(APIView):
#     def post(self,request):
#         try:
#             serializer=signupserializer(data=request.data)
#             if serializer.is_valid():
#                user = serializer.save()
#                refresh_token=RefreshToken.for_user(user)
#                access_token=refresh_token.access_token
#                return Response({"refresh_token":str(refresh_token),"access_token":str(access_token),"data":serializer.data},status=status.HTTP_201_CREATED)
#             else :
#                 return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)     
#         except Exception as e: 
#                  return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

# class loginapi(TokenObtainPairView):
#     permission_classes=[AllowAny]
#     serializer_class=loginserializer

           


# class product_handler(APIView):
#     # parser_classes = [MultiPartParser, FormParser] 
#     def post(self, request):
#         serializer = product_detailsserializer(data=request.data)
#         print(request.FILES)
      
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         else:
#             print(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, productid=None):
#         if productid:
#             try:
#                 product = product_details.objects.get(id=productid)
#                 serializer = product_detailsserializer(product)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Exception:
#                 return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

#         products = product_details.objects.all()
#         serializer = product_detailsserializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self,request,productid=None):
#             if productid:
#                 product=product_details.objects.get(id=productid)
#                 serializer=product_detailsserializer(product,data=request.data)
                
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data,status=status.HTTP_201_CREATED)
#             else:
#                 return Response("id is must")
    

#     def delete(self,request,productid=None):
#             if productid:
#                 product=product_details.objects.get(id=productid)
#                 product.delete()
#                 return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
#             else:
#                 return Response("id is must")



def signup_handler(request):
  
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirmedpassword=request.POST.get("confirmedpassword")

        if password != confirmedpassword:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })
        if User.objects.filter(username=username).exists():
               return redirect('signup')
        elif User.objects.filter(email=email).exists():
               return redirect("signup")

        data={
        "first_name" : first_name,
        "last_name" : last_name,
        "username": username,
        "email": email,
        "password": password
        
        }
    
        try:
            serializer = signupserializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return redirect('login_handler')
        except Exception:
              return render(request, "signup.html", {
            "error": serializer.errors
        })
        
        
    return render(request, "signup.html")


def login_handler(request):
    if request.method == 'POST':
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        serializer = loginserializer(data=data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect("admin")
            else:
                return redirect("home")

        return render(request, "login.html", {
            "errors": serializer.errors
        })

    #  For GET request
    return render(request, "login.html")
             
             
def post_page(request):
    if request.method == "POST":
        data = {
            "product_name": request.POST.get("product_name"),
            "product_price": request.POST.get("product_price"),
            "product_category": request.POST.get("product_category"),
            "product_image": request.FILES.get("product_image"),

        }
        serializer=product_detailsserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('product_list')
        
    return render(request, "product_form.html") #Displays empty form this is  GET request


def edit_page(request, productid=None):
   

    product=product_details.objects.get(id=productid)
    if request.method == "POST": # it run only when submit click
        
        data = {
            "product_name": request.POST.get("product_name"),
            "product_price": request.POST.get("product_price"),
            "product_category": request.POST.get("product_category"),
            "product_image": request.FILES.get("product_image"),
        }
        if productid:
            
            serializer=product_detailsserializer(product,data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect('product_list')
    

    return render(request,'edit.html',{"product":product})
       
       
def delete_page(request, productid):

    if request.method == "POST":
        if productid:
            products=product_details.objects.get(id=productid)
            products.delete()
            return redirect('product_list')
        return render(request, "delete.html", {
            "error": "Delete failed",
             "productid": productid
       })
    return render(request,'delete.html')
       

def product_list_page(request):
    
    products=product_details.objects.all()
    serializer=product_detailsserializer(products,many=True)
    product=serializer.data
   
    return render(request, "product_list.html", {"products": product}) 
    


def dashboard(request):
    total_products = product_details.objects.count()        
    total_categories = products_category.objects.count()
    print("Total Products:", total_products)
    print("Total Categories:", total_categories)

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
    }

    return render(request, 'dashboard.html', context)



def category(request,cat_id=None):
    products=product_details.objects.filter(product_category_id=cat_id )
    print(cat_id)
    return render(request, 'product_cat.html',{"products":products})
   


def categorypage(request):
    category=products_category.objects.all()
    
    return render(request, 'category.html',{"category":category})
    
   

        
       


        