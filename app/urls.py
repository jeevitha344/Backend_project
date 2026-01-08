from django.urls import path
from .views import*



urlpatterns = [
     #---------------logins-------------------------------

    path('signup/',signup_page,name='signup'),
    path('signup_handler/',signup_handler,name='signup_handler'),
    path('login/',login_page,name='login'),
    path('login_handler/',login_handler,name='login_handler'),
    path('logout/',logout_handler,name='logout'),
   
     #---------------userpanal-------------------------------
    path('home/',home_page,name='home'),
    path('products/',products,name='products'),
    path('about/',about_page,name='about'),
    path('contact/',contact_page,name='contact'),

    #---------------adminpanal-------------------------------
    path('admin/',admin_page,name='admin'),
    path('dashboard/',dashboard,name='dashboard'),
    path('product_list/',product_list_page,name='product_list'),
    path('post_page/',post_page,name='post_page'),
   path('product_form/',product_form_page,name='product_form'),
  path('order/',order_page,name='order'),
  path('signupapi/',signupapi.as_view(),name='signupapi'),
  path('loginapi/', loginapi.as_view(), name='loginapi'),
 path('product_handler/',product_handler.as_view(),name='product_list_api'),
path("product_handler/<int:productid>/", product_handler.as_view(), name="product_detail_api"),


  path('edit/<int:productid>/',edit_page,name='edit_page'),
  # path('edit1/<int:productid>/',edit,name='edit1'),
   path('delete/<int:productid>/',delete_page,name='delete_page'),
    # path('delete1/<int:productid>/',delete,name='delete1'),
#   path('dashboard1/',dashboard,name='dashboard'),
    
 #---------------adminpanal-------------------------------



#   path('add_product/',add_product, name='add_product'),
 

    path('category/',categorypage, name='category_page'),

    path('category/<int:cat_id>/',category, name='category'),

    # path('home',home_page,name='home'),
    # path('products',products,name='products'),
    # path('signup',signup_page,name='signup'),
    # path('login',login_page,name='login'),
    # path('signup_handler',signup_handler),
    # path('login_handler',login_handler),
    
]

