'''
AMIEL VINCENT V. DE CASTRO
Y6L
'''

from cryptography.fernet import Fernet

def key_fernet():
	file_key = open('key.key','rb')
	key = file_key.read()
	return Fernet(key)

def decrypt_file(file):
	f = key_fernet()

	file_library_system = open(file,'rb')
	encrypted = file_library_system.read()
	decrypted = f.decrypt(encrypted)

	file_library_system_new = open(file,'wb')
	file_library_system_new.write(decrypted)
	file_library_system_new.close()

def encrypt_file(file):
	f = key_fernet()
	
	file_library_system = open(file,'rb')
	original = file_library_system.read()
	encrypted = f.encrypt(original)
	
	file_library_system_new = open(file,'wb') 
	file_library_system_new.write(encrypted)
	file_library_system_new.close()