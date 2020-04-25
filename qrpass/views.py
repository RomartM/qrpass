import json

from django.shortcuts import render
from django.http import JsonResponse
from .decryption import qr_pass_decrypt, qr_pass_validate


def home(request):
    return render(request, 'main.html')


def webrtc(request):
    return render(request, 'webrtc.html')


def validate(request, qr_hash):
    if not (qr_pass_validate(qr_hash)):
        return JsonResponse(status=200, data={'code': 401, 'response': 'Unauthorized'})
    if len(qr_hash.split('==')[1]) > 0:
        return JsonResponse(status=200, data={'code': 403, 'response': 'Forbidden'})
    user_data = {
        'code': 200,
        'response': 'Valid QR',
        'id': json.loads(qr_pass_decrypt(qr_hash)).get('user-id'),
        'name': 'Romart',
        'position':'Web Developer',
        'photo': 'https://lh3.googleusercontent.com/proxy/7Heu55BHR_178drkDtt2LGQAMGP6zyMzy79zaUnO8a6nJ3PEbvMoMtcg8qxZzEZNhco9Ja4ypHhVSwNNE_dyyMH9tudJKVYIZxv1nEzs1zGz3zteow'
    }
    return JsonResponse(status=200, data=user_data)
