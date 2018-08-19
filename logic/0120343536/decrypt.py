import operator

flag = "JTW_$U!$@G@U@GQW_FGDZRE_G$_#RTV"

"""
_ -> 95
$ -> 36
! -> 33
@ -> 64
# -> 35
"""

"""
A  -  Z
65 - 90
"""
flag_ascii = \
[74, 84, 87, 95, 36, 85, 33, 36,
 64, 71, 64, 85, 64, 71, 
81, 87, 95, 70, 71, 68, 90, 82, 69, 
95, 71, 36, 95, 35, 82, 84, 86]

def in_of_ch(c):
	return ord(c) - 65

def ch_of_in(inx):
	return chr(inx+65)

def do(data, key, op):
	r = []

	i_ = [0, 1, 2, 0, 3, 4, 3, 5, 3, 6]
	i = 0
	for e in data:
		if not (ord(e) >= ord('A') and ord(e) <= ord('Z')):
			continue

		r.append(op(ord(e), ord(key[i_[i % len(i_)] % len(key)])))
		i += 1
			

	return r

LEN = (ord('Z')-65)+1

def calculate(x, y):
	num_index = x - 65
	key_index = y - 65

	num_index ^= num_index
	num_in
	return x ^ y

d = set(open('dictionary.txt', 'rb').read().split('\r\n'))
results = [''.join(map(chr, do(flag, key, calculate))) for key in d]
results.sort(key=lambda x: x.count('E'), reverse=True)

print '\n'.join(results)