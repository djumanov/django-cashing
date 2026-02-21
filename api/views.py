from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product


@method_decorator(cache_page(60), name="dispatch")
class ProductListView(APIView):

    def get(self, request):
        data = Product.objects.all().values()
        return Response(data)
    

class ProductDetailView(APIView):
    
    def get(self, request, pk):
        cache_key = f"product:{pk}"

        data = cache.get(cache_key)
        if not data:
            try:
                product = Product.objects.get(pk=pk)
                data = {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price
                }
                cache.set(cache_key, data, timeout=60)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=404)
        return Response(data)
