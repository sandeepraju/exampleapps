# Starndard python imports
import random

# Third party imports
import plivo

class PlivoTwoFactorAuth:
	""" `PlivoTwoFactorAuth` provides two factor authentication
		mechanism for applications using Plivo APIs
	"""

	def __init__(self, credentails, appNumber):
		"""
		"""
		self.p = plivo.RestAPI(credentails["auth_id"],
								credentails["auth_token"])
		self.appNumber = appNumber

	def getVerificationCode(self, dstNumber, message="__code__"):
		""" `getVerificationCode` accepts destination
			number to which call has to be made along with the message
			that has to be sent.

			The message text should contain a `__code__` construct
			in the message text which will be replaced by the
			code generated before sending the SMS
		"""
		code = random.choice(xrange(100000,999999))  # generating 6 digit random code
		responseCode, responseData = self.p.send_message({
										"src": self.appNumber,
										"dst": dstNumber,
										"text": message.replace("__code__", str(code)).strip(),
										"type": "sms"				
									})

		if responseCode != 202:
			raise Exception

		return code