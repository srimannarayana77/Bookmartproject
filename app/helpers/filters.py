from django.db.models import Q

def user_filters(users, params):
    try:
        filters = Q()
        first_name = params.get('first_name')
        last_name = params.get('last_name')
        email = params.get('email')
        user_type = params.get('user_type')

        if first_name:
            filters &= Q(first_name__icontains=first_name)

        if last_name:
            filters &= Q(last_name__icontains=last_name)

        if email:
            filters &= Q(email__icontains=email)

        if user_type:
            filters &= Q(user_type=user_type)

        return users.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e

def publisher_filters(publishers, params):
    try:
        filters = Q()
        user_first_name = params.get('user_first_name')
        user_last_name = params.get('user_last_name')
        user_email = params.get('user_email')
        user_type = params.get('user_type')
        company_name = params.get('company_name')
        address_keyword = params.get('address_keyword')

        if user_first_name:
            filters &= Q(user__first_name__icontains=user_first_name)

        if user_last_name:
            filters &= Q(user__last_name__icontains=user_last_name)

        if user_email:
            filters &= Q(user__email__icontains=user_email)

        if user_type:
            filters &= Q(user__user_type=user_type)

        if company_name:
            filters &= Q(company__name__icontains=company_name)

        if address_keyword:
            filters &= Q(address__icontains=address_keyword)

        return publishers.filter(filters)
    
    except Exception as e:
        print("Error:", e)
        raise e


def company_filters(companies, params):
    try:
        filters = Q()
        name = params.get('name')

        if name:
            filters &= Q(name__icontains=name)

        return companies.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e

def customer_filters(customers, params):
    try:
        filters = Q()
  # Add filters for User fields
        user_first_name = params.get('user_first_name')
        user_last_name = params.get('user_last_name')
        user_email = params.get('user_email')
        
        user_filters = Q()

        if user_first_name:
            user_filters &= Q(user__first_name__icontains=user_first_name)

        if user_last_name:
            user_filters &= Q(user__last_name__icontains=user_last_name)

        if user_email:
            user_filters &= Q(user__email__icontains=user_email)

        filters &= user_filters

        return customers.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e


def book_filters(books, params):
    try:
        filters = Q()
        title = params.get('title')
        ISBN = params.get('ISBN')
        genre = params.get('genre')
        price = params.get('price')
        quantity_in_stock = params.get('quantity_in_stock')
        publisher_id = params.get('publisher_id')

        if title:
            filters &= Q(title__icontains=title)

        if ISBN:
            filters &= Q(ISBN__icontains=ISBN)

        if genre:
            filters &= Q(genre__icontains=genre)

        if price:
            filters &= Q(price=price)

        if quantity_in_stock:
            filters &= Q(quantity_in_stock=quantity_in_stock)

        if publisher_id:
            filters &= Q(publisher_id=publisher_id)

        return books.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e

    

def cart_filters(carts, params):
    try:
        filters = Q()
        customer_id = params.get('customer_id')
        book_id = params.get('book_id')
        location = params.get('location')

        if customer_id:
            filters &= Q(customer__id=customer_id)

        if book_id:
            filters &= Q(books__id=book_id)

        if location:
            filters &= Q(location__icontains=location)

        return carts.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e

def order_filters(orders, params):
    try:
        filters = Q()
        customer_id = params.get('customer_id')
        cart_id = params.get('cart_id')
        total_price = params.get('total_price')
        payment_status = params.get('payment_status')

        if customer_id:
            filters &= Q(customer__id=customer_id)

        if cart_id:
            filters &= Q(cart__id=cart_id)

        if total_price:
            filters &= Q(total_price=total_price)

        if payment_status is not None:
            filters &= Q(payment_status=payment_status)

        return orders.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e

def payment_filters(payments, params):
    try:
        filters = Q()
        order_id = params.get('order_id')
        payment_method = params.get('payment_method')
        amount = params.get('amount')

        if order_id:
            filters &= Q(order__id=order_id)

        if payment_method:
            filters &= Q(payment_method__icontains=payment_method)

        if amount:
            filters &= Q(amount=amount)

        return payments.filter(filters)

    except Exception as e:
        print("Error:", e)
        raise e