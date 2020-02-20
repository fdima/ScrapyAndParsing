def ddd(text):
	 return int(''.join(filter(lambda x: x.isdigit(), text)))

print (ddd("99 9,3 xcxc 3we"))