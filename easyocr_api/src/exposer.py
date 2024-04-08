import os
import json

from Shimarin.plugins.flask_api import emitter, app, CONTEXT_PATH
from Shimarin.server.events import Event

from flask import request

EVENTS: list[Event] = []


def checkID():
    return os.getenv("PRIVATE_SECRET") == request.args.get("secret")


@app.route(CONTEXT_PATH + "/captcha", methods=["POST"])
async def captcha():
    data: dict = request.json
    image = data.get("image")
    if not checkID():
        return {
            "status": "error",
            "msg": "Secret is wrong"
        }, 401
    if image is None:
        return {
            "status": "error",
            "msg": "Error loading image!"
        }, 400
    event = Event.new("captcha", image, json.loads)
    EVENTS.append(event)
    await emitter.send(event)
    return {
        "status": "processing",
        "id": event.identifier
    }


@app.route(CONTEXT_PATH + "/result", methods=["GET"])
async def result():
    if not checkID():
        return {
            "status": "error",
            "msg": "Secret is wrong"
        }, 401
    event_id = request.args.get("id")
    if not any(event.identifier == event_id for event in EVENTS):
        return {
            "status": "error",
            "msg": "ID not found!"
        }, 400
    event = [event for event in EVENTS if event.identifier == event_id][0]
    if event.answered:
        return {
            "status": "done",
            "text": event.answer["text"]
        }
    return {
        "status": "processing",
        "id": event_id
    }


@app.route(CONTEXT_PATH + "/health", methods=["GET", "HEAD"])
async def health_check():
    return {
        "status": "up"
    }, 200


def main():
    app.run(host="0.0.0.0", port=2222)
