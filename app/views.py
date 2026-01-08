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


# def signup_handler(request):

# #     context = {
# #     "error":"",
# #     "error1":"",
# #     "error2":"",

# # }

#     if request.method == 'POST':
       

#         firstname=request.POST.get("firstname")
#         lastname=request.POST.get("lastname")
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         confirmedpassword=request.POST.get("confirmedpassword")

#         # if not username :
#         #     context["error1"] = "*Username is required"

#         # if  not  password:
            
#         #     context["error2"]="*password is required"

#         # if context["error1"] or context["error2"]:

#             # return render(request, "signup.html", context)
#         # return render(request, "signup.html")

#         if password == confirmedpassword:
#             if User.objects.filter(username=username).exists():
#                 return redirect('signup')
#             elif User.objects.filter(email=email).exists():
#                 return redirect("signup")
#             else:
               
#                 userinfo=User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username,password=password)
#                 # user= userinfo.save()
#                 refresh_token=RefreshToken.for_user(userinfo)
#                 access_token=refresh_token.access_token
#                 print(refresh_token)
#                 print(access_token)
#                 return redirect("login")
#         else:
#             return redirect("signup")



#------------------------------------------login--------------------------------------

def login_page(request):
    return render(request,'login.html')
        
# def login_handler(request):

# #     context = {
# #     "error":"",
# #     "error1":"",
# #     "error2":"",

# # }

#     if request.method == 'POST':
#         username=request.POST.get("username")
#         password=request.POST.get("password")



#         # if  not username:
#         #     context["error1"] = "*Username is required"

#         # if  not password:
            
#         #     context["error2"]="*password is required"

#         # if context["error1"] or context["error2"]:

#         #     return render(request, "login.html", context)
            
#         user = authenticate(username=username,password=password)
        
#         if user is not None:
#             login(request,user)
#             print(user)
#             refresh_token = RefreshToken.for_user(user)
#             access_token = refresh_token.access_token
#             print("refersh token",refresh_token)
#             print("access token",access_token)
#             # if user == 'ADMIN':
#             if user.is_superuser or user.is_staff:
#                 return redirect("admin")
#             else:
#                 return redirect("home")
#         else :  
#             # context ["error"]="*Invalid  username or password"     
#         # return render(request,"login.html",context)
#          return render(request,"login.html")
        
#     return render(request,'login.html')

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

# def dashboard_page(request):
#     return render(request,'dashboard.html')

# def product_list_page(request):
#     return render(request,'product_list.html')

def product_form_page(request):
    return render(request,'product_form.html')

# def edit(request,productid):
#     # product = product_details.objects.get(id=productid)
#     return render(request, 'edit.html', {'productid': productid})

# def delete(request,productid):
#     # product = product_details.objects.get(id=productid)
#     return render(request, 'delete.html', {'productid': productid})


#------------------------------------------apiview--------------------------------------
class signupapi(APIView):
    def post(self,request):
        try:
            serializer=signupserializer(data=request.data)
            if serializer.is_valid():
               user= serializer.save()
               refresh_token=RefreshToken.for_user(user)
               access_token=refresh_token.access_token
               return Response({"refresh_token":str(refresh_token),"access_token":str(access_token),"data":serializer.data},status=status.HTTP_201_CREATED)
            else :
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)     
        except Exception as e: 
                 return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

class loginapi(TokenObtainPairView):
    permission_classes=[AllowAny]
    serializer_class=loginserializer

           


