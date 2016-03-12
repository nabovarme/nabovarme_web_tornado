import paho.mqtt.client as mqtt
import rethinkdb as r
import urlparse

from pprint import pprint
#topic: /sample/v1/6185544/1457737320 payload: heap=15592&t1=67.46 C&t2=26.87 C&tdif=40.59 K&flow1=14 l/h&effect1=0.6 kW&hr=71343 h&v1=2745.12 m3&e1=74536 kWh&

nabo_channels = [
        "/sample/v1/#",
        "/status/v1/#",
        "/uptime/v1/#"
        ]
r.connect("0.0.0.0", 32768).repl()

sample_table = ""

r.connect("0.0.0.0", 32768).repl()

r_table = r.db("nabovarme").table("samples")

def on_connect(client, userdata, flags, rc):
    print "connected"
    [client.subscribe(channel) for channel in nabo_channels]

def on_message(client, userdata, msg):
    #print "topic:", msg.topic, "payload:", msg.payload
    payload = urlparse.parse_qs(urlparse.urlsplit(msg.payload).path)
    payload = {key:value for key,value in ((key,dict(zip(["value", "unit"], values[0].split(" ")))) for key, values in payload.iteritems())}
    payload.pop("heap")
    doc = dict(zip(["meter_id", "unix_time"],[int(val) for val in msg.topic.split("/")[3:]]))
    doc['unix_time'] = r.epoch_time(doc["unix_time"])
    doc["payload"] = payload
    if payload:
        pprint(r_table.insert(doc).run())
    else:
        print "not inserting", payload
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("loppen.christiania.org")
client.loop_forever()
