from urllib import request

from django.shortcuts import render

from rest_framework.decorators import api_view

from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, DetailedProductSerializer, CartItemsSerializer
from rest_framework.response import Response


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
        product_id = request.data.get('product_id')

        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)

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

    except Exception as e:
        return Response({"error": str(e)}, 500)