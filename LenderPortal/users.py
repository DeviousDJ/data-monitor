#greg's password is 1234

userTable = [
	{"id": 1, "username": "greg", "password": "e2fc714c4727ee9395f324cd2e7f331f"},
	{"id": 2, "username": "alfie", "password": "efgh"},
	{"id": 3, "username": "bob", "password": "ijkl"}
]

from md5 import md5

print type(userTable)

class User:
	def __init__(self, username):
		self.db = userTable
		self.username = username

	def set_password(self, newpassword):
		newpassword = md5(newpassword).hexdigest()
		# update table

	def get_id(self):
		for row in self.db:
			if row['username']==self.username:
				return unicode(row['id'])

	def is_anonymous(self):
		return False

	def is_active(self):
		return True

	def is_authenticated(self):
		return False

	def authenticate(self, password):
		password = md5(password).hexdigest()
		for row in self.db:
			if row['username']==self.username:
				if row['password']==password:
					return True
		return False

u = User("greg")
print u.get_id()
print u.is_anonymous()
print u.authenticate("abcd")
print u.authenticate("e2fc714c4727ee9395f324cd2e7f331f")