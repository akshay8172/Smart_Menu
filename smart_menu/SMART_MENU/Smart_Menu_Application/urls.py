from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('admin_dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('manage_tables', views.manage_tables, name='manage_tables'),
    path('manage_chefs', views.manage_chefs, name='manage_chefs'),
    path('admin_add_new_chef',views.admin_add_new_chef,name='admin_add_new_chef'),
    path('manage_delivery_staffs',views.manage_delivery_staffs,name='manage_delivery_staffs'),
    path('admin_add_new_delivery_staff',views.admin_add_new_delivery_staff,name='admin_add_new_delivery_staff'),
    path('edit_delivery_staff/<id>',views.edit_delivery_staff,name='edit_delivery_staff'),
    
    path('menu/manage/', views.manage_menu_items, name='manage_menu_items'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    
    path('category/add/', views.add_category, name='add_category'),
    path('view_ratings_reviews', views.view_ratings_reviews, name='view_ratings_reviews'),
    path('view_bills_payments', views.view_bills_payments, name='view_bills_payments'),
    path('view_order_reports', views.view_order_reports, name='view_order_reports'),
    path('manage_tables/', views.manage_tables, name='manage_tables'),
    path('add_table/', views.add_table, name='add_table'),
    path('edit_table/<int:table_id>/', views.edit_table, name='edit_table'),
    path('delete_table/<int:table_id>/', views.delete_table, name='delete_table'),
    path('table/<int:table_number>/', views.table_detail, name='table_detail'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('manage_offers/', views.manage_offers, name='manage_offers'),
    path('edit_offer/<int:id>/', views.edit_offer, name='edit_offer'),
    path('delete_offer/<int:id>/', views.delete_offer, name='delete_offer'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove_item/<id>', views.remove_item, name='remove_item'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('set-table/<int:table_number>/', views.set_table_number, name='set_table'),
    path('buy_now/<int:item_id>/<int:table_number>/', views.buy_now, name='buy_now'),
    path('order_status/<int:table_number>/', views.order_status, name='order_status'),  # Correct pattern
    path('checkout/', views.checkout_view, name='checkout'),
    path('ratings/<int:table_number>/', views.ratings, name='ratings'),
    # path('payment/<id>', views.payment, name='pay'),
    
    
    path('on_payment_success',views.on_payment_success),
    path('user_pay_proceed/<id>/<amt>',views.user_pay_proceed),
    
    
    
    
    path('kitchen_home', views.kitchen_home, name='kitchen_home'),
    path('accept_order/<id>', views.accept_order, name='accept_order'),
    path('assign_order/<id>', views.assign_order, name='assign_order'),
    path('staff_manage_products', views.staff_manage_products, name='staff_manage_products'),
    
    
    
    path('delivery_home', views.delivery_home, name='delivery_home'),




    
]
