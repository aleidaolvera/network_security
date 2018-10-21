import hashlib
import json
import sys

json_file = sys.argv[1]     # grab json file from arg
message_sig = sys.argv[2]   # grab message or sig file

with open(json_file,'r') as r:
    json_data = r.read()
pubkey = json.loads(json_data)
e = pubkey["e"];
n = pubkey["n"];
with open(message_sig,'r') as r:
    json_data = r.read()
sig_file = json.loads(json_data)
original_sig = sig_file["sig"];
original_msg = sig_file["m"];
# ensure message is going to be hashed over ascii version
original_msg.encode('ascii')
# message_sig turns into hashed int
message_int = int(hashlib.sha256(original_msg).hexdigest(),16)
# decrypt to find message_int / signature from hashed int using pub key pairs (e,n) from json file
calculated_msg = pow(original_sig, e, n)
print(calculated_msg == message_int)
