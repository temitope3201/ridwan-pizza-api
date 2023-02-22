import unittest
from .. import create_app
from ..utils import db
from ..config.config import config_dict
from flask_jwt_extended import create_access_token
from ..models.orders import Order, Sizes

class OrderTestCase(unittest.TestCase):

    def setUp(self):
        
        self.app = create_app(config = config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    
    def tearDown(self):
        db.drop_all()

        self.app = None

        self.client = None

        self.appctx.pop()

    def test_get_all_orders(self):

        token = create_access_token(identity='testuser')
        headers = {"Authorization": f"Bearer {token}"}


        
        response = self.client.get('/orders/orders', headers = headers)

        assert response.status_code == 200
        assert response.json == []

    
    
    def test_create_order(self):
        token = create_access_token(identity='testuser')
        headers = {"Authorization": f"Bearer {token}"}

        data ={
            "size": "SMALL",
            "quantity": 1,
            "flavour": "SUYA"
        }

        response = self.client.post('orders/orders',json = data, headers = headers)
        assert response.status_code == 201

        orders = Order.query.all()

        assert len(orders) == 1

        assert orders[0].size == Sizes.SMALL
        assert response.json['size'] == "Sizes.SMALL"
        assert response.json['flavour'] == "Flavour.SUYA"

        # response2 = self.client.get('orders.order/1', headers = headers)

        # assert response2.status_code == 201

    
    def test_get_specific_order(self):

        order = Order(
            quantity =1,
            size = "SMALL",
            flavour = "SUYA"
        )

        order.save()

        token = create_access_token(identity='testuser')
        headers = {"Authorization": f"Bearer {token}"}        

        response = self.client.get('orders/order/1', headers = headers)

        # orders = Order.query.get_or_404(1)


        # assert len[orders] == 1
        assert response.status_code == 200
        

