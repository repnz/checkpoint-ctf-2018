import socket


def seed(x):
    pass


def dilla(seq1, seq2):
    seed(seq1[0])


def kendrick_sum(a):
    s = 0

    for item in a:
        s += item

    return s


def andre_mul(a, b):
    if len(a) > len(b):
        raise Exception  # 1

    dilla(a, [0]*len(a))

    t10 = [0]*(len(a)+len(b))

    for i in xrange(len(b)):
        for j in xrange(len(a)):
            t10[i+j] += a[j]*b[i]

    for i in xrange(len(t10)-2):
        if t10[i] >= 10:
            t10[i+1] += t10[i]/10
            t10[i] %= 10

    return t10


def guru_max(a, b):
    """max function"""
    return a if a > b else b


def doom_compare(aa, bb):
    """
    Checks if aa and bb are equal, ignoring right zeros
    Just compares two integers in the chk repr
    :param aa: list of numbers
    :param bb: list of numbers
    :return: if aa is
    """
    i = len(aa)/2

    # garbage
    while i >= 1:
        if aa[i] == 0:
            aa[i] = 0
        i -= 1

    # Ignore right digits
    i = len(aa)-1
    m = []

    while i >= 0:
        # 6
        if aa[i] > 0:
            # 9
            m = aa[:i+1]
            break
        i -= 1

    # Ignore right digits
    # 7
    f = []

    i = len(bb) - 1
    while i >= 0:
        if bb[i] > 0:
            # 14
            f = bb[:i+1]
            break
        i -= 1

    i = len(aa) - 1

    while i >= 0:
        if aa[i] > 0:
            t43 = aa[i]
            break
        i -= 1

    if len(m) > len(f):
        return 1  # 21
    elif len(m) < len(f):
        return -1  # 23
    else:  # The length is equal
        # 24
        i = len(m) - 1
        # 27
        while i >= 0:
            # 25
            if m[i] > f[i]:
                raise Exception  # 28
            # 29
            elif m[i] < f[i]:
                raise Exception  # 30
            else:  # The value is equal.
                # 31
                i -= 1
        # 26
        return -2


def rakim_sub(a, b):
    """
    Calculates array difference between a and b
    Returns a list that represents the diff
    """
    if doom_compare(a, b) == -1:
        raise Exception  # 1

    diff_arr = [0]*len(a)
    i = 0

    # this is diff array
    # the diff between a - b
    while i < len(a):
        # 3
        a_i = a[i] if i < len(a) else 0
        b_i = b[i] if i < len(b) else 0

        if a_i < b_i:
            raise Exception  # 10

        diff_arr[i] = a_i - b_i
        i += 1

    return diff_arr


def gza_add(a, b):
    """
    Create a new list representing the adding of a and b
    for each element
        c[i] = (a[i]+b[i])%10
        c[i+1] = (a[i]+b[i])/10
    """
    length_of_t4 = guru_max(len(a), len(b)) + 1
    t4 = [0]*length_of_t4
    t5 = [0]

    # doesnt do anything.
    # t8 = a
    # t5 = [0]
    t8 = rakim_sub(a, t5)

    # doesnt do anything!
    # it has to be equal......... because a is t8
    if doom_compare(a, t8) != -2:
        raise Exception  # 1

    # 2, 3
    reminder = 0
    i = 0

    while i < len(t4):
        # 4
        a_i = a[i] if i < len(a) else 0

        # 7
        b_i = b[i] if i < len(b) else 0

        sum_of_digits = (a_i + b_i + reminder)
        reminder = sum_of_digits / 10

        if sum_of_digits >= 10:
            # probably here happens sum_of_digits %= 10
            # sum_of_digits %= 10
             raise Exception  # 10

        # 11
        t4[i] = sum_of_digits
        i += 1

    return t4


def to_number(a):
    i = len(a)-1

    while i >= 0:
        if a[i] > 0:
            num = a[:i+1]
            break
        i -= 1
    else:
        return 0

    return int(''.join(map(str, reversed(num))))


def nas_to_digits(a):
    """
    Convert a string representation of an integer
    to a list containing its digits
    """
    digits = []
    i = len(a) - 1
    z = 0

    while i >= 0:
        a_digit = ord(a[i])-48

        if 0 <= a_digit < 10:
            digits.append(a_digit)

        z += a_digit
        if z == 1024:
            raise Exception("Unknown")
        i -= 1

    return digits


def generate_flag_length_nas():
    t27 = andre_mul((1,), (0, 1))
    t32 = gza_add((0, 2), t27)
    t37 = gza_add((0, 2), t32)
    return andre_mul((2,), t37)


def generate_flag_length():
    """
    (10 + 20 + 20)*2 = 100
    """
    t27 = andre_mul((1,), (0, 1))
    t32 = gza_add((0, 2), t27)
    t37 = gza_add((0, 2), t32)
    digits_num = andre_mul((2,), t37)
    return to_number(digits_num)


def assert_math_func(func, a, b, result):
    assert doom_compare(func(nas_to_digits(str(a)), nas_to_digits(str(b))), nas_to_digits(str(result)))


def test_to_digits():
    assert doom_compare(nas_to_digits(str('123')), (3, 2, 1))
    assert doom_compare(nas_to_digits(str('12a3')), (3, 0, 2, 1))


def test_gza_add():
    for i in xrange(20):
        for j in xrange(20):
            assert_math_func(gza_add, i, j, i+j)


