
from twisted.web import server, resource
from twisted.internet import reactor, endpoints, ssl
from fake_switches.netconf import dict_2_etree
from lxml import etree
import time
import json
import logging

CONNECTION_ID=0
 
class Brocade(resource.Resource):
    isLeaf = True
    def render_PATCH(self, request):
        content = request.content.read().decode("utf-8")
        logging.info("PATCH %s %r %s", request.getHeader('authorization'), request.uri, content)
        res=dict(Response={
        })
        return etree.tostring(dict_2_etree(res), pretty_print=True)

    def render_GET(self, request):
        content = request.content.read().decode("utf-8")
        logging.info("GET %s %r %s", request.getHeader('authorization'), request.uri, content)
        if request.uri == b"/rest/running/brocade-fibrechannel-switch/fibrechannel-switch":
            res=dict(Response={
                "fibrechannel-switch":{
                    "firmware-version": "42"
                }
            })
            return etree.tostring(dict_2_etree(res), pretty_print=True)
        elif request.uri == b"/rest/running/zoning/effective-configuration":
            res=dict(Response={
                "effective-configuration":{
                    "cfg-name": "ConfigA",
                    "checksum": "42"
                }
            })
            return etree.tostring(dict_2_etree(res), pretty_print=True)
        elif request.uri == b"/rest/running/zoning/defined-configuration/alias": 
            res=dict(Response={
                "alias": []
            })
            return etree.tostring(dict_2_etree(res), pretty_print=True)
        elif request.uri == b"/rest/running/zoning/defined-configuration/zone":
            res=dict(Response={
                "zone": []
            })
            return etree.tostring(dict_2_etree(res), pretty_print=True)
        elif request.uri == b"/rest/running/zoning/defined-configuration/cfg":
            res=dict(Response={
                "cfg": []
            })
            return etree.tostring(dict_2_etree(res), pretty_print=True)
        elif request.uri == b"/rest/running/zoning/defined-configuration":
            res=dict(Response={
               "defined-configuration": { "zone": [] } 
            })
            return etree.tostring(dict_2_etree(res), pretty_print=True)

        return b"<html>Hello, world!</html>"

    def render_POST(self, request):
        global CONNECTION_ID
        content = request.content.read().decode("utf-8")
        if request.uri == b"/rest/login":
            time.sleep(0.1) # this can take time
            logging.info("POST login %r %s", request.uri, content)
            CONNECTION_ID += 1
            request.responseHeaders.addRawHeader("Authorization", "CNX" + str(CONNECTION_ID))
        else:
            logging.info("POST %r %r %s", request.getHeader('authorization'), request.uri, content)
        return b"<html>Hello, world!</html>"


class Svc(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        global CONNECTION_ID
        content = request.content.read().decode("utf-8")
        if request.uri == b"/rest/auth":
            time.sleep(0.1) # this can take time
            logging.info("POST auth %r %s", request.uri, content)
            CONNECTION_ID += 1
            b = json.dumps({"token": "CNX" + str(CONNECTION_ID)})
            return b.encode('utf-8')
        elif request.uri == b'/rest/lshost/test1':
            logging.info("POST %s %r %s", request.getHeader('x-auth-token'), request.uri, content)
            res = {'id': '226', 'name': 'test1', 'port_count': '2', 'type': 'generic', 'mask': '1111111111111111111111111111111111111111111111111111111111111111', 'iogrp_count': '1', 'status': 'offline', 'site_id': '', 'site_name': '', 'host_cluster_id': '', 'host_cluster_name': '', 'protocol': 'scsi', 'nodes': [{'WWPN': 'abc', 'node_logged_in_count': '0', 'state': 'offline'}, {'WWPN': 'def', 'node_logged_in_count': '0', 'state': 'offline'}]}
            return json.dumps(res).encode('utf-8')

        elif request.uri == b'/rest/mkhost': 
            logging.info("POST %s %r %s", request.getHeader('x-auth-token'), request.uri, content)
            return json.dumps({"message": "ca roule"}).encode('utf-8')
        else:
            logging.info("POST %s %r %s", request.getHeader('x-auth-token'), request.uri, content)
        return b"<html>Hello, world!</html>"

logging.basicConfig(level='DEBUG')
logger = logging.getLogger()
logger.setLevel('DEBUG')

site = server.Site(Brocade())
endpoint = endpoints.SSL4ServerEndpoint(reactor, 8443, ssl.DefaultOpenSSLContextFactory("pkey", "cert.pem"))
endpoint.listen(site)


site = server.Site(Svc())
endpoint = endpoints.SSL4ServerEndpoint(reactor, 7443, ssl.DefaultOpenSSLContextFactory("pkey", "cert.pem"))
endpoint.listen(site)


reactor.run()


