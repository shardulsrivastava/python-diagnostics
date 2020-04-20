#!/usr/bin/env python

from flask import render_template
import requests
import os
import socket


class Diagnostics:
    diagnostic_endpoints = None

    @staticmethod
    def render(app, endpoints):
        Diagnostics.diagnostic_endpoints = endpoints
        app.add_url_rule('/heartbeat', 'heartbeat', Diagnostics.heartbeat)
        app.add_url_rule('/diagnostics', 'diagnostics', Diagnostics.diagnostics)

    @staticmethod
    def create_html():
        current_path = os.path.dirname(os.path.realpath(__file__))
        templates_dir = f"{os.getcwd()}/templates"
        if not os.path.isdir(templates_dir):
            os.makedirs(templates_dir)
        with open(f"{current_path}/templates/diagnostics.html", 'r') as src, open(f"{templates_dir}/diagnostics.html",
                                                                                  'w') as destination:
            destination.write(src.read())

    @staticmethod
    def get_status(endpoints):
        status = "All Systems Are Operational"
        for endpoint in endpoints:
            endpoint_status = endpoint["status"]
            if endpoint_status == "Not Operational":
                status = "Not All Systems Are Operational"
                break
        return status

    """
    This method return 1 in case of success or 0 in case of failure of probe.
    """

    @staticmethod
    def probe(endpoint):
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return Diagnostics.probe_http(endpoint)
        elif endpoint.startswith("tcp://"):
            return Diagnostics.probe_tcp(endpoint)
        else:
            print(f"Unsupported probe endpoint => {endpoint}")

    @staticmethod
    def probe_http(url):
        probe_status = 0
        response = requests.get(url=url)
        if response.status_code == 200 or response.status_code == 301:
            probe_status = 1
        return probe_status

    @staticmethod
    def probe_tcp(url):
        probe_status = 0
        endpoint = url.replace("tcp://", "").split(":")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect((endpoint[0], int(endpoint[1])))
            s.shutdown(socket.SHUT_RDWR)
            probe_status = 1
        except:
            print(f"Unable to connect to => {url}")
        finally:
            s.close()
        return probe_status

    @staticmethod
    def diagnostics():
        endpoints = Diagnostics.diagnostic_endpoints
        i = 0
        Diagnostics.create_html()
        for component in endpoints:
            endpoint = component["endpoint"]
            probe_status = Diagnostics.probe(endpoint)

            if probe_status > 0:
                endpoints[i]["status"] = "Operational"
                endpoints[i]["class"] = "label-success"
            else:
                endpoints[i]["status"] = "Not Operational"
                endpoints[i]["class"] = "label-danger"
            i = i + 1
        overall_status = Diagnostics.get_status(endpoints)

        return render_template("diagnostics.html", len=len(endpoints),
                               diagnostic_components=endpoints, status=overall_status)

    @staticmethod
    def heartbeat():
        return "Ok"


if __name__ == "__main__":
    diagnostic_endpoints = [
        {"name": "API", "endpoint": "https://www.iproperty.com.my/consumer/api/suggestions/diagnostic"},
        {"name": "Upstream - IProperty MY",
         "endpoint": "https://www.iproperty.com.my/consumer/api/suggestions/diagnostic"},
        {"name": "Downstream - Some API",
         "endpoint": "https://www.iproperty.com.my/consumer/api/suggestions/diagnostic"},
        {"name": "Database", "endpoint": "tcp://auroradb.cust-tools.prod.sg.rea-asia.local:3306"}
    ]
    Diagnostics.render(diagnostic_endpoints)
