from definitions import ROOT_DIR
from os import path
import pickle
import math
from bitarray import bitarray


class PrimeUtils:
    def __init__(self):
        self.sieve = [0, 0]
        self.primes = []
        self.sieve_file_path = path.join(ROOT_DIR, "build/prime_sieve.txt")
        try:
            open(self.sieve_file_path, 'rb')
        except IOError:
            f = open(self.sieve_file_path, 'wb+')
            pickle.dump((self.primes, self.sieve), f)
            f.close()

    def file_stored_prime_sieve_helper(self, n):
        with open(self.sieve_file_path, 'rb') as f:
            tmp_primes, tmp_sieve = pickle.load(f)
            if len(tmp_sieve) >= n:
                return tmp_primes, tmp_sieve
            else:
                tmp_sieve = self.augment_existing_sieve(tmp_sieve, n)
                tmp_primes = [prime for prime in tmp_sieve if not prime == 0]
        with open(self.sieve_file_path, 'wb') as f:
            pickle.dump((tmp_primes, tmp_sieve), f)
            return tmp_primes, tmp_sieve

    def in_mem_prime_sieve_helper(self, n):
        if len(self.sieve) > n:
            return self.primes, self.sieve
        else:
            self.sieve = self.augment_existing_sieve(self.sieve, n)
            self.primes = [prime for prime in self.sieve if prime != 0]
            return self.primes, self.sieve

    def augment_existing_sieve(self, existing_sieve, desired_length):
        print(len(existing_sieve), desired_length)
        tmp_sieve = existing_sieve + list(range(len(existing_sieve), desired_length))
        for i in range(int(math.sqrt(len(tmp_sieve)))):
            if tmp_sieve[i] != 0:
                j = 2 * i
                while j < len(tmp_sieve):
                    tmp_sieve[j] = 0
                    j += i
        return tmp_sieve

    def prime_sieve_helper(self, n):
        if n > 1000000:
            return self.file_stored_prime_sieve_helper(n)
        else:
            return self.in_mem_prime_sieve_helper(n)

pu = PrimeUtils()

print(pu.prime_sieve_helper(100007001)[1][10000001])


