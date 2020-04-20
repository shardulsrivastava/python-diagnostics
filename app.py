#!/usr/bin/env python
from flask import Flask
from diagnostics import Diagnostics

diagnostic_endpoints = [
    {"name": "API", "endpoint": "https://www.iproperty.com.my/consumer/api/suggestions/diagnostic"},
    {"name": "Upstream - IProperty MY", "endpoint": "https://www.iproperty.com.my/consumer/api/suggestions/diagnostic"},
    {"name": "Downstream - Some API", "endpoint": "https://www.iproperty.com.my/consumer/api/suggestions/diagnostic"},
    {"name": "Database", "endpoint": "tcp://auroradb.cust-tools.prod.sg.rea-asia.local:3306"}
]

app = Flask(__name__)
Diagnostics.render(app, diagnostic_endpoints)


@app.route("/hello")
def test():
    return "Hello"


if __name__ == '__main__':
    app.run()
