# Local project imports
from core import app, r, p

# Standard python imports
import os

# Third party imports
from flask import render_template, send_from_directory, g, request, abort, jsonify


# Application index
@app.route("/")
def index():
    return render_template("index.html")

# Application start POST
@app.route("/start", methods=["POST"])
def startPOST():
    buddyList = []
    respData = {}  # Stores all data that will be returned

    r.flushall()  # Flush all old keys

    for i in xrange(1,6):
        user = request.form["user%s" % i]
        pnum = request.form["pnum%s" % i]
        if user != "" and pnum != "":
            uid = r.incr("global:userid")  # Get a unique id for each user
            buddyList.append({
                "uid": uid,
                "user": user,
                "num": pnum,
                "verified": '0'  # By default, not verified
                })

            r.set("uid:%s:name" % uid, user)
            r.set("uid:%s:number" % uid, pnum)
            r.set("uid:%s:verified" % uid, "0")

            r.set("number:%s:uid" % pnum, uid)  # Reverse index for lookup via number

            r.rpush("global:group", uid)  # Storing uid in list (NOT set as order is important)

    respData["buddyList"] = buddyList

    # Search & rent a number
    code, response = p.search_numbers({"country_code": "1"})  # Fixed to US numbers

    if code != 200:  # Bad request to the api
        abort(500)

    if response["meta"]["total_count"] == 0:  # No more numbers left
        abort(500)

    number = response["objects"].pop()["number"]  # Extract first number from the list
    code, response = p.rent_number({"number": number, "app_id": app.config["PLIVO_APP_ID"]})  # rent the number

    if code != 201:  # Was unable to rent the number
        # TODO: retry for few more times?
        abort(500)

    r.set("global:number", number)  # Storing currently rented number
    respData["number"] = number

    # send verfication for all 5 users
    for uid in r.lrange("global:group", 0, -1):
        code, response = p.send_message({
                            "src": number,
                            "dst": r.get("uid:%s:number" % uid),
                            "text": "Hi, You have been invited to a group chat. Reply with YES to join. Ignore if not interested.",
                            "type": "sms"
                            })

        if code != 202:  # Bad request to api. message queuing failed
            abort(500)

    return render_template("start.html", respData=respData)

# Application start GET
@app.route("/start", methods=["GET"])
def startGET():
    respData = {
        "number": r.get("global:number"),
        "buddyList": []
    }

    for uid in r.lrange("global:group", 0, -1):
        respData["buddyList"].append({
                "uid": uid,
                "user": r.get("uid:%s:name" % uid),
                "num": r.get("uid:%s:number" % uid),
                "verified": r.get("uid:%s:verified" % uid)
            })

    return render_template("start.html", respData=respData)

# Application message
@app.route("/message")
def message():
    src = request.args.get('From', '')
    text = request.args.get('Text', '')
    srcUid = r.get("number:%s:uid" % src)

    if srcUid:
        if r.get("uid:%s:verified" % srcUid) == "1":
            # Number is verified, send the messsage to the group
            uids = set.difference(set(r.lrange("global:group", 0, -1)), set([srcUid]))  # finding a set difference to find all users except the sender
            for uid in uids:
                if r.get("uid:%s:verified" % uid) == "1":
                    code, response = p.send_message({
                            "src": r.get("global:number"),
                            "dst": r.get("uid:%s:number" % uid),
                            "text": "%s: %s" % (r.get("uid:%s:name" % srcUid), text),
                            "type": "sms"
                            })
        else:
            # Number is not verified, check if the incoming message is 'YES'
            if text.strip().upper() == "YES":
                r.set("uid:%s:verified" % srcUid, "1")

    return ""

# Verifiction of the number
@app.route("/verification")
def verfication():
    resp = {
        "status": "success",
        "buddyList": []
    }

    for uid in r.lrange("global:group", 0, -1):
        if r.get("uid:%s:verified" % uid) == "1":
            resp["buddyList"].append({
                    "uid": uid,
                    "verified": True
                })
        else:
            resp["buddyList"].append({
                    "uid": uid,
                    "verified": False
                })

    return jsonify(resp)

# Application error handlers
@app.errorhandler(500)
def server_error(error=None):
    return render_template("500.html"), 500

@app.errorhandler(404)
def not_found(error=None):
    return render_template("404.html"), 404

@app.errorhandler(400)
def bad_request(error=None):
    return render_template("400.html"), 400


# Etc routes (favicon, robots.txt, humans.txt, etc.)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')


@app.route('/humans.txt')
def humans():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'humans.txt', mimetype='text/plain')
