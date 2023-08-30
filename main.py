from flask import Flask, render_template, request, make_response, redirect, Response
from datetime import datetime
from time import time
from ad import Ad
import os
import json
import config
import requests

ads: list = []

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
        turnstile_html = f"<div class=\"cf-turnstile\" data-sitekey={config.turnstile_sitekey} data-callback=\"javascriptCallback\"></div>"
    else:
        turnstile_html = ""

    adsHTML = ""
    for ad in ads[::-1]:
        date_time = str(datetime.fromtimestamp(ad.time))
        adsHTML = adsHTML + f"<b> {ad.name} <font color=\"#999999\">[ {date_time} ]</font></b><br><br>" + ad.description.replace(
            '\n', '<br>') + "<br><br>"

    return render_template("index.html",
                           ads=adsHTML,
                           turnstile_html=turnstile_html,
                           title=config.title,
                           heading=config.heading)


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

    print(name)
    print(description)
    ads.append(Ad(name, description, int(time()), True))
    return redirect("/", code=301)


if config.ssl_type == "self-signed":
    ssl_context = "adhoc"
elif config.ssl_type == "custom":
    ssl_context = (config.ssl_cert, config.ssl_key)
else:
    ssl_context = None

app.run(host="0.0.0.0", port=config.port, ssl_context=ssl_context)
