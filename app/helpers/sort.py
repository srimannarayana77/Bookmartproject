def sort_users(sortBY,sortType,users):
    if sortType.lower() == 'desc':
        users = users.order_by(f'-{sortBY}')
    else:
       users = users.order_by(sortBY)

    return users

def sort_publishers(sortBY,sortType,publishers):
    if sortType.lower() == 'desc':
        publishers = publishers.order_by(f'-{sortBY}')
    else:
       publishers = publishers.order_by(sortBY)

    return publishers

def sort_companies(sortBY,sortType,companies):
    if sortType.lower() == 'desc':
        companies = companies.order_by(f'-{sortBY}')
    else:
       companies = companies.order_by(sortBY)

    return companies

def sort_customers(sortBY,sortType,customers):
    if sortType.lower() == 'desc':
        customers = customers.order_by(f'-{sortBY}')
    else:
       customers = customers.order_by(sortBY)

    return customers

def sort_books(sortBY,sortType,books):
    if sortType.lower() == 'desc':
        books = books.order_by(f'-{sortBY}')
    else:
       books= books.order_by(sortBY)

    return books

def sort_carts(sortBY,sortType,carts):
    if sortType.lower() == 'desc':
        carts = carts.order_by(f'-{sortBY}')
    else:
       carts= carts.order_by(sortBY)

    return carts
def sort_orders(sortBY,sortType,orders):
    if sortType.lower() == 'desc':
        orders = orders.order_by(f'-{sortBY}')
    else:
       orders= orders.order_by(sortBY)

    return orders
def sort_payments(sortBY,sortType,payments):
    if sortType.lower() == 'desc':
        payments = payments.order_by(f'-{sortBY}')
    else:
       payments= payments.order_by(sortBY)

    return payments