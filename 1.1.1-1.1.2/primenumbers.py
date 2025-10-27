def find_and_print_primes(start, end):
    if start < 2:
        start = 2

    print(f"Prime numbers between {start} and {end}:")
    for num in range(start, end + 1):
        is_prime = True
        if num <= 1:
            is_prime = False
        else:
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
        
        if is_prime:
            print(num)

find_and_print_primes(1, 100000)