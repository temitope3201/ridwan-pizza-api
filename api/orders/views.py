from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db


order_namespace = Namespace('orders', description='namespace for orders')

order_model = order_namespace.model(
    'Order',{
        'id': fields.Integer(description = 'id of the order'),
        'quantity': fields.Integer(description= 'quantity of order', required = True),
        'size': fields.String(description = 'size of order', required = True, enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'] ),
        'order_status': fields.String(description = 'status of our order', enum =['PENDING', 'IN_TRANSIT, DELIVERED']),
        'flavour': fields.String(description = 'flavour of our pizza', required = True, 
                                enum = ['BARBECUE_CHIKEN', 'BARBECUE_BEEF', 'MAGHERITTA', 'PEPPERONI', 'SUYA', 'MARGHERITTA'])
    }
)
order_status_model = order_namespace.model(
    'Order',{
        'order_status': fields.String(description = 'status of our order', enum =['PENDING', 'IN_TRANSIT, DELIVERED'])
    }
)



@order_namespace.route('/orders')
class OrdersGetCreate(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "Get All Orders")
    @jwt_required()
    def get(self):

        """
            get all orders
        """

        orders = Order.query.all()

        
        return orders, HTTPStatus.OK


    @jwt_required()
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "create an order")
    def post(post):

        """
            create an order
        """
        data = request.get_json()

        username = get_jwt_identity()

        current_user = User.query.filter_by(username = username).first()

        new_order = Order(
            quantity = data['quantity'],
            size = data['size'],
            flavour = data['flavour'],
            customer = current_user  
        )

        # new_order.user = current_user

        db.session.add(new_order)
        db.session.commit()

        return new_order, HTTPStatus.CREATED

@order_namespace.route('/order/<int:order_id>')
class GetUpdateDeleteOrder(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Retrieve an Order by Id",
        params = {"order_id": " The unique id of a specific user"}
        )
    @jwt_required()
    def get(self, order_id):
        """
            Retrieve an Order by Id
        """
        order = Order.get_by_id(order_id)

        return order, HTTPStatus.OK


    @jwt_required()
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Update an Order by Id", 
        params = {"order_id": " The unique id of a specific order"})
    def put(self, order_id):
        """
            Update an Order by Id
        """

        order_to_update = Order.get_by_id(order_id)

        data = order_namespace.payload

        order_to_update.quantity = data['quantity']
        order_to_update.size = data['size']
        order_to_update.flavour = data['flavour']

        db.session.commit()

        return order_to_update, HTTPStatus.OK


    @jwt_required()
    @order_namespace.doc(
        description = "Delete an Order by Id",
        params = {"order_id": " The unique id of a specific order"})
    def delete(self, order_id):
        """
            Delete an Order by Id
        """

        order_to_delete = Order.get_by_id(order_id)
        
        db.session.delete(order_to_delete)
        db.session.commit()

        return {"message": "Deleted Successfully"}, HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetUserOrder(Resource):

    @jwt_required()
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Retrieve a User's Order by Id",
        params = {
            "order_id": " The unique id of a specific order",
            "user_id": " The unique id of a specific User"})
    def get(self, user_id, order_id):
        """
            Retrieve a User's Order by Id
        """
        user = User.get_by_id(user_id)

        orders = user.orders

        order = orders[order_id]

        return order, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/orders')
class AllUserOrders(Resource):

    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    @order_namespace.doc(
        description = "Retrieve all orders for a user",
        params = {"user_id": " The unique id of a specific user"})
    def get(self, user_id):
        """
            Retrieve all orders for a user
        """
        user = User.get_by_id(user_id)

        orders = user.orders

        return orders, HTTPStatus.OK

@order_namespace.route('/orders/status/<int:order_id>')
class UpdateOrderStatus(Resource):

    @jwt_required()
    @order_namespace.marshal_with(order_model)
    @order_namespace.expect(order_status_model)
    @order_namespace.doc(
        description = "Update the status of an order",
        params = {"order_id": " The unique id of a specific order"})
    def patch(self, order_id):
        """
            Update the status of an order
        """ 

        order_to_update = Order.get_by_id(order_id)

        data = order_namespace.payload

        order_to_update.order_status = data["order_status"]

        db.session.commit()

        return order_to_update, HTTPStatus.OK
    