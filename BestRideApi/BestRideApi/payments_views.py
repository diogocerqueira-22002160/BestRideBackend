import json
import urllib.parse
import urllib3
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

class Payments(APIView):

    @api_view(['POST'])
    def make_payment(request):
        http = urllib3.PoolManager()
        data = {
            "amount": request.data['amount'],
            "currency": "eur",
            "source": request.data['token'],
            "description": "Example charge",
        }

        data = urllib.parse.urlencode(data)

        headers = {
            'Authorization': 'Bearer ' + 'sk_test_51JUeiuImOAMxh8jbAfe6Xt8n8BQdNyjbPmO9bgVSvzyNjhv9SaqL54C2T3YJcvhyLw65539fI9zJFY3rfBqRGwOQ0084dqyi6Y',
        }

        r = http.request('POST', 'https://api.stripe.com/v1/charges',headers=headers,body=data)
        return Response({'msg':r.read()})