def test_andre_mul():
    for i in xrange(10):
        for j in xrange(100):
            assert_math_func(andre_mul, i, j, i*j)


def test():
    test_to_digits()
    test_gza_add()
    test_andre_mul()


def is_valid_end(end):
    return (ord(end[8]) - ord(end[9])) == ord(end[12])


"""
sum(
"""
def check_input(input):
    success = True
    fields = input.split(' ')
    fields_num = []

    for field_str in fields:
        try:
            fields_num.append(int(field_str))
        except ValueError:
            fields_num.append(0)

    flag_length = generate_flag_length_nas()
    fields_len_nas = nas_to_digits(str(len(fields_num)))

    if doom_compare(fields_len_nas, flag_length) != -2:
        success = False

    for field in fields_num:
        if field <= 0:
            raise Exception("Fields cannot be less then 0")

    half_fields = [0]*(len(fields_num)/2)

    """
    half fields represents the diffs between 2 items
    diffs list
    """
    for i in xrange(len(half_fields)):
        half_fields[i] = fields_num[i*2] - fields_num[i*2+1]

    for i in xrange(len(half_fields)):
        until_now = half_fields[:i+1]
        until_now = kendrick_sum(until_now)
        until_now = str(until_now)
        until_now = nas_to_digits(until_now)

        if doom_compare(until_now, [0]) == -1:
            raise Exception('something is lower')

    even_sum = 0
    odd_sum = 0

    for i in xrange(0, len(fields_num)-1, 2):
        even_sum += fields_num[i]
        odd_sum += fields_num[i+1]

    if even_sum != odd_sum:
        print 'sums are not equal ', even_sum, odd_sum
        success = False

    for i in xrange(len(fields_num)):
        u_arr = []
        for x in xrange(len(u_arr)):
            pass

    if fields_num[49] != 98:
        print '49 != 98, 49=', fields_num[49]
        success = False

    v = fields_num[8] - fields_num[9]
    b = fields_num[12]

    if v != b:
        print 'v != b, v=', v, 'b=', b
        success = False

    if not success:
        print 'No flag for you'
    else:
        print 'yay'

import hashlib


def sha256(x):
    return hashlib.sha256(x).hexdigest()

import itertools

import string
chars = string.letters+string.digits


def hack_hash(end_of_hash, sha):
    for perm in itertools.permutations(chars, 4):
        abcd = ''.join(perm)
        if sha256(abcd+end_of_hash) == sha:
            return abcd
    raise Exception("could not crack hash")


def extract_data(s):

    data = s.recv(1024)

    if len(data) < 120:
        data += s.recv(1024)

    while True:
        try:
            end_of_hash = data[data.index('+')+1:data.index(')')]
            sha = data[data.index('== ')+3:data.index(' (A')]
            return end_of_hash, sha
        except ValueError:
            print data
            data = s.recv(1024)


def extract_abcd_data(abcd):
    first_diff = abcd[0] - abcd[1]
    second_diff = abcd[2] - abcd[3]

    if first_diff < 0:
        raise Exception("Hello???")

    if (first_diff + second_diff) < 0:
        raise Exception("Hello?????????")

    return first_diff+second_diff


def find_divs(h):
    h = sorted(h)

    for a in h:
        for b in h:
            for d in reversed(h):
                if (a+b) == d:
                    return a, b, d
                elif (a+b)>d:
                    break

    raise Exception("Not Found")


def create_f(abcd, i):
    return (
        abcd[i],
        abcd[i+1],
        abcd[i+1],
        abcd[i]
    )


def generate_hack(abcd):
    abcd = sorted(map(ord, abcd), reverse=True)

    arr = [None]*100
    a, b, d = find_divs(abcd)
    arr[:4] = create_f(abcd, 0)
    arr[4:8] = create_f(abcd, 2)

    arr[8] = d
    arr[9] = b
    arr[10] = b
    arr[11] = d
    arr[12] = a
    arr[13] = a
    arr[14] = a
    arr[15] = a

    for i in xrange(16, 48, 4):
        abcd_i = (i-16)/2
        arr[i:i+4] = create_f(abcd, abcd_i)

    arr[48] = 98
    arr[49] = 98

    for i in xrange(50, 98, 4):
        abcd_i = ((i-50)/2) % len(abcd)
        arr[i:i+4] = create_f(abcd, abcd_i)

    arr[98] = abcd[0]
    arr[99] = abcd[0]

    return arr


import time


def main():
    #s = "pciJwR0mCePYmfkeo3iH"
    #print hack_hash('WIjQzqRBGvn5XaKH', '7b8eab361acedd91a59f659a4c536a4dc14881fc4a6ddd97f637a2d767d1db3e')
    #exit()

    #h = ' '.join(map(str, generate_hack('dcba')))
    #check_input(' '.join(map(str, generate_hack('wmMKfIe6R4BecDG7nQB4'))))
    #exit()

    while True:
        s = socket.socket()
        s.connect(('35.194.63.219', 2003))
        end_of_hash, sha = extract_data(s)
        print end_of_hash, sha

        try:
            abcd = hack_hash(end_of_hash, sha)
            print abcd
            if 'b' not in abcd:
                s.close()
                continue
            f = generate_hack(abcd)
            print check_input(' '.join(map(str, f)))
        except Exception as e:
            print e
            s.close()
            continue

        s.send(abcd)
        print s.recv(1024)
        sol = ''.join(map(chr, f))
        print sol
        s.send(sol)
        print s.recv(1024)
        s.close()



if __name__ == '__main__':
    main()

