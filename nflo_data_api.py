from flask import Flask
from scfinder import get_recent_records

app = Flask(__name__)

CACHE = {}

@app.route("/")
def ret_def():
    return "Default Endpoint"

@app.route("/data")
def ret_data():
    global CACHE
    recs = get_recent_records('1m')
    d = {}# MAC to MAC
    if recs:
        for rec in recs:
            key = str(rec.smac) + str(rec.dmac)
            if key in d:
                # update pkts and bytes
                d[key]['pkts'] += rec.pkts
                d[key]['kB'] += rec.byts/1000
            else:
                d[key] = {
                    'pkts': rec.pkts,
                    'kB': rec.byts/1000,
                }
            d[key]['kB'] = int(round(d[key]['kB']))

    return(str(d))
