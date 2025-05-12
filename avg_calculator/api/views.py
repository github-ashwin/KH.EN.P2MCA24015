from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
# Create your views here.

window_size = 10
window_state = []

URLS = {
    'p': 'http://20.244.56.144/evaluation-service/primes',
    'f': 'http://20.244.56.144/evaluation-service/fibo',
    'e': 'http://20.244.56.144/evaluation-service/even',
    'r': 'http://20.244.56.144/evaluation-service/rand'
}

def get(request,type):
    global window_state

    prev_window = window_state.copy()

    if type not in URLS:
        return JsonResponse({'error': "Invalid type"})
    
    try:
        header = {'Authorization':f"Bearer{settings.access_token}"}
        response = requests.get(URLS[type], headers=header, timeout=0.5)

        if response.status_code != 200:
            return JsonResponse({"error": "Fail"})
        
        fetched_numbers = response.json().get("numbers", [])

        for i in fetched_numbers:
            if i not in window_state:
                window_state.append(i)
                if len(window_state) > window_size:
                    window_state.pop(0)
        
        avg = round(sum(window_state) / len(window_state), 2) if window_state else 0.0

        return JsonResponse({
            "windowPrevState": prev_window,
            "windowCurrState": window_state,
            "numbers": fetched_numbers,
            "avg": avg
        })
    
    except requests.exceptions.RequestException:
        return JsonResponse({"error": "Timeout"})