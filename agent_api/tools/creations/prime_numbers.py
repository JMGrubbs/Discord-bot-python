def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# Generate prime numbers under 100
prime_numbers = [str(x) for x in range(2, 100) if is_prime(x)]

# Print the prime numbers in a comma-separated format
print(",".join(prime_numbers))
