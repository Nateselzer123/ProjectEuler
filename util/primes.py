from definitions import ROOT_DIR
from os import path
import pickle
import math
from bitarray import bitarray
import time


class PrimeUtils:
    def __init__(self):
        self.sieve = bitarray([0, 0])
        self.sieve_file_path = path.join(ROOT_DIR, "build/prime_sieve.txt")
        try:
            open(self.sieve_file_path, 'rb').close()
        except IOError:
            f = open(self.sieve_file_path, 'wb+')
            pickle.dump(self.sieve, f)
            f.close()

    def file_stored_prime_sieve_helper(self, n):
        with open(self.sieve_file_path, 'rb') as f:
            tmp_sieve = pickle.load(f)
            if len(tmp_sieve) >= n:
                return tmp_sieve
            else:
                self.augment_existing_sieve(tmp_sieve, n)
        with open(self.sieve_file_path, 'wb') as f:
            pickle.dump(tmp_sieve, f)
            return tmp_sieve

    def in_mem_prime_sieve_helper(self, n):
        if len(self.sieve) > n:
            return self.sieve
        else:
            self.augment_existing_sieve(self.sieve, n)
            return self.sieve

    def augment_existing_sieve(self, existing_sieve, desired_length):
        existing_sieve.extend([1] * (desired_length - len(existing_sieve)))
        for i in range(int(math.sqrt(len(existing_sieve)))):
            if existing_sieve[i] != 0:
                j = 2 * i
                while j < len(existing_sieve):
                    existing_sieve[j] = 0
                    j += i
        return existing_sieve

    def prime_sieve_helper(self, n):
        if n > 1000000:
            return self.file_stored_prime_sieve_helper(n)
        else:
            return self.in_mem_prime_sieve_helper(n)

    def primes_less_than(self, n):
        ps = self.prime_sieve_helper(n)[:n]
        return [x for x in range(len(ps)) if ps[x]]