class product_handler(APIView):
    # parser_classes = [MultiPartParser, FormParser] 
    def post(self, request):
        serializer = product_detailsserializer(data=request.data)
        print(request.FILES)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, productid=None):
        if productid:
            try:
                product = product_details.objects.get(id=productid)
                serializer = product_detailsserializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        products = product_details.objects.all()
        serializer = product_detailsserializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,productid=None):
            if productid:
                product=product_details.objects.get(id=productid)
                serializer=product_detailsserializer(product,data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response("id is must")
    

    def delete(self,request,productid=None):
            if productid:
                product=product_details.objects.get(id=productid)
                product.delete()
                return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("id is must")
#------------------------------------------adminpanal post --------------------------------------



# def post_page(request):
#     if request.method == "POST":
#         data = {
#             "product_name": request.POST.get("product_name"),
#             "product_price": request.POST.get("product_price"),
#             "product_category": request.POST.get("product_category"),  # ✅ FIXED
#             "product_image": request.POST.get("product_image"),
#         }

#         try:
#             response = requests.post(
#                 "http://127.0.0.1:8000/app/product_handler/",
#                 json=data  # ✅ FIXED
#             )
#         except requests.exceptions.RequestException:
#             return render(request, "product_form.html", {
#                 "error": "API server not reachable"
#             })

#         if response.status_code == 201:
#             return redirect("product_list")

#         return render(request, "product_form.html", {
#             "error": response.json()
#         })

#     return render(request, "product_form.html")


# def signup_handler(request):
#     url1="http://127.0.0.1:8000/app/signupapi/" 
#     if request.method == "POST":
#         firstname = request.POST.get("firstname")
#         lastname = request.POST.get("lastname")
        
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         confirmedpassword=request.POST.get("confirmedpassword")

#         if password != confirmedpassword:
#             return render(request, "signup.html", {
#                 "error": "Passwords do not match"
#             })
#         if User.objects.filter(username=username).exists():
#                return redirect('signup')
#         elif User.objects.filter(email=email).exists():
#                return redirect("signup")
        

#         data={
#              "first_name":firstname,
#              "last_name":lastname,
#              "username":username,
#              "email":email,
#              "password":password,
             
#         }
#         try:
#          response =requests.post(
#                 url1,
#                 data=data,
#             )
#         except requests.exceptions.RequestException:
#             return render(request, "signup.html", {
#                 "error": "API server not reachable"
#            })
#         if response.status_code == 201:
#             return redirect("login")

#         return render(request, "signup.html", {"error": response.json()})
#     return render(request, "signup.html")


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

    # ✅ For GET request
    return render(request, "login.html")
             
             
        
     





# def login_handler(request):
#  url2 = "http://127.0.0.1:8000/app/loginapi/"
#  if request.method == 'POST':
       
#         data={
#             "username":request.POST.get("username"),
#             "password":request.POST.get("password"),
#         }
        

#         response= requests.post(
#             url2,
#             data=data
#         )
        
        
     
#         if response.status_code == 200:
#             tokens = response.json()
#             request.session["access_token"] = tokens["access"]
#             request.session["refresh_token"] = tokens["refresh"]
#             user = User.objects.get(username=data["username"])
#             print(user)
#             if user.is_superuser or user.is_staff:
               
#                     return redirect("admin")
#             else:
#                     return redirect("home")
           
#         return render(request, "login.html", {"error": "Invalid credentials"})
    
#  return render(request, "login.html")




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



# def post_page(request):
#     if request.method == "POST":
#         data = {
#             "product_name": request.POST.get("product_name"),
#             "product_price": request.POST.get("product_price"),
#             "product_category": request.POST.get("product_category"),
#             "product_image": request.POST.get("product_image"),

#         }
#         files={
#             "product_image": request.FILES.get("product_image")
#         }
#         # files = {}
#         # if "product_image" in request.FILES:
#         #     files["product_image"] = request.FILES["product_image"]
        
#         # url="http://127.0.0.1:8000/app/product_handler/" # app/apiclass_path
#         url = request.build_absolute_uri(reverse("product_list_api"))

#         try:
#                 response = requests.post(
                    
#                     url,
#                     data=data,
#                     files=files
#                 )
#         except requests.exceptions.RequestException:
#             return render(request, "product_form.html", {"error": "API server not reachable"})

#         if response.status_code == 201:
#             return redirect("product_list")

#         return render(request, "product_form.html", {"error": response.json()})

#     return render(request, "product_form.html") #Displays empty form this is  GET request



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
       
       









# def edit_page(request, productid):
#     url = request.build_absolute_uri(
#     reverse("product_detail_api", args=[productid]) #url="http://127.0.0.1:8000/app/product_handler/id" # app/apiclass_path
# )# url contain Endpoint path  # We give the URL because API only understands
# # requests made to its endpoint, and the ID in the URL tells which product to act on.


#     if request.method == "POST": # it run only when submit click
#         data = {
#             "product_name": request.POST.get("product_name"),
#             "product_price": request.POST.get("product_price"),
#             "product_category": request.POST.get("product_category"),
#             # "product_image": request.POST.get("product_image"),
#         }
#         files={
#             "product_image": request.FILES.get("product_image")
#         }
#         # files = {}
#         # if "product_image" in request.FILES:
#         #     files["product_image"] = request.FILES["product_image"]
#         # else:
#         #     data["product_image"] = request.POST.get["product_image"] 

#         response = requests.put(url, data=data,files=files)
#         print(response.status_code, response.text)  # debug

#         if response.status_code in [200, 201]:
#             return redirect("product_list")

#         return render(request, "edit.html", {
#             "error": response.text,
#             "product": data,
#             "productid": productid
#         })

#     #   firstly this will work  when user click the GET request  call then  it call to api and
#     #  fetch the data  then the form get loaded with the previous data  after that  the user can sent the edit data
#     response = requests.get(url)
#     if response.status_code == 200:
#         product = response.json()
#         return render(request, "edit.html", {"product": product, "productid": productid})

#     return redirect("product_list")  # When does this run  
# # ONLY IF:

# # API returns error (404 / 500)

# # Product does not exist

# #--------------------------------------------







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
    

# def delete_page(request, productid):
#     url = request.build_absolute_uri(
#     reverse("product_detail_api", args=[productid])
# )

    
#     if request.method == "POST":
#         response = requests.delete(url)
#         if response.status_code == 204:
#             return redirect("product_list")

#         return render(request, "delete.html", {
#             "error": "Delete failed",
#             "productid": productid
#         })

#     return render(request, "delete.html", {"productid": productid})



# def product_list_page(request):
#     url = request.build_absolute_uri(reverse("product_list_api"))
#     response = requests.get(url)
#     products = response.json()
#     return render(request, "product_list.html", {"products": products})





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
    
   

















# orm -------------------------------------------------------------------------

# def post_page(request):
#     if request.method == "POST":
#         name = request.POST.get("product_name")
#         price = request.POST.get("product_price")
#         category_id = request.POST.get("product_category")
#         image = request.POST.get("product_image")


#         product_details.objects.create(
#             product_name=name,
#             product_price=price,
#             product_category_id=category_id,   # ✅ pass object
#             product_image=image          # ✅ FILES
#         )

#         return redirect("product_list")

#     # products= product_details.objects.all()
#     # return render(request, "product_list.html", {"products": products})


# def product_list_page(request):
#         products=product_details.objects.all()
#         return render(request,'product_list.html',{'products':products})


# def edit_page(request, productid=None):
#     product = product_details.objects.get(id=productid)

#     if request.method == 'POST':
#         product.product_name = request.POST.get('product_name')
#         product.product_price = request.POST.get('product_price')
#         product.product_category_id=request.POST.get('product_category')
#         product.product_image=request.POST.get('product_image')
#         product.save()
#         return redirect('product_list')
    
# def delete_page(request, productid=None):
#     product = product_details.objects.get(id=productid)

#     if request.method == 'POST':
#         product.delete()
#         return redirect('product_list')
    


#-----------------------------------------------------------------------------------------------------------------#















# class product_handler(APIView):

#     def post(self,request):
#         try:
#              serializer=product_detailsserializer(data=request.data)
             
#              if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_201_CREATED)
#         except Exception as e:
           
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def get(self,request):
#         try:
#             product=product_details.objects.all()
#             serializer=product_detailsserializer(product)
#             return Response(request,product,status=status.HTTP_201_CREATED)

#         except Exception:

#             return Response(status=status.HTTP_400_BAD_REQUEST)



# def add_product(request):
#     if request.method == "POST":
#         data = {
#             "product_name": request.POST.get("product_name"),
#             "product_price": request.POST.get("product_price"),
#             "product_category": request.POST.get("product_category"),
#             "product_description": request.POST.get("product_description"),
#         }

#         files = {
#             "product_image": request.FILES.get("product_image")
#         }

#         # call API
#         requests.post(
#             "http://127.0.0.1:8000/product_handler/",
#             data=data,
#             files=files
#         )

#         # AFTER saving → redirect to list page
#         return redirect("product_list")



        

 
    # def put(self,request,productid):
    #     try:
    #         if productid:
    #             product=product_details.objects.get(id=productid)
    #             serializer=product_detailsserializer(product,request.data)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 return Response(
    #                  {"message":"product data get updated","data":serializer.data},

    #                  status=status.HTTP_200_OK
    #                 )
    #             else:
    #                 return Response({"message":"id must"})
    #     except  Exception :
    #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        





# def product_list_page(request):
#     response = requests.get("http://127.0.0.1:8000/app/product_handler/")
#     products = response.json()  # API response
#     return render(request, "product_list.html", {"products": products})




# def categories(request):
#     #variable = tablename.objects.all()
#     categories = products_category.objects.all()  # Get all categories from DB
#     return render(request, 'category.html', {'categories': categories})

# def products_by_category(request, cat_id):
#     #variable = tablename.objects.all()
#     products = product_details.objects.filter(product_category_id=cat_id)  # Only products of this category
#     # categories = products_category.objects.all()   , 'categories': categories  # Sidebar or dropdown if needed
#     return render(request, 'product_cat.html', {'products': products})

       
## if User.objects.filter(username=username).exists() and User.objects.filter(password=password).exists():
#--------------------------------------------
# Takes the username entered by the user
# Takes the password entered by the user
# Django:
# Finds the user with that username
# Hashes the password
# Compares it with the stored password
# If both are correct → returns a User object
# If wrong → returns None
#authenticate() checks login credentials and gives you the user object if valid, otherwise None.
# authenticate is a Django function
# It comes from django.contrib.auth
# It checks username & password against the database

        
       


        