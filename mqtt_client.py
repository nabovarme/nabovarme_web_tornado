import paho.mqtt.client as mqtt
import rethinkdb as r
import urlparse
from logging import getLogger
from helpers.log import get_logger

logger = get_logger("mqtt_client")

nabo_channels = [
        "/sample/v1/#",
        ]
r.connect("0.0.0.0", 32768).repl()
r_table = r.db("nabovarme").table("samples")

def on_connect(client, userdata, flags, rc):
    print "connected"
    [client.subscribe(channel) for channel in nabo_channels]

def on_message(client, userdata, msg):
    try:
        payload = urlparse.parse_qs(urlparse.urlsplit(msg.payload).path)
        payload = {key:value for key,value in ((key,dict(zip(["value", "unit"], values[0].split(" ")))) for key, values in payload.iteritems())}
        payload.pop("heap", None)
        doc = dict(zip(["meter_id", "unix_time"],[int(val) for val in msg.topic.split("/")[3:]]))
        doc['unix_time'] = r.epoch_time(doc["unix_time"])
        doc["payload"] = payload
        if payload:
           res = r_table.insert(doc).run()
           if not res["inserted"] == 1:
               msg = "not inserted! topic:{} payload:{}".format(msg.topic, msg.payload)
               raise ValueError(msg)
    except Exception:
        logger.exception(msg.topic)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("loppen.christiania.org")
client.loop_forever()
