import blockcipher
import Crypto.Cipher.ARC2
import Crypto
from pkg_resources import parse_version

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
MODE_CTR = 6
#RC2 blocksize is 8bytes, XTS requires 16bytes
#MODE_XTS = 7
MODE_CMAC = 8

def new(key,mode=blockcipher.MODE_ECB,IV=None,counter=None,effective_keylen=None):
	"""Create a new cipher object

	ARC2 using pycrypto for algo en pycryptoplus for ciphermode

	new(key,mode=blockcipher.MODE_ECB,IV=None,counter=None,effective_keylen=None):
		key = raw string containing the keys
		mode = python_AES.MODE_ECB/CBC/CFB/OFB/CTR/CMAC
		IV = IV as a raw string
			-> only needed for CBC mode
		counter = counter object (Cipher/util.py:Counter)
			-> only needed for CTR mode
		effective_keylen = how much bits to effectively use from the supplied key
			-> will only be used when the pycrypto version on your system is >2.0.1

	http://www.ietf.org/rfc/rfc2268.txt
	Doctest will fail when using pycrypto 2.0.1 and older
	------------------------------------
	>>> from CryptoPlus.Cipher import ARC2
	>>> key = "0000000000000000".decode('hex')
	>>> plaintext = "0000000000000000".decode('hex')
	>>> ek = 63
	>>> cipher = ARC2.new(key,ARC2.MODE_ECB,effective_keylen=ek)
	>>> cipher.encrypt(plaintext)
	'ebb773f993278eff'
	"""
	return ARC2(key,mode,IV,counter,effective_keylen)

class ARC2(blockcipher.BlockCipher):
	def __init__(self,key,mode,IV,counter,effective_keylen):
		# pycrypto versions newer than 2.0.1 will have support for "effective_keylen"
		if parse_version(Crypto.__version__) <= parse_version("2.0.1"):
			self.cipher = Crypto.Cipher.ARC2.new(key)
		else:
			self.cipher = Crypto.Cipher.ARC2.new(key,effective_keylen)
		self.blocksize = Crypto.Cipher.ARC2.block_size
		blockcipher.BlockCipher.__init__(self,key,mode,IV,counter)

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()