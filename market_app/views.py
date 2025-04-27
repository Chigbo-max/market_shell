from urllib import request

from django.shortcuts import render

from rest_framework.decorators import api_view

from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, DetailedProductSerializer, CartItemsSerializer, SimpleCartSerializer, \
    CartSerializer
from rest_framework.response import Response

import logging
logger = logging.getLogger(__name__)


@api_view(['GET'])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)



@api_view(['POST'])
def add_item(request):
    try:
        cart_code = request.data.get('cart_code')
        print(cart_code)
        product_id = request.data.get('product_id')
        print(product_id)


        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

        if not created:
            cartItem.quantity += 1
            cartItem.save()

        serializer = CartItemsSerializer(cartItem)
        return Response({"data": serializer.data, "message": "Cart item created successful"}, 200)

    except Cart.DoesNotExist:
        return Response({"error": "Cart does not exist"}, 404)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, 404)
    except Product.MultipleObjectsReturned:
        return Response({"error": "Product already exists"}, 404)
    except Exception as e:
        return Response({"error": str(e)}, 500)


@api_view(['GET'])
def product_in_cart(request):
    try:
        cart_code = request.query_params.get('cart_code')
        product_id = request.query_params.get('product_id')

        cart = Cart.objects.get(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
        return Response({"product_exists_in_cart": product_exists_in_cart}, 200)

    except (Cart.DoesNotExist, Product.DoesNotExist):
        return Response({"product_exists_in_cart": False}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, 500)

@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get('cart_code')
    try:
        cart = Cart.objects.get(cart_code=cart_code, paid=False)
        serializer = SimpleCartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        logger.warning(f"Cart not found for code: {cart_code}")
        return Response({"number of items": 0}, 200)

    except Exception as e:
        return Response({"error": str(e)}, 500)


@api_view(['GET'])
def get_cart(request):
    cart_code = request.query_params.get('cart_code')
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity'))
        cart_item = CartItem.objects.get(id=cartitem_id)
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response({"data":serializer.data, "message": "Cart item updated successful"}, 200)
    except Exception as e:
        return Response({"error": str(e)}, 500)
