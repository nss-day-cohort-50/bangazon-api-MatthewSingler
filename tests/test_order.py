from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product, PaymentType


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        product = Product.objects.get(pk=1)

        self.order1 = Order.objects.create(
            user=self.user1
        )
        #need to create a payment for the order. This is all made up and from scratch. This info comes from the payment type model. By adding self. in front of payment type we can use it as a variable in all tests.
        self.payment_type = PaymentType.objects.create(
            merchant_name = "My merchant",
            acct_number = "123321",
            customer = self.user1
        )

        self.order1.products.add(product)

        self.order2 = Order.objects.create(
            user=self.user2
        )

        self.order2.products.add(product)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_delete_order(self):
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # TODO: Complete Order test

    def test_order_payment(self): #This is our test to check that a payment type can be added to an order. We are updating the order with a payment type.
        url = f"/api/orders/{self.order1.id}/complete"
        #the url that the client requests info from is this. We use api in front b/c? We can use the order id from the order object we created i the setup at top.
        order = {
            "paymentTypeId": self.payment_type.id
        }  # the only thing we are interested in is the payment type because that is the only object using request.data in the order view. This is what the client is sending back and that's what we want to check.
        response = self.client.put(url, order, format='json')
        #What we want to send in the response?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #what gets returned?
        order = Order.objects.get(pk=self.order1.id)
        #We make a new order variable because it is being updated. It will not have the payment type we created on line 57. So we get the Order from the orm that has a PK of self.order1.id?
        self.assertEqual(order.payment_type.id, self.payment_type.id)
        #We check to see that the order.payment_type.id is the same as the self.payment_type.id we created on line 57.
