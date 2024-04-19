import time
import random
import math

# Function to perform a brute force attack to find the private_exponent which is d
def bruteforce(e, eul):
    d=1
    while True:
        if (d * e) % eul == 1:
            return d
        d += 1

# Prompting the user to choose the bit lenght either 8 or 16
print("Choose the bit lenght: ")
print("1. 8-bits")
print("2. 16-bits")
choice = input("Enter your choice (1 or 2):")
if choice == "1":
    bit_lenght = 8
elif choice == "2":
    bit_lenght = 16
else:
    print("Invalid choice! Exiting...")
    exit()
# Function that generates RSA keys
def generate_rsa_keys(bit_length):
    p = int(input("Enter a prime number (p):"))
    while not is_prime(p):
        p=int(input("Error!, please enter a prime number:"))
    q = int(input("Enter a prime numbe (q):"))
    while not is_prime(q):
        q=int(input("Error!, please enter a prime number:"))
    if p == q:
        print("The two prime values cannot be equal")
        raise ValueError("The two prime values cannot be equal")
    n = p * q
    # Checking if n exceeds the maximum value allowed for the chosen bit lenght
    if n > 255 and bit_lenght == 8:
        print("n is greater than 8 bits")
        raise ValueError(f"{n} is not an 8 bit number")
    if n > 65532 and bit_lenght == 16:
        print("n is greater than 16 bits")
        raise ValueError(f"{n} is not a 16 bit number")
    eul = (p - 1) * (q - 1)
    e = choose_public_exponent(eul)
    
    start=time.perf_counter()
    
    d = bruteforce(e,eul)

    end = time.perf_counter()

    runtime = end - start

    print(f"Run time is {runtime} seconds")
    # Ensuring that e is not equal to d
    while e == d:
        e = choose_public_exponent(eul)
        d = bruteforce(e,eul)

    public_key = (n, e)
    private_key = (n, d)
    
    return n, public_key, private_key
# Function that checks if the number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num))+ 1):
        if num % i == 0:
            return False
    return True


# Function to choose a public exponent
def choose_public_exponent(eul):
 
    e = random.randrange(2, eul)
    while math.gcd(e, eul) != 1:
        e = random.randrange(2, eul)
    return e


# Function for encryption
def encryption(message, public_key):
    n, e= public_key
    if message >= n:
        print( ValueError("The message you have entered cannot be is larger than n "))
        raise( ValueError("The message you have entered cannot be is larger than n "))
    return pow(message, e, n)
# Function for decryption
def decryption(c, private_key):
    n, d = private_key
    return pow(c, d, n)
# Function to factorize a number
def factorize(n):
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors

# Generate RSA keys
n, public_key, private_key = generate_rsa_keys(bit_lenght)
print("Public Key (n, e):", public_key)
print("Private Key (n, d):", private_key)
print("Prime factors of n:",factorize(n))
message = int(input("Enter the message you want to encrypt: "))
encrypted_message= encryption(message, public_key)
decrpted_message= decryption(encrypted_message, private_key)
print("Original Message:", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message", decrpted_message)