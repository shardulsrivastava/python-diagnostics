#!/usr/bin/env python

from flask import request
import requests
import os
import socket
from jinja2 import Template


class Diagnostics:
    diagnostic_endpoints = []

    @staticmethod
    def render(app, endpoints, root_path=''):
        if isinstance(endpoints, list):
            Diagnostics.diagnostic_endpoints = endpoints
            app.add_url_rule(f'{root_path}/heartbeat', 'heartbeat', Diagnostics.heartbeat)
            app.add_url_rule(f'{root_path}/diagnostics', 'diagnostics', Diagnostics.diagnostics)
        else:
            raise DiagnosticEndpointException("endpoints should be a list")

    @staticmethod
    def render_html(diagnostic_endpoints):
        status = Diagnostics.get_status(diagnostic_endpoints)
        length = len(diagnostic_endpoints)
        current_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{current_path}/templates/diagnostics.html", 'r') as template_html:
            template = Template(template_html.read())
            return template.render(len=length, diagnostic_components=diagnostic_endpoints, status=status)

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
    def probe(application_endpoint):
        endpoint = application_endpoint["endpoint"]
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return Diagnostics.probe_http(endpoint)
        elif endpoint.startswith("tcp://"):
            return Diagnostics.probe_tcp(endpoint)
        else:
            request_url = request.url_root[:-1] + endpoint
            return Diagnostics.probe_http(request_url)

    @staticmethod
    def probe_http(url):
        probe_status = 0
        probe_exception = None
        try:
            response = requests.get(url=url, timeout=2)
            response.raise_for_status()
            if response.status_code == 200 or response.status_code == 301:
                probe_status = 1
        except requests.exceptions.Timeout:
            probe_exception = "Request Timed out in 2 seconds."
            print(f"Unable to connect to => {url}, Exception => {probe_exception}")
        except requests.exceptions.TooManyRedirects:
            probe_exception = "Too Many Redirects."
            print(f"Unable to connect to => {url}, Exception => {probe_exception}")
        except requests.exceptions.HTTPError as err:
            probe_exception = f"Couldn't connect to URL. Failed with HTTP {err.response.status_code}"
            print(f"Unable to connect to => {url}, Exception => {probe_exception}")
        except requests.exceptions.RequestException:
            probe_exception = "Unable to connect to URL"
            print(f"Unable to connect to => {url}, Exception => {probe_exception}")
        except Exception as exception:
            probe_exception = exception
            print(f"Unable to connect to => {url}, Exception => {probe_exception}")

        return {"status": probe_status, "exception": probe_exception}

    @staticmethod
    def probe_tcp(url):
        probe_status = 0
        probe_exception = None
        endpoint = url.replace("tcp://", "").split(":")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect((endpoint[0], int(endpoint[1])))
            s.shutdown(socket.SHUT_RDWR)
            probe_status = 1
        except socket.error as error:
            if not error.errno and "timed out" in str(error):
                probe_exception = "Request Timed out in 2 seconds."
            elif error.errno == 8:
                probe_exception = "Couldn't resolve DNS address."
            else:
                probe_exception = os.strerror(error.errno)
            print(f"Unable to connect to => {url}, Exception => {probe_exception}")
        finally:
            s.close()
        return {"status": probe_status, "exception": probe_exception}

    @staticmethod
    def diagnostics():
        endpoints = Diagnostics.diagnostic_endpoints
        i = 0
        ##Diagnostics.create_html()
        for component in endpoints:
            probe_response = Diagnostics.probe(component)
            probe_status = probe_response["status"]

            if probe_status > 0:
                endpoints[i]["status"] = "Operational"
                endpoints[i]["class"] = "label-success"
            else:
                endpoints[i]["status"] = "Not Operational"
                endpoints[i]["class"] = "label-danger"

            endpoints[i]["exception"] = probe_response["exception"]
            i = i + 1

        return Diagnostics.render_html(endpoints)

    @staticmethod
    def heartbeat():
        return "Ok"


class DiagnosticEndpointException(Exception):
    pass
