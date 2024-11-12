from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from.models import *
import qrcode # type: ignore
import qrcode.image.svg # type: ignore
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib import messages
from decimal import Decimal
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.urls import reverse
from decimal import Decimal
from django.db.models import F, Sum



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def admin_dashboard(request):
    return render(request, 'admin/admin_home.html')


def login(request):
    if 'submit' in request.POST:
        user_name = request.POST['username']
        password = request.POST['password']
        
        login_fetch = LoginTable.objects.filter(username=user_name, password=password)
        if login_fetch.exists():
            login_objects = LoginTable.objects.get(username=user_name, password=password)
            request.session['lid'] = login_objects.id
            
            user_role = login_objects.role
            
            if user_role == 'admin':
                return redirect("/admin_dashboard")
            elif user_role == 'kitchen_staff':
                return redirect("/kitchen_home")
            elif user_role == 'delivery_staff':
                return redirect("/delivery_home")
            else:
                return HttpResponse('''<script>alert("Invalid Credentials"); window.location = "/";</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid Credentials"); window.location = "/";</script>''')
    else:
        return render(request, 'login.html')


def manage_tables(request):
    tables = RestaurantTable.objects.all()  # Fetch all tables from the database
    return render(request, 'admin/manage_tables.html', {'tables': tables})

def generate_qr_code(table):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    url = table.get_absolute_url()
    qr.add_data(f'http://192.168.98.206:8000{url}')  
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    qr_image = ContentFile(byte_io.getvalue())
    return qr_image

