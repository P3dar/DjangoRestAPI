from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from rest_framework.permissions import BasePermission
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum

# check if the user is a Manager


class IsManager(BasePermission):
    def has_permission(self, request):
        return request.user.groups.filter(name='Manager').exists()


# check if the user is part of the delivery crew

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request):
        return request.user.groups.filter(name='Delivery Crew').exists()

# can view or add managers, to use this endpoint you must be a manager


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def managers(request):
    if IsManager().has_permission(request):
        if request.method == 'GET':
            managers_group = Group.objects.get(name='Manager')
            users = managers_group.user_set.all()
            serialized_users = UserSerializer(users, many=True)
            return Response(serialized_users.data)
        elif request.method == 'POST':
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username)
                managers_group = Group.objects.get(name='Manager')
                managers_group.user_set.add(user)
                return Response({'message': 'user added to manager group'}, status.HTTP_201_CREATED)
            else:
                return Response({'message': 'username is required'}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)


# can delete a manager, to use this you must be a manager

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delManagers(request, pk):
    if IsManager().has_permission(request):
        if request.method == 'DELETE':
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username, pk=pk)
                managers_group = Group.objects.get(name='Manager')
                managers_group.user_set.remove(user)
                return Response({'message': 'deleted from Manager'}, status.HTTP_200_OK)
            else:
                return Response({'message': 'username is required'}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)


# can view or add memeber to the delivery crew group, to use this endpoint you must be a manager


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def deliverycrew(request):
    if IsManager().has_permission(request):
        if request.method == 'GET':
            delivery_group = Group.objects.get(name='Delivery Crew')
            users = delivery_group.user_set.all()
            serialized_users = UserSerializer(users, many=True)
            return Response(serialized_users.data)
        elif request.method == 'POST':
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username)
                delivery_group = Group.objects.get(name='Delivery Crew')
                delivery_group.user_set.add(user)
                return Response({'message': 'user added to Delivery Crew'}, status.HTTP_201_CREATED)
            else:
                return Response({'message': 'username is required'}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)


# delete a memebr of the delivery crew, to use this endpoint you must be a manager


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delDelivery(request, pk):
    if IsManager().has_permission(request):
        if request.method == 'DELETE':
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username, pk=pk)
                delivery_group = Group.objects.get(name='Delivery Crew')
                delivery_group.user_set.remove(user)
                return Response({'message': 'deleted from Delivery Crew'}, status.HTTP_200_OK)
            else:
                return Response({'message': 'username is required'}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)


# a manager can see and add categories

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def categories(request):
    if IsManager().has_permission(request):
        if request.method == 'GET':
            items = Category.objects.select_related()
            serialized_items = CategoySerializer(items, many=True)
            return Response(serialized_items.data, status.HTTP_200_OK)
        elif request.method == 'POST':
            serialized_items = CategoySerializer(data=request.data)
            serialized_items.is_valid(raise_exception=True)
            serialized_items.save()
            return Response({"message": "New category added"}, status.HTTP_201_CREATED)
    else:
        return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)

# a logged client can only use the get method to see all menu items, a manager can post a new item


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def menuitems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_filter = request.query_params.get('category')
        price_filter = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=5)
        page = request.query_params.get('page', default=1)
        if category_filter:
            items = items.filter(category__slug=category_filter)
        elif price_filter:
            items = items.filter(price__lte=price_filter)
        elif search:
            items = items.filter(title__contains=search)
        elif ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method == 'POST':
        if IsManager().has_permission(request):
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message": "New menuitem added"}, status.HTTP_201_CREATED)
        else:
            return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)


# a client can only use get method to see a single menu item, a manger can even modify or delete


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def SingleMenuItem(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'GET':
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data)
    elif request.method == 'PATCH':
        if IsManager().has_permission(request):
            serialized_item = MenuItemSerializer(
                item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message": "menuitem modified"}, status.HTTP_201_CREATED)
        else:
            return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if IsManager().has_permission(request):
            item.delete()
            return Response({'message': 'Item deleted from Menu items'}, status.HTTP_200_OK)
        else:
            return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)


