from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # to serialize image for emtire url(max_length important)
    image = serializers.ImageField(max_length=None, allow_empty_file=False, required=False)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'category')
