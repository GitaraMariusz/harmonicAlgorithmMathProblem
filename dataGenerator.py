import random

def generate_random_numbers(n, min=0, max=1000):
    random_numbers = []

    if n % 2 != 0:
        n=n-1
        
    for i in range(n):
        number = random.uniform(min, max)
        random_numbers.append({"id": i, "number": number})
        
        return generate_random_numbers
    
print(generate_random_numbers)