from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home),
    path('about/',views.about),
    path('search=<str:search>',views.wos_search,name="Searching Without Signin"),
    path('signin/',views.signingin),
    path('help/',views.help),
    path('contact/',views.contactus),
    path('register/',views.create_account),

    path('bussinessPage/<int:id>',views.bussiness_page,name="bussiness page"),
    path('bussinessPage/<int:id>/details',views.bussiness_page_details,name="bussiness details"),
    path('bussinessPage/<int:id>/products',views.bussiness_page_product,name="Bussiness Products"),
    path('bussinessPage/<int:id>/add_product',views.bussiness_page_addproduct,name="bussiness details"),
    path('bussinessPage/<int:id>/changeprice',views.bussiness_change_price,name="Product Price Change"),
    path('bussinessPage/<int:id>/discount',views.bussiness_discount,name="Product Discount"),
    path('bussinessPage/<int:id>/remove',views.bussiness_product_remove,name="Product Remove"),
    path('bussinessPage/<int:id>/issue',views.bussiness_issue,name="Issue related query"),
    path('bussinessPage/<int:id>/Products=rating',views.bussiness_product_rating,name="Products rating"),
    path('bussinessPage/<int:id>/Products=rating/<str:pid>',views.bussiness_product_allfeed,name="Products rating feedback"),
    path('bussinessPage/<int:id>/ProductsOrderStatus',views.bussiness_product_managing,name="Products Order Manage"),
    path('bussinessPage/<int:id>/ProductsOrderStatus/productid<str:pid>/manage',views.product_order,name="Products Order"),

    path('home/<int:id>/cart',views.cart,name="Product Saved"),
    path('home/<int:id>/offers',views.offers,name="Gift Offers"),
    path('home/<int:id>',views.customer_home,name="Customer Home"),
    path('home/<int:id>/details',views.details,name="Customer details"),
    path('home/<int:id>/order',views.orders,name="Customer orders"),
    path('home/<int:id>/passwordchange',views.passwordchange,name="Customer Contact"),
    path('home/<int:id>/feedbackform',views.feedback,name="Customer feedback"),
    path('home/<int:id>/addressupdate',views.addressupdate,name="Customer address"),
    path('home/<int:id>/search<str:searchvalue>/',views.searching_page,name='searching'),
    path('home/<int:id>/purchase/<str:pid>',views.purchase,name="purchase"),
    path('home/<int:id>/purchase/<str:pid>/placed-order',views.confirmed,name="Order Placed"),
] 