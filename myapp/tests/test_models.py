from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):

    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(
            name='Temporary product',
            price=1.99,
            available=True
        )
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                price=1.99,
                available=True
            )
            temp_product.full_clean()

    def test_create_product_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                name='',
                price=1.99,
                available=True
            )
            temp_product.full_clean()

    def test_create_product_with_short_name(self):
        temp_product = Product.objects.create(
            name='A',
            price=1.99,
            available=True
        )
        self.assertEqual(temp_product.name, 'A')

    def test_create_product_with_max_name_length(self):
        max_length_name = 'A' * 255
        temp_product = Product.objects.create(
            name=max_length_name,
            price=1.99,
            available=True
        )
        self.assertEqual(temp_product.name, max_length_name)

    def test_create_product_with_exceeding_name_length(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                name='A' * 256,
                price=1.99,
                available=True
            )
            temp_product.full_clean()

    def test_create_product_with_zero_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                name='Free product',
                price=0.0,
                available=True
            )
            temp_product.full_clean()

    def test_create_product_with_high_price(self):
        temp_product = Product.objects.create(
            name='Expensive product',
            price=99999.99,
            available=True
        )
        self.assertEqual(temp_product.price, 99999.99)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                name='Invalid price product',
                price=-1.99,
                available=True
            )
            temp_product.full_clean()

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                name='Invalid price format',
                price=1.999,
                available=True
            )
            temp_product.full_clean()



class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(
            name='John Doe',
            address='123 Main St'
        )
        self.assertEqual(temp_customer.name, 'John Doe')
        self.assertEqual(temp_customer.address, '123 Main St')

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(
                name='John Doe',
                address=''
            )
            temp_customer.full_clean()

    def test_create_customer_with_short_name(self):
        temp_customer = Customer.objects.create(
            name='A',
            address='123 Main St'
        )
        self.assertEqual(temp_customer.name, 'A')

    def test_create_customer_with_max_name_length(self):
        max_length_name = 'A' * 100
        temp_customer = Customer.objects.create(
            name=max_length_name,
            address='123 Main St'
        )
        self.assertEqual(temp_customer.name, max_length_name)

    def test_create_customer_with_exceeding_name_length(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(
                name='A' * 101,
                address='123 Main St'
            )
            temp_customer.full_clean()



class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name="John Doe",
            address="123 Main St"
        )

        self.product1 = Product.objects.create(
            name="Product 1",
            price=10.00,
            available=True
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            price=20.00,
            available=False
        )

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(
            customer=self.customer,
            status="New"
        )
        order.products.add(self.product1)
        self.assertEqual(order.customer.name, "John Doe")
        self.assertEqual(order.status, "New")
        self.assertEqual(order.products.count(), 1)

    def test_create_order_with_invalid_status(self):
        order = Order(
            customer=self.customer,
            status="Invalid Status"
        )
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_calculate_total_price_with_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status="New"
        )
        order.products.add(self.product1, self.product2)
        total_price = order.calculate_total_price()
        self.assertEqual(total_price, 30.00)

    def test_calculate_total_price_with_no_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status="New"
        )
        total_price = order.calculate_total_price()
        self.assertEqual(total_price, 0.00)

    def test_check_order_fulfillment_with_available_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status="New"
        )
        order.products.add(self.product1)
        is_fulfilled = order.check_order_fulfillment()
        self.assertTrue(is_fulfilled)

    def test_check_order_fulfillment_with_unavailable_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status="New"
        )
        order.products.add(self.product2)
        is_fulfilled = order.check_order_fulfillment()
        self.assertFalse(is_fulfilled)
