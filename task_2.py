import math
import copy
import binascii


def F(x, y, z):
    result = (x & y | ~x & z)
    return result


def G(x, y, z):
    result = x & z | y & ~z
    return result


def H(x, y, z):
    result = x ^ y ^ z
    return result


def I(x, y, z):
    result = y ^ (x | ~ z)
    return result


def addition(x, y, m=2 ** 32):  # Функция для сложения по модулю 2**32
    z = (x + y) % m
    return z


def shift(x, s):  # Функция для битового сдвига
    x = bin(x)[2:]
    x = x[s:] + x[:s]
    return int(x, 2)


text = input("Введите текст: ")

My_string = ''
for i in text:
    My_string += hex(ord(i))[2:]
length = str(hex(len(My_string) * 4))
My_string += '8'
My_string += ('0' * (112 - len(My_string) % 128 + 4))
My_string = My_string + '0' * (16 - len(length)) + length[2:]

buffers = [
    0x67425301,  # A
    0xEDFCBA45,  # B
    0x98CBADFE,  # C
    0x13DCE476  # D
]

S = [
    [7, 12, 17, 22],
    [5, 9, 14, 20],
    [4, 11, 14, 23],
    [6, 10, 15, 21]
]

P = [F, G, H, I]

T = []  # Константы
for i in range(1, 65):
    T.append(round(2 ** 32 * abs(math.sin(i))))

blocks = []
#print(My_string)
for i in range(2, len(My_string), 128):
    blocks.append(My_string[i:i + 128])

for b in range(0, len(blocks)):
    block = copy.deepcopy(blocks[b])
    blocks[b] = []
    for i in range(0, 128, 8):
        blocks[b].append(int(block[i:i + 8], 16))

iteration = 0
for b in range(0, len(blocks)):
    for r in range(0, 4):
        for i in range(0, len(blocks[b])):
            bufferCopy = copy.deepcopy(buffers)
            processFunction = P[r](buffers[1], buffers[2], buffers[3])
            buffers[0] = addition(buffers[0], processFunction)
            buffers[0] = addition(buffers[0], blocks[b][i])
            buffers[0] = addition(buffers[0], T[iteration])
            buffers[0] = shift(buffers[0], S[r][i // 4])
            buffers[0] = addition(buffers[0], buffers[1])
            buffers = buffers[3:4] + buffers[0:3]
            iteration += 1

hex_string = '0x'
for i in buffers:
    hi = hex(i)[2:]
    if len(hi) < 8:
        hi = '0' * (8 - len(hi)) + hi
    hex_string += hi
print(hex_string)
