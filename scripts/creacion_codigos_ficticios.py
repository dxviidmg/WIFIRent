import random
import string
from codigos.models import * 

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def run():
    n = int(input('Numero de codigos a crear: '))
    slug = input('Url del plan: ')

    plan = Plan.objects.get(slug=slug)
    i = 0
    while i < n:
        i += 1
        codigo = get_random_string(11)

        Codigo.objects.get_or_create(
            codigo = codigo, 
            plan = plan)
    
    print('fin')
    