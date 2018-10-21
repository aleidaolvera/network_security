import hashlib
import json
import sys


json_file = sys.argv[1]     # grab json file from arg
message = sys.argv[2]   # grab message or sig file

with open(json_file,'r') as r:
    json_data = r.read()
privkey = json.loads(json_data)
d = privkey["d"];
n = privkey["n"];
# ensure message is going to be hashed over ascii version
message.encode('ascii')
# message_sig turns into hashed int
message_int = int(hashlib.sha256(message).hexdigest(),16)
# create signature from hashed int using private key pairs (d,n) from json file
signature = pow(message_int, d, n)
signature_json = {
    "sig" : signature,
    "m" : message
  }
# dump json to a sig.json file
myjson = json.dumps(signature_json)
with open("sig.json",'w') as w:
    w.write(myjson)
print(myjson)
