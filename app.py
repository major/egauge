"""Simple flask server for querying eGauge data."""
import os
import xml.etree.ElementTree as ET

import requests
from flask import Flask, jsonify

EGAUGE_ADDRESS=os.environ.get("EGAUGE_ADDRESS")
EGAUGE_URL=f"http://{EGAUGE_ADDRESS}/cgi-bin/egauge?inst"

app = Flask(__name__)


def get_egauge_xml():
    """Retrieve the XML from the eGauge device."""
    return requests.get(EGAUGE_URL).content

def parse_xml():
    """Parse the XML returned from the eGauge device."""
    root = ET.fromstring(get_egauge_xml())

    for elem in root.findall('./r[@n="Grid"]/i'):
        grid_power = int(elem.text)

    for elem in root.findall('./r[@n="Solar"]/i'):
        solar_power = int(elem.text)

    return {
        "current_usage": abs(solar_power) - grid_power,
        "from_grid": grid_power,
        "from_solar": solar_power
    }


@app.route('/')
def egauge_data():
    return jsonify(parse_xml())


if __name__ == '__main__':
    app.run(host="0.0.0.0")
