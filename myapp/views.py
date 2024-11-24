from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
import json
from django.core.exceptions import ValidationError

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
        

        missing_fields = []
        if 'name' not in data:
            missing_fields.append('\'name\'')
        if 'price' not in data:
            missing_fields.append('\'price\'')
        if 'available' not in data:
            missing_fields.append('\'available\'')

        if missing_fields:
            return HttpResponseBadRequest(f"Missing required fields: {', '.join(missing_fields)}.")

        try:
            price = Decimal(str(data.get('price')))
        except (ValueError, Decimal.InvalidOperation):
            return HttpResponseBadRequest("Invalid value for 'price'. Price must be a valid decimal number.")

        name = data.get('name')
        available = data.get('available')
        product = Product(name=name, price=price, available=available)

        try:
            product.full_clean()
            product.save()
        except ValidationError as e:
            error_messages = []
            for field, messages in e.message_dict.items():
                if field == '__all__':
                    error_messages.extend(messages)
                else:
                    error_messages.extend(f"{field}: {message}" for message in messages)
            return HttpResponseBadRequest(f"Invalid data: {', '.join(error_messages)}")

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        }, status=201)

    else:
        return HttpResponseBadRequest("Invalid HTTP method. Only GET and POST are allowed.")

@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound(f"Product with ID {product_id} not found.")

    if request.method == 'GET':
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        })

    return HttpResponseBadRequest("Invalid HTTP method. Only GET is allowed.")