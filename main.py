from flask import Flask, render_template, request, make_response, redirect, Response
from datetime import datetime
from threading import Thread
from time import time, sleep
from ad import Ad
import requests
import config
import json
import pytz
import os

ads: list = []


def ma_nap_magyar_gmt_plus_2():
    # Nap nevek magyar fordításban
    nap_nevek = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]

    # Jelenlegi dátum és idő lekérése
    aktualis_datumido = datetime.now()

    # GMT+2 időzóna beállítása
    gmt_plus_2 = pytz.timezone('Etc/GMT+2')

    # Jelenlegi dátum és idő átkonvertálása a GMT+2 időzónába
    gmt_plus_2_datumido = aktualis_datumido.astimezone(gmt_plus_2)

    # A hét napjának meghatározása és visszaadása
    nap_index = gmt_plus_2_datumido.weekday()
    nap_magyar = nap_nevek[nap_index]

    return nap_magyar


if not os.path.exists("hirdetesek"):
    os.mkdir("hirdetesek")
else:
    for adFile in os.listdir("hirdetesek"):
        with open("hirdetesek/" + adFile, mode="r", encoding="UTF-8") as adF:
            data = json.loads(adF.read())
            ads.append(Ad(str(data["name"]), str(data["description"]), int(data["time"]), False))

app = Flask(__name__)

ads = sorted(ads, key=lambda inst: inst.time)


@app.route("/", methods=["GET"])
def home() -> str:
    if config.turnstile_enabled:
        captcha_name = "Captcha:"
        turnstile_html = f"<div class=\"cf-turnstile\" data-sitekey={config.turnstile_sitekey} data-callback=\"javascriptCallback\"></div>"
    else:
        captcha_name = "Milyen nap van ma magyarországon?"
        turnstile_html = "<input type=\"text\" class=\"grayinput\" name=\"mai-nap\" size=\"60\" maxlength=\"100\">"

    adsHTML = "<div style=\"border-color:#ffffff;border-style:solid;border-width:3px\">"
    i = 0
    for ad in ads[::-1]:
        i += 1

        if i > 1:
            adsHTML += "<br><hr>"

        date_time = str(datetime.fromtimestamp(ad.time))
        adsHTML = adsHTML + f"<br><b> <div class=\"setbyuser\">{ad.name}</div> <font color=\"#999999\">[ {date_time} ]</font></b><br><br><div class=\"setbyuser\">" + ad.description.replace(
            '\n', '<br>') + "</div>"

        adsHTML += "<br>"

    adsHTML += "</div>"
    word_wrap = ""
    if config.ad_word_wrap:
        word_wrap = \
            """
                .setbyuser {
                  word-wrap: break-word;
                  width: 650px;
                }
            """
    return render_template("index.html",
                           ads=adsHTML,
                           turnstile_html=turnstile_html,
                           title=config.title,
                           heading=config.heading,
                           captcha_name=captcha_name,
                           word_wrap=word_wrap)


@app.route("/add-ad", methods=["POST"])
def add_server() -> Response:
    resp = make_response()
    try:
        name = request.form['name'].strip()
        description = request.form['description'].strip()

        if name.replace(" ", "").replace("\n", "") == "" \
                or description.replace(" ", "").replace("\n", "") == "":
            raise Exception("blank fields :(")

        name = name.replace("<", "\\<").replace(">", "\\>")
        description = description.replace("<", "\\<").replace(">", "\\>")
    except:
        resp.status_code = 400
        resp.response = "Blank fields!"
        return resp

    try:
        if len(name) > 50 or len(description) > 4000:
            raise Exception("fields too long :(")
    except:
        resp.status_code = 400
        resp.response = "Fields too long!"
        return resp

    if config.turnstile_enabled:
        try:
            tkn = request.form.get('cf-turnstile-response')
            cf_ip = request.headers.get("CF-Connecting-IP")
            print(tkn)
            resp_json = json.loads(
                requests.post(url="https://challenges.cloudflare.com/turnstile/v0/siteverify",
                              data=f"secret={config.turnstile_secretkey}&response={tkn}&remoteip={cf_ip}",
                              headers={
                                  "Content-Type": "application/x-www-form-urlencoded"
                              }, ).text
            )

            print(json.dumps(resp_json))

            if not resp_json["success"]:
                raise Exception("invalid captcha :(")
        except:
            resp.status_code = 400
            resp.response = "Captcha invalid!"
            return resp
    else:
        try:
            mainap = request.form.get('mai-nap')
            if not mainap.strip() == ma_nap_magyar_gmt_plus_2().strip():
                raise Exception("Captcha invalid :(")
        except:
            resp.status_code = 400
            resp.response = "Captcha invalid!"
            return resp

    ads.append(Ad(name, description, int(time()), True))
    return redirect("/", code=301)


if config.ssl_type == "self-signed":
    ssl_context = "adhoc"
elif config.ssl_type == "custom":
    ssl_context = (config.ssl_cert, config.ssl_key)
else:
    ssl_context = None


def start_flask():
    app.run(host="0.0.0.0", port=config.port, ssl_context=ssl_context, debug=False)


flask_thread = Thread(target=start_flask)
flask_thread.daemon = True


def restarter():
    start_time = time()
    restart_seconds = config.restart_hours * 60 * 60
    while True:
        sleep(0.1)
        if time() - start_time >= restart_seconds:
            exit(-60000001)


if config.restart_hours != -1:
    flask_thread.start()
    restarter()
else:
    flask_thread.daemon = False
    flask_thread.run()