# an authenticated user can create, view or delete different cart objects


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cart(request):
    user = request.user
    if request.method == 'GET':
        items = Cart.objects.filter(user=user)
        if items.exists():
            serialized_item = CartItemSerializer(items, many=True)
            return Response(serialized_item.data)
        else:
            return Response({'message': 'Cart is empty.'}, status.HTTP_200_OK)
    elif request.method == 'POST':
        serialized_item = CartItemSerializer(
            data=request.data, context={'user': request.user})
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save(user=user)
        return Response({'message': 'item added to Cart'}, status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        items = Cart.objects.filter(user=user)
        if items.exists():
            items.delete()
            return Response({'message': 'items deleted from Cart'}, status.HTTP_200_OK)
        else:
            return Response({'message': 'Cart is alredy empty.'}, status.HTTP_200_OK)

# An authenticated user can create an order object and see he's own orders.
# a manager can see every order
# a delivery boy can only see the orders with his id


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def Makeorder(request):
    if request.method == 'GET':
        if IsManager().has_permission(request):
            items = Order.objects.select_related('user').all()
            if items.exists():
                status_filter = request.query_params.get('status')
                date_filter = request.query_params.get('date')
                search = request.query_params.get('search')
                ordering = request.query_params.get('ordering')
                perpage = request.query_params.get('perpage', default=5)
                page = request.query_params.get('page', default=1)
                if status_filter:
                    items = items.filter(status=status_filter)
                elif date_filter:
                    items = items.filter(date=date_filter)
                elif search:
                    items = items.filter(id__contains=search)
                elif ordering:
                    ordering_fields = ordering.split(',')
                    items = items.order_by(*ordering_fields)
                paginator = Paginator(items, per_page=perpage)
                try:
                    items = paginator.page(number=page)
                except EmptyPage:
                    items = []
                serialized_item = OrderSerializer(items, many=True)
                return Response(serialized_item.data)
            else:
                return Response({'message': 'No placed Orders.'}, status.HTTP_200_OK)
        elif IsDeliveryCrew().has_permission(request):
            items = Order.objects.filter(delivery_crew=request.user)
            if items.exists():
                status_filter = request.query_params.get('status')
                date_filter = request.query_params.get('date')
                search = request.query_params.get('search')
                ordering = request.query_params.get('ordering')
                perpage = request.query_params.get('perpage', default=5)
                page = request.query_params.get('page', default=1)
                if status_filter:
                    items = items.filter(status=status_filter)
                elif date_filter:
                    items = items.filter(date=date_filter)
                elif search:
                    items = items.filter(id__contains=search)
                elif ordering:
                    ordering_fields = ordering.split(',')
                    items = items.order_by(*ordering_fields)
                paginator = Paginator(items, per_page=perpage)
                try:
                    items = paginator.page(number=page)
                except EmptyPage:
                    items = []
                serialized_item = OrderSerializer(items, many=True)
                return Response(serialized_item.data)
            else:
                return Response({'message': 'No Orders for you.'}, status.HTTP_200_OK)
        else:
            items = Order.objects.filter(
                user=request.user)
            if items.exists():
                status_filter = request.query_params.get('status')
                date_filter = request.query_params.get('date')
                search = request.query_params.get('search')
                ordering = request.query_params.get('ordering')
                perpage = request.query_params.get('perpage', default=5)
                page = request.query_params.get('page', default=1)
                if status_filter:
                    items = items.filter(status=status_filter)
                elif date_filter:
                    items = items.filter(date=date_filter)
                elif search:
                    items = items.filter(id__contains=search)
                elif ordering:
                    ordering_fields = ordering.split(',')
                    items = items.order_by(*ordering_fields)
                paginator = Paginator(items, per_page=perpage)
                try:
                    items = paginator.page(number=page)
                except EmptyPage:
                    items = []
                serialized_item = OrderSerializer(items, many=True)
                return Response(serialized_item.data)
            else:
                return Response({'message': 'No Orders for the current user.'}, status.HTTP_200_OK)
    if request.method == 'POST':
        if Cart.objects.filter(user=request.user).exists():
            orderSer = OrderSerializer(data=request.data, context={
                'user': request.user})
            orderSer.is_valid(raise_exception=True)
            ordSav = orderSer.save(user=request.user)
            order_pk = orderSer.instance.pk
            order = Order.objects.get(pk=order_pk)
            cart_items = Cart.objects.filter(user=request.user)
            order_items = []
            for cart_item in cart_items:
                cart_item = OrderItem(
                    order=order,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.menuitem.price,
                    price=cart_item.quantity * cart_item.menuitem.price)
                order_items.append(cart_item)
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()
            total = OrderItem.objects.filter(order=order_pk).aggregate(
                total=Sum('price'))['total'] or 0
            ordSav.total = total
            ordSav.save()
            return Response({'message': 'Order created successfully'}, status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Your Cart is empty'}, status.HTTP_200_OK)

# when get method is used the function return the single order with the specified id wrtitten in the url
# a customer can only see his orders, a manger or a delivery BOI instead can see every order, if it exist
# the patch method is only for managers. the delivery crew can use it but only for change the 'status' field
# the delete method is only for managers


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def singleOrder(request, pk):
    item = get_object_or_404(Order, pk=pk)
    if request.method == 'GET':
        if IsManager().has_permission(request) or IsDeliveryCrew().has_permission(request):
            serialized_item = OrderSerializer(item)
            return Response(serialized_item.data)
        else:
            if item.user == request.user:
                serialized_item = OrderSerializer(item)
                return Response(serialized_item.data)
            else:
                return Response({'message': 'Error, this order is not yours'}, status.HTTP_403_FORBIDDEN)
    elif request.method == 'PATCH':
        if IsManager().has_permission(request):
            serialized_item = SingleOrderSerializer(
                item, data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message": "Order modified"}, status.HTTP_201_CREATED)
        elif IsDeliveryCrew().has_permission(request):
            if 'status' not in request.data or len(request.data.keys()) > 1:
                return Response({'message': 'As a delivery staff member you cannnot change this field'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serialized_item = SingleOrderSerializer(
                    item, data=request.data, partial=True)
                serialized_item.is_valid(raise_exception=True)
                serialized_item.save()
                return Response({"message": "Status Order modified"}, status.HTTP_201_CREATED)
        else:
            return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if IsManager().has_permission(request):
            item.delete()
            return Response({'message': 'Order deleted'}, status.HTTP_200_OK)
        else:
            return Response({"message": "You don't have the required permissions"}, status.HTTP_403_FORBIDDEN)
# THE END
