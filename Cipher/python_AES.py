# wrapper for rijndael.py. rijndael.py can be found here:
#	http://bitconjurer.org/rijndael.py
# other possible python AES implementations:
#	http://psionicist.online.fr/code/rijndael.py.txt
#	http://jclement.ca/software/pyrijndael/

import blockcipher
from rijndael import rijndael

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
MODE_CTR = 6
MODE_XTS = 7
MODE_CMAC = 8

def new(key,mode=blockcipher.MODE_ECB,IV=None,counter=None):
	"""Create a new cipher object

	new(key,mode=blockcipher.MODE_ECB,IV=None,counter=None):
		key = raw string containing the key, AES-128..256 will be selected according to the key length
			-> when using XTS mode: the key should be a concatenation of the 2 keys needed
		mode = python_AES.MODE_ECB/CBC/CFB/OFB/CTR/XTS/CMAC
		IV = IV as a raw string
			-> only needed for CBC mode
		counter = counter object (Cipher/util.py:Counter)
			-> only needed for CTR mode
    
    	EXAMPLE:
	----------
	>>> import python_AES
	>>> cipher = python_AES.new('0123456789012345')
	>>> cipher.encrypt('0123456789012345')
	'_}\\xf0\\xbf\\x10:\\x8cJ\\xe6\\xfa\\xad\\x99\\x06\\xac;*'
	>>> cipher.decrypt(_)
	'0123456789012345'

	CBC EXAMPLE (plaintext = 3 blocksizes):
	-----------------------------------------
	>>> from binascii import hexlify,unhexlify
	>>> import python_AES
	>>> key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c')
	>>> IV = unhexlify('000102030405060708090a0b0c0d0e0f')
	>>> plaintext1 = unhexlify('6bc1bee22e409f96e93d7e117393172a')
	>>> plaintext2 = unhexlify('ae2d8a571e03ac9c9eb76fac45af8e51')
	>>> plaintext3 = unhexlify('30c81c46a35ce411e5fbc1191a0a52ef')
	>>> cipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> ciphertext = cipher.encrypt(plaintext1 + plaintext2 + plaintext3)
	>>> hexlify(ciphertext)
	'7649abac8119b246cee98e9b12e9197d5086cb9b507219ee95db113a917678b273bed6b8e3c1743b7116e69e22229516'
	>>> decipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> plaintext = decipher.decrypt(ciphertext)
	>>> hexlify(plaintext)
	'6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	OR: supply plaintext as seperate pieces:
	------------------------------------------
	>>> cipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> hexlify( cipher.encrypt(plaintext1 + plaintext2[:-2]) )
	'7649abac8119b246cee98e9b12e9197d'
	>>> hexlify( cipher.encrypt(plaintext2[-2:] + plaintext3) )
	'5086cb9b507219ee95db113a917678b273bed6b8e3c1743b7116e69e22229516'
	>>> decipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> hexlify(decipher.decrypt(ciphertext[:22]))
	'6bc1bee22e409f96e93d7e117393172a'
	>>> hexlify(decipher.decrypt(ciphertext[22:]))
	'ae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	CTR EXAMPLE:
	------------
	>>> from util import Counter
	>>> key = '2b7e151628aed2a6abf7158809cf4f3c'.decode('hex')
	>>> counter = Counter('f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'.decode('hex'))
	>>> cipher = python_AES.new(key,python_AES.MODE_CTR,counter=counter)
	>>> plaintext1 = '6bc1bee22e409f96e93d7e117393172a'.decode('hex')
	>>> plaintext2 = 'ae2d8a571e03ac9c9eb76fac45af8e51'.decode('hex')
	>>> plaintext3 = '30c81c46a35ce411e5fbc1191a0a52ef'.decode('hex')
	>>> ciphertext = cipher.encrypt(plaintext1 + plaintext2 + plaintext3)
	>>> ciphertext.encode('hex')
	'874d6191b620e3261bef6864990db6ce9806f66b7970fdff8617187bb9fffdff5ae4df3edbd5d35e5b4f09020db03eab'
	>>> counter2 = Counter('f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'.decode('hex'))
	>>> decipher = python_AES.new(key,python_AES.MODE_CTR,counter=counter2)
	>>> decipher.decrypt(ciphertext).encode('hex')
	'6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	XTS EXAMPLE:
	cipher/decipher plaintext of 3 blocks, provided as a 2 pieces (31 bytes + 33 bytes)
	------------
	>>> key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c'*2)
	>>> plaintext1 = unhexlify('6bc1bee22e409f96e93d7e117393172a')
	>>> plaintext2 = unhexlify('ae2d8a571e03ac9c9eb76fac45af8e51')
	>>> plaintext3 = unhexlify('30c81c46a35ce411e5fbc1191a0a52ef')
	>>> cipher = python_AES.new(key,python_AES.MODE_XTS)
	>>> ciphertext = cipher.encrypt(plaintext1 + plaintext2[:15])
	>>> decipher = python_AES.new(key,python_AES.MODE_XTS)
	>>> deciphertext = decipher.decrypt(ciphertext)
	>>> hexlify(deciphertext)
	'6bc1bee22e409f96e93d7e117393172a'
	>>> ciphertext2 = cipher.encrypt(plaintext2[15:]+plaintext3)
	>>> deciphertext2 = decipher.decrypt(ciphertext2)
	>>> hexlify(deciphertext2)
	'ae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	XTS-AES-128 applied for a data unit of 512 bytes
	testvector: http://grouper.ieee.org/groups/1619/email/pdf00086.pdf


	>>> key = '2718281828459045235360287471352631415926535897932384626433832795'.decode('hex')
	>>> plaintext = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'.decode('hex')
	>>> cipher = python_AES.new(key,python_AES.MODE_XTS)
	>>> cipher.encrypt(plaintext).encode('hex')
	'27a7479befa1d476489f308cd4cfa6e2a96e4bbe3208ff25287dd3819616e89cc78cf7f5e543445f8333d8fa7f56000005279fa5d8b5e4ad40e736ddb4d35412328063fd2aab53e5ea1e0a9f332500a5df9487d07a5c92cc512c8866c7e860ce93fdf166a24912b422976146ae20ce846bb7dc9ba94a767aaef20c0d61ad02655ea92dc4c4e41a8952c651d33174be51a10c421110e6d81588ede82103a252d8a750e8768defffed9122810aaeb99f9172af82b604dc4b8e51bcb08235a6f4341332e4ca60482a4ba1a03b3e65008fc5da76b70bf1690db4eae29c5f1badd03c5ccf2a55d705ddcd86d449511ceb7ec30bf12b1fa35b913f9f747a8afd1b130e94bff94effd01a91735ca1726acd0b197c4e5b03393697e126826fb6bbde8ecc1e08298516e2c9ed03ff3c1b7860f6de76d4cecd94c8119855ef5297ca67e9f3e7ff72b1e99785ca0a7e7720c5b36dc6d72cac9574c8cbbc2f801e23e56fd344b07f22154beba0f08ce8891e643ed995c94d9a69c9f1b5f499027a78572aeebd74d20cc39881c213ee770b1010e4bea718846977ae119f7a023ab58cca0ad752afe656bb3c17256a9f6e9bf19fdd5a38fc82bbe872c5539edb609ef4f79c203ebb140f2e583cb2ad15b4aa5b655016a8449277dbd477ef2c8d6c017db738b18deb4a427d1923ce3ff262735779a418f20a282df920147beabe421ee5319d0568'


	CMAC EXAMPLE:
	-------------
	testvector: http://csrc.nist.gov/publications/nistpubs/800-38B/Updated_CMAC_Examples.pdf
	
	>>> key = '2b7e151628aed2a6abf7158809cf4f3c'.decode('hex')
	>>> plaintext = '6bc1bee22e409f96e93d7e117393172a'.decode('hex')
	>>> cipher = python_AES.new(key,python_AES.MODE_CMAC)
	>>> cipher.encrypt(plaintext).encode('hex')
	'070a16b46b4d4144f79bdd9dd04a287c'

	CMAC EXAMPLE2:
	--------------
	>>> key = '2b7e151628aed2a6abf7158809cf4f3c'.decode('hex')
	>>> plaintext = '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411'.decode('hex')
	>>> cipher = python_AES.new(key,python_AES.MODE_CMAC)
	>>> cipher.encrypt(plaintext).encode('hex')
	'dfa66747de9ae63030ca32611497c827'
	"""
	return python_AES(key,mode,IV,counter)

class python_AES(blockcipher.BlockCipher):
	"""Wrapper for pure python implementation rijndael.py

	"""
	def __init__(self,key,mode,IV,counter):
		if mode == MODE_XTS:
			assert len(key)/2 in (16, 24, 32)
			self.cipher = rijndael(key[:16], 16)
			self.cipher2 = rijndael(key[16:], 16)
		else:
			self.cipher = rijndael(key, 16)
		self.blocksize = 16
		blockcipher.BlockCipher.__init__(self,key,mode,IV,counter)

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
