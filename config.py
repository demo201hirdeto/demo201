
"""
Website settings
"""

# The title of the webpage
title: str = "Demo201 Hirdető"

# The heading that is displayed under 'vezerlo'
heading: str = "ITT TUTSZ SZERVERT HÍRDETNI ODA A EMAIL CIMHEZ BE ÍROD HIRDET@OLDAL.HU ÉS A NÉVHEZ MEG BE ÍROD AMIT AKKARSZ AZ ÜZENÖ FALNÁL ODA CSAK A NEVET ÍRD MEG A EMAIL CIMEDET ÉS KÉSZ"

# Word wrap the ads put up by users
ad_word_wrap: bool = True

"""
Port to run the webserver on.
"""

port: int = 8080

"""
Possible options for ssl_type:
> 'none' (browsers don't like this)
> 'self-signed' (browsers will display big nono error)
> 'custom' (add your own certificate below in ssl_cert, and your private key in ssl_key)

PRO TIP: You can use self-signed with CloudFlare's full tls mode.
"""

ssl_type: str = "none"

ssl_cert: str = "cert.pem"
ssl_key: str = "key.pem"

"""
Misc settings
"""

# Stop every # hours
# This can be useful if you have a sh script running a while loop that automatically restarts the server
# Exit code of the program will be: -60000001
# Set to -1 to disable (Not recommended)
restart_hours: float = -1

"""
CAPTCHA SETTINGS

It's highly recommended to enable turnstile. Otherwise the captcha will switch to our beloved, what's the day today?
Turnstile is really cool. Its also free! Generate your keys here: https://dash.cloudflare.com/?to=/:account/turnstile/add

IMPORTANT: DO NOT SHARE your secret key!
"""

turnstile_enabled: bool = False

turnstile_sitekey: str = "0x4AAAAAAA--------------"
turnstile_secretkey: str = "0x4AAAAAAA-------------------------"
