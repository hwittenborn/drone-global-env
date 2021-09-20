import base64
import hashlib
import hmac
import os
import json
import re

from fastapi import FastAPI, Request, Body
from functions.validate_config import validate_config

# Verify config file.
response_vars = validate_config()

app = FastAPI()

# Verify that a token was passed.
plugin_token = os.environ.get("DRONE_ENV_PLUGIN_TOKEN")

if plugin_token is None:
    print("[Error] A plugin token wasn't set.")
    print("[Error] Make sure the 'DRONE_ENV_PLUGIN_TOKEN' environment variable is set, and try again.")
    exit(1)

# Start up app.
@app.post("/")
async def main(request: Request):
    # Get headers and body.
    headers = request.headers
    body = (await request.body()).decode()

    # Get needed JSON data.
    json_body = json.loads(body)
    build_link = json_body["build"]["link"]

    # Verify digest.
    digest = headers.get("digest").split("=")
    digest_title = digest[0]
    digest_string = "=".join(digest[1:])

    calculated_digest = hashlib.sha256(body.encode()).digest()
    calculated_digest_base64 = base64.b64encode(calculated_digest).decode()

    if calculated_digest_base64 != digest_string:
        print(f"[Error] Sent data didn't match recorded digest hash ({build_link}).")
        return []

    signature = headers.get("signature").split(',')

    # Make sure we have the signature header.
    if signature is None:
        print(f"[Error] Couldn't find the signature header ({build_link}).")
        return []

    # Get list of signature headers we need to verify.
    for i in signature:
        if re.search("^headers=", i) is not None:
            signature_headers = re.sub('^headers=|"', "", i).split(" ")

    # Generate HMAC string.
    hmac_verification_string = ""

    for i in signature_headers:
        current_header_value = headers.get(i)

        if current_header_value is None:
            print(f"[Error] Couldn't find needed header '{i} ({build_link})'.")
            return []

        hmac_verification_string += f"{i}: {current_header_value}\n"

    # Strip the leading newline from the verification string.
    hmac_verification_string = hmac_verification_string.strip()

    # base64-encode the HMAC signature.
    hmac_digest = hmac.digest(plugin_token.encode(), hmac_verification_string.encode(), hashlib.sha256)
    hmac_digest_base64 = base64.b64encode(hmac_digest).decode()

    # Actually return the data.
    print(f"[Info] Succesfully processed request ({build_link}).")
    return response_vars
