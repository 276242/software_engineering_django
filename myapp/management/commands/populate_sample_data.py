from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        # products
        product1 = Product.objects.create(
            name='Racing Gloves',
            price=19.99,
            available=True
        )
        product2 = Product.objects.create(
            name='Racing Suit',
            price=199.99,
            available=True
        )
        product3 = Product.objects.create(
            name='Helmet',
            price=59.99,
            available=False
        )

        # customers
        customer1 = Customer.objects.create(
            name='Lando Norris',
            address='McLaren Technology Centre'
        )
        customer2 = Customer.objects.create(
            name='Carlos Sainz',
            address='Ferrari S.p.A. Via Abetone Inferiore n. 4'
        )
        customer3 = Customer.objects.create(
            name='Lewis Hamilton',
            address='Mercedes AMG Petronas F1 Operations Centre'
        )

        # orders
        order1 = Order.objects.create(
            customer=customer1,
            status='New'
        )
        order1.products.add(product1)

        order2 = Order.objects.create(
            customer=customer2,
            status='In Process'
        )
        order2.products.add(product2)

        order3 = Order.objects.create(
            customer=customer1,
            status='Completed'
        )
        order3.products.add(product1, product3)

        self.stdout.write("Data created successfully.")