
class FlowRecord(object):
    def __init__(self, index, host, timestamp, sip, dip, smac, dmac, pkts, byts, layer2=False):
        self.index = index
        self.host = host
        self.timestamp = timestamp
        self.sip = sip
        self.dip = dip
        self.smac = smac
        self.dmac = dmac
        self.pkts = pkts
        self.byts = byts
        self.layer2 = layer2

    def __repr__(self):
        return 'FloRec S {} {} {} D {}'.format(self.smac, self.byts, self.pkts, self.dmac)

    @classmethod
    def create_record(cls, data):
        source = data["_source"]
        if "netflow" in source:
            index = data["_index"]
            host = source["host"]
            timestamp = source["@timestamp"]
            netflow = source["netflow"]
            layer2 = False
            if "sourceIPv4Address" in netflow:
                sip = netflow["sourceIPv4Address"]
                dip = netflow["destinationIPv4Address"]
            else:
                sip = ''
                dip = ''
                layer2 = True
            pkts = netflow['packetDeltaCount'] if 'packetDeltaCount' in netflow else 0
            byts = netflow['octetDeltaCount'] if 'octetDeltaCount' in netflow else 0
            smac = netflow["sourceMacAddress"]
            dmac = netflow["destinationMacAddress"]

            return cls(index, host, timestamp, sip, dip, smac, dmac, pkts, byts, layer2)
        return None