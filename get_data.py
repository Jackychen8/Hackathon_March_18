import requests
import json

class ElasticSearchObj(object):
    def __init__(self, host='localhost'):
        self.es_host = host

    def request(self, method, url, headers=None, data=None):
        if not headers:
            # mutable default arguments are bad
            headers = {}
        types = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete
        }
        default_header = {
            "Content-Type": "application/json"
        }
        headers.update(default_header)
        if method.upper() in types:
            try:
                return types[method.upper()](url, headers=headers, data=json.dumps(data))
            except Exception:
                msg = "url: "
                raise Exception("Request", msg)
        raise Exception("Request", "Method: {0} not valid".format(method))

    def search(self, query, i=None):
        url = "{0}/{1}/_search".format(self.es_host, i) if i else "{0}/_search".format(self.es_host)
        data = {
            "query": query,
            "sort": {"@timestamp": "desc"},
            "_source": ["@timestamp", "host", "netflow.destinationIPv4Address",
                        "netflow.destinationMacAddress", "netflow.sourceIPv4Address",
                        "netflow.sourceMacAddress", "netflow.packetDeltaCount", "netflow.octetDeltaCount"],
            "size": "500"
        }
        print(url)
        res = self.request("POST", url, data=data)
        print(res.status_code)
        return res.json()["hits"]["hits"] if res.status_code == 200 else []