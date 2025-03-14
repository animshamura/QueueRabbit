import base64

d_token = "aGZfRkF6Vll5eHNkdUtvand3cFhtYkRFblVXdnpmS2FCSFhIdw=="
dtok = d_token.encode("ascii")
tok = base64.b64decode(dtok)
token = tok.decode("ascii")