def add_table(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        if RestaurantTable.objects.filter(table_number=table_number).exists():
            messages.error(request, 'Table number already exists.')
            return redirect('add_table')

        table = RestaurantTable(table_number=table_number)
        qr_image = generate_qr_code(table)
        table.qr_code.save(f'table_{table_number}_qr.png', qr_image, save=False)
        table.save()
        messages.success(request, f'Table {table_number} added successfully.')
        return redirect('manage_tables')
    return render(request, 'admin/add_table.html')


def edit_table(request, table_id):
    table = RestaurantTable.objects.get(id=table_id)
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        if RestaurantTable.objects.filter(table_number=table_number).exclude(id=table_id).exists():
            messages.error(request, 'Table number already exists.')
            return redirect('edit_table', table_id=table_id)

        table.table_number = table_number
        qr_image = generate_qr_code(table)
        table.qr_code.save(f'table_{table_number}_qr.png', qr_image, save=False)
        table.save()
        messages.success(request, f'Table {table_number} updated successfully.')
        return redirect('manage_tables')
    context = {
        'table': table,
    }
    return render(request, 'admin/edit_table.html', context)

def delete_table(request, table_id):
    table = RestaurantTable.objects.get(id=table_id)
    table.delete()
    messages.success(request, f'Table {table.table_number} deleted successfully.')
    return redirect('manage_tables')


def table_detail(request, table_number):
    request.session['table_number'] = table_number
    table = RestaurantTable.objects.get(table_number=table_number)
    menu_items = MenuItem.objects.filter(is_available=True)
    offers = Offer.objects.all()
    context = {
        'table': table,
        'menu_items': menu_items,
        'offers':offers,
    }
    return render(request, 'Customers/table_details.html', context)


def manage_chefs(request):
    chefs = LoginTable.objects.filter(role='kitchen_staff')
    return render(request, 'admin/admin_view_chefs.html', {'chefs': chefs})

def admin_add_new_chef(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['confirm_password']
        
        if  LoginTable.objects.filter(username=username).exists():
            return redirect('/admin_home')
        
        chef_details = LoginTable.objects.create(
            username=username,
            password=password,
            role='kitchen_staff'
        )
        chef_details.save()
        return HttpResponse('''<script>alert("Added New Kitchen Staff"); window.location = "/manage_chefs";</script>''')
    return render(request, 'admin/admin_add_new_chef.html')

def manage_delivery_staffs(request):
    staffs = DeliveryStaff.objects.all()
    return render(request, 'admin/manage_delivery_staff.html',{'staffs':staffs})

def admin_add_new_delivery_staff(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        gender = request.POST['gender']
        dob = request.POST['dob']
        photo = request.FILES['image']
        
        if LoginTable.objects.filter(username=username).exists():
            return HttpResponse(''' 
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'error',
                            title: 'Username Already Exists',
                            text: 'Please try with another username',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.history.back();  
                            }
                        });
                    });
                </script>
            ''')
        
        login_details = LoginTable.objects.create(
            username=username,
            password=password,
            role='delivery_staff'
        )
        
        DeliveryStaff.objects.create(
            LOGIN_ID=login_details,
            name=name,
            phone=phone,
            email=email,
            gender=gender,
            date_of_birth=dob,
            photo=photo
        )
        return redirect('/manage_delivery_staffs')
    return render(request, 'admin/add_new_staff.html')



def edit_delivery_staff(request, id):
    staff = get_object_or_404(DeliveryStaff, id=id)

    if request.method == 'POST':
        staff.name = request.POST['name']
        staff.phone = request.POST['phone']
        staff.email = request.POST['email']
        staff.gender = request.POST['gender']
        staff.date_of_birth = request.POST['dob']

        if 'image' in request.FILES:
            staff.photo = request.FILES['image']

        staff.save()
        return redirect('manage_delivery_staffs')  

    return render(request, 'admin/edit_delivery_staff.html', {'staff': staff})

# def table_view(request, table_number):
#     table = RestaurantTable.objects.get(table_number=table_number)
#     context = {
#         'table': table,
#         'menu_items': MenuItem.objects.filter(is_available=True),
#     }
#     return render(request, 'table_menu.html', context)

def manage_menu_items(request):
    menu_items = MenuItem.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin/admin_manage_menu.html', {
        'menu_items': menu_items,
        'categories': categories
    })

def add_menu_item(request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_available = 'is_available' in request.POST
        image = request.FILES['image']
        
        MenuItem.objects.create(
            CATEGORY_ID=category,
            name=name,
            description=description,
            price=price,
            is_available=is_available,
            image=image
        )
        return redirect('manage_menu_items')

def edit_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    if request.method == "POST":
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        menu_item.name = request.POST.get('name')
        menu_item.description = request.POST.get('description')
        menu_item.price = request.POST.get('price')
        menu_item.is_available = 'is_available' in request.POST
        menu_item.image = request.FILES.get('image', menu_item.image)  # Keep the current image if no new one is uploaded
        menu_item.save()
        return redirect('manage_menu_items')

    return render(request, 'admin/admin_edit_menu.html', {
        'menu_item': menu_item,
        'categories': Category.objects.all()
    })

def delete_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    menu_item.delete()
    return redirect('manage_menu_items')

def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        Category.objects.create(category_name=category_name)
        return redirect('manage_menu_items')
    
def add_offer(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item')
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        offer_title = request.POST.get('offer_title')
        discount_percentage = Decimal(request.POST.get('discount_percentage'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Calculate the discounted price
        discounted_price = menu_item.price - (menu_item.price * discount_percentage / 100)

        offer = Offer(
            menu_item=menu_item,
            offer_title=offer_title,
            discount_percentage=discount_percentage,
            price=discounted_price,  # Store the discounted price
            start_date=start_date,
            end_date=end_date
        )
        offer.save()
        return redirect('manage_offers')

    menu_items = MenuItem.objects.all()
    return render(request, 'admin/add_offer.html', {'menu_items': menu_items})

def manage_offers(request):
    offers = Offer.objects.all()
    return render(request, 'admin/manage_offers.html', {'offers': offers})

def edit_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    
    if request.method == 'POST':
        offer.discount_percentage = request.POST.get('discount_percentage')
        offer.offer_start = request.POST.get('offer_start')
        offer.offer_end = request.POST.get('offer_end')
        offer.save()
        return redirect('manage_offers')

    products = MenuItem.objects.all()
    return render(request, 'admin/edit_offer.html', {'offer': offer, 'products': products})


def delete_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.delete()
    return redirect('manage_offers')


def set_table_number(request, table_number):
    table = get_object_or_404(RestaurantTable, table_number=table_number)

    # Set the table number in the session
    request.session['table_number'] = table_number

    # Redirect to the menu or another page where the user can add items to the cart
    return render(request, 'Customers/menu.html', {'table_number': table_number})

def add_to_cart(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            menu_item_id = data.get('menu_item_id')
            table_number = data.get('table_number')
          

            # Fetch the menu item and the table
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            table = get_object_or_404(RestaurantTable, table_number=table_number)

            # Check if the table already has an active order (status 'Cart')
            order, created = Order.objects.get_or_create(TABLE=table, status='Cart')

            # Check if the menu item is already in the order (cart)
            order_item, item_created = OrderItem.objects.get_or_create(
                ORDER_ID=order,
                MENU_ID=menu_item,
                defaults={'quantity': 1, 'price': menu_item.price}
            )

            if not item_created:
                # If the item is already in the cart, increase its quantity
                order_item.quantity += 1
                order_item.save()

            # Return the updated cart item count
            cart_item_count = OrderItem.objects.filter(ORDER_ID=order).count()

            return JsonResponse({'success': True, 'cart_item_count': cart_item_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_cart_items(request):
    # Retrieve the table number from the session (assumes it's set after scanning the QR code)
    table_number = request.session.get('table_number')

    if not table_number:
        return render(request, 'Customers/view_cart.html', {
            'cart_items': [],
            'total': Decimal('0.00')
        })

    # Fetch the active cart order for the table
    order = Order.objects.filter(TABLE__table_number=table_number, status='Cart').first()

    if not order:
        return render(request, 'Customers/view_cart.html', {
            'cart_items': [],
            'total': Decimal('0.00')
        })

    # Fetch all cart items related to this order
    cart_items = OrderItem.objects.filter(ORDER_ID=order)

    # Calculate total for each item and the overall total
    total_amount = Decimal('0.00')
    for item in cart_items:
        item.total_price = item.quantity * item.price  # Calculate total price for each item
        total_amount += item.total_price  # Sum up the total amount
    order.amount = total_amount
    order.save()

    # Render the cart view with cart items and total amount
    return render(request, 'Customers/view_cart.html', {
        'cart_items': cart_items,
        'total': total_amount
    })
    

def remove_item(request, id):
    # Retrieve the order item by its primary key (id)
    item = get_object_or_404(OrderItem, id=id)
    
    # Delete the item
    item.delete()

    # Redirect to the cart page
    return redirect('/cart')

@csrf_exempt
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')

        try:
            order_item = OrderItem.objects.get(id=item_id)
            
            if action == 'increase':
                order_item.quantity += 1
            elif action == 'decrease' and order_item.quantity > 1:
                order_item.quantity -= 1

            order_item.total_price = order_item.quantity * order_item.MENU_ID.price
            order_item.save()

            # Recalculate the cart total
            table_number = request.session.get('table_number')
            order = Order.objects.filter(TABLE__table_number=table_number, status='Cart').first()
            cart_items = OrderItem.objects.filter(ORDER_ID=order)
            cart_total = sum(item.quantity * item.MENU_ID.price for item in cart_items)

            return JsonResponse({
                'success': True,
                'quantity': order_item.quantity,
                'total_price': order_item.total_price,
                'cart_total': cart_total,
            })
        except OrderItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def buy_now(request, item_id, table_number):
    if request.method == 'POST':
        # Get the menu item and table
        menu_item = get_object_or_404(MenuItem, id=item_id)
        table = get_object_or_404(RestaurantTable, table_number=table_number)

        total_amount = Decimal(str(menu_item.price)) * Decimal('1')  # For quantity 1
        # Create the order
        order = Order.objects.create(TABLE=table, status='Ordered',amount=total_amount )

        # Create the order item
        order_item = OrderItem.objects.create(
            ORDER_ID=order,
            MENU_ID=menu_item,
            quantity=1,  # Assuming 1 for Buy Now
            price=total_amount,
            status='Ordered',  
            
        )

        return redirect('order_status', table_number=table.table_number)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def order_status(request, table_number):
    table = get_object_or_404(RestaurantTable, table_number=table_number)
    orders = Order.objects.filter(Q(status='Ordered') | Q(status='accepted') | Q(status='Assigned') | Q(status='delivered'), TABLE=table)

    order_items_list = []
    for order in orders:
        items = OrderItem.objects.filter(ORDER_ID=order)
        order_items_list.append((order, items))
    context = {
        'table': table,
        'order_items_list': order_items_list,
    }
    for order in orders:
        print(f"Order ID: {order.id}, Amount: {order.amount}")  
    return render(request, 'Customers/order_status.html', context)






def checkout_view(request):
    if request.method == 'POST':
        table_number = request.session.get('table_number')
        orders = Order.objects.filter(TABLE__table_number=table_number, is_active=True)
        
        if not orders.exists():
            messages.error(request, 'No active orders found for this table.')
            return redirect('cart')

        for order in orders:
            # Calculate total price for the order
            order_items = OrderItem.objects.filter(ORDER_ID=order)
            
            # Calculate total using aggregation
            total = order_items.aggregate(
                total_amount=Sum(F('quantity') * F('price'))
            )['total_amount'] or Decimal('0.00')
            
            # Update order items and store individual item totals
            for item in order_items:
                item.status = 'Ordered'
                item.total_price = item.quantity * item.price
                item.save()
            
            # Update order status and total amount
            order.status = 'Ordered'
            order.amount = total
            order.save()
            
            # Debug print to verify
            print(f"Order ID: {order.id}")
            print(f"Total Amount: {total}")
            print("Items:")
            print(request.sesion['table_number'])
            for item in order_items:
                print(f"- {item.MENU_ID}: {item.quantity} x {item.price} = {item.total_price}")
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_status', table_number=table_number)
    else:
        return render(request, 'checkout.html')

def order_page(request, table_number):
    table = RestaurantTable.objects.get(table_number=table_number)
    menu_items = MenuItem.objects.filter(is_available=True)
    return render(request, 'Customers/order_page.html', {'table': table, 'menu_items': menu_items})




def user_pay_proceed(request,id,amt):
    table_number = request.session.get('table_number')
    request.session['rid'] = id
    request.session['pay_amount'] = amt
    amount_in_paisa = int(float(amt) * 100)
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client,table_number)
    payment = client.order.create({'amount': amount_in_paisa, 'currency': "INR", 'payment_capture': '1'})
    return render(request,'Customers/UserPayProceed.html',{'p':payment,'val':[],"lid":table_number,"id":request.session['rid']})

def on_payment_success(request):
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    tbl = request.session['lid']
    print(tbl)
    
    ob = Order.objects.get(id=request.session['rid'])
    ob.status = 'Paid'
    ob.save()
    print(tbl)
    return HttpResponse(f'<script>window.location.href = "/table/{tbl}/";</script>')


def ratings(request, table_number):
    # Retrieve the specific table
    table = get_object_or_404(RestaurantTable, table_number=table_number)

    # Fetch orders with status 'Paid' for the specified table
    paid_orders = Order.objects.filter(TABLE=table, status='Paid')

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        ratings = request.POST.get('rating')
        order_id = request.POST.get('order_id')
        
        # Retrieve the order and update feedback if available
        order = Order.objects.get(id=order_id)
        if feedback_text:
            Feedback.objects.create(ORDER=order, TABLE=table, feedback=feedback_text,ratings=ratings)
        
        # Update the order status to 'Rated'
        order.status = 'Rated'
        order.save()
        
        # Redirect to refresh the page after submission
        return redirect('ratings', table_number=table_number)
    
    # Render the page with paid orders for rating
    return render(request, 'Customers/ratings.html', {'paid_orders': paid_orders, 'table_number': table_number})









def kitchen_home(request):
    pending_orders = Order.objects.filter(Q(status='Ordered') | Q(status='accepted'), is_active=True).order_by('-id')
    delivery_staff = DeliveryStaff.objects.all()  # Fetch all delivery staff

    context = {
        'pending_orders': pending_orders,
        'delivery_staff': delivery_staff,  # Pass the delivery staff to the template
    }
    return render(request, 'Kitchen_Staff/orders.html', context)

def accept_order(request, id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=id)
        order.status = 'accepted'
        order.save()  
        return redirect('/kitchen_home')
    return redirect('/kitchen_home')

def assign_order(request, id):
    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        staff = get_object_or_404(DeliveryStaff, id=staff_id)
        order = get_object_or_404(Order, id=id)
        assign = Assign(STAFF=staff, ORDER=order, status='assigned')
        assign.save()
        order.status = 'Assigned'
        order.save()
        return redirect('/kitchen_home')
    return redirect('/kitchen_home')

def staff_manage_products(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(MenuItem, id=product_id)

        product.is_available = not product.is_available
        product.save()

        return redirect('staff_manage_products')

    context = {
        'menu_items': menu_items,
    }
    return render(request, 'Kitchen_Staff/staff_manage_products.html', context)


def delivery_home(request):
    assigned_orders = Assign.objects.filter(status='assigned')

    if request.method == 'POST':
        assign_id = request.POST.get('assign_id')
        assign = get_object_or_404(Assign, id=assign_id)
        
        assign.status = 'delivered'
        assign.ORDER.status = 'delivered'
        assign.ORDER.save()  # Save the Order status change
        assign.save()  # Save the Assign status change
        return redirect('delivery_home')
    return render(request, 'Delivery_Staff/staff_home.html', {'assigned_orders': assigned_orders})




def view_reviews(request):
    return render(request, 'admin/view_reviews.html')

def view_bills_payments(request):
    # Get all paid orders
    bills = Order.objects.filter(status='Rated').prefetch_related('payment_set')  
    return render(request, 'admin/view_bills.html', {'bills': bills})



def view_reports(request):
    return render(request, 'admin/view_reports.html')

def view_ratings_reviews(request):
    feeds = Feedback.objects.all().order_by('-id')
    return render(request, 'admin/view_ratings_reviews.html', {'feeds': feeds})



from django.db.models import Sum
from datetime import datetime

def view_order_reports(request):
    # Get all menu items for the search dropdown
    menu_items = MenuItem.objects.all()

    # Initialize the query parameters
    product_name = request.GET.get('product_name', '')
    order_date = request.GET.get('order_date', '')

    # Filter the orders based on the search criteria
    order_items = OrderItem.objects.all()

    if product_name:
        order_items = order_items.filter(MENU_ID__name__icontains=product_name)

    if order_date:
        try:
            order_date = datetime.strptime(order_date, '%Y-%m-%d')
            order_items = order_items.filter(ORDER_ID__order_time=order_date)
        except ValueError:
            pass  # Handle incorrect date format

    # Aggregate sales by menu item
    sales_data = order_items.values('MENU_ID__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')

    # Prepare data for the chart
    labels = [item['MENU_ID__name'] for item in sales_data]
    sales = [item['total_sales'] for item in sales_data]

    context = {
        'labels': labels,
        'sales': sales,
        'menu_items': menu_items,
    }

    return render(request, 'admin/view_order_reports.html', context)


def logout_view(request):
    # Implement logout logic here
    return render(request, 'logout.html')

