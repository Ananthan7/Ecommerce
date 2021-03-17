from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="39c8vsvtr68wpzy2",
        public_key="dr73pdv6dpyq4vk6",
        private_key="af8dea5c05533fa39d1dd2a2114d8f4a"
    )
)

def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, please login again'})

    return JsonResponse({'clientToken': gateway.client_token.generate(), 'seccess': True})

@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid session, please login again'})

    nonce_from_the_client = request.P0ST["paymentMethodNonce"]
    amount_from_the_client = request.P0ST["amount"]

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({"success": result.is_success, "transaction": {'id': result.transaction.id, 'amount': result.transaction.amount}})
    else:
        return JsonResponse({'error': True, 'success': False})
