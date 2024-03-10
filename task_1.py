import random

a = input("Введите строку: ")
arr = []
for i in range(len(a)):
    arr.append(ord(a[i]))


hash = []
C = random.uniform(0, 1)

for i in range(len(arr)):
    K = arr[i]
    M = len(arr)
    result = round(M*((K*C)%1))
    hash.append(str(result))

print(''.join(hash))

