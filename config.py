
"""
Port to run the webserver on.
"""

port: int = 8080

"""
Possible options:
> 'none' (browsers don't like this)
> 'self-signed' (browsers will display big nono error)
> 'custom' (add your own certificate below in ssl_cert, and your private key in ssl_key)
"""
ssl_type: str = "none"

ssl_cert: str = "cert.pem"
ssl_key: str = "key.pem"

"""
CAPTCHA SETTINGS

It's highly recommended to enable turnstile.
Turnstile is really cool. Generate your keys here: https://dash.cloudflare.com/?to=/:account/turnstile/add

IMPORTANT: DO NOT SHARE your secret key!
"""

turnstile_enabled: bool = False

turnstile_sitekey: str = "0x4AAAAAAA--------------"
turnstile_secretkey: str = "0x4AAAAAAA-------------------------"

