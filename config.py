
"""
Possible options:
> 'self-signed' (browsers will display big nono error)
> 'custom' (add your own certificate below in ssl_cert, and your private key in ssl_key)
"""
ssl_type = "self-signed"

ssl_cert = "cert.pem"
ssl_key = "key.pem"

"""
CAPTCHA SETTINGS

It's highly recommended to enable turnstile.
Turnstile is really cool. Generate your keys here: https://dash.cloudflare.com/?to=/:account/turnstile/add

IMPORTANT: DO NOT SHARE your secret key!
"""

turnstile_enabled = False

turnstile_sitekey = "0x4AAAAAAA--------------"
turnstile_secretkey = "0x4AAAAAAA-------------------------"

