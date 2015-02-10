import boto.ec2
import boto

class data:
    def __init__(self, credentials, Items):
        self.Name = 'SG'
        self.Priority = 8
        self.show = True
        self.HeaderNames = ['Protocol', 'Port', 'Source']
        self.HeaderWidths = ['1', '2', '6']
        self.HeaderKeys = ['protocol', 'port', 'source']
        self.credentials = credentials
        self.Items = Items
        self.skipRegions = []

    def resultDict(self, sg, name, rule):
        res = {}
        res['protocol'] = str(sg.ip_protocol)
        if sg.from_port != sg.to_port:
            res['port'] = "-".join([str(sg.from_port),str(sg.to_port)])
        else:
            res['port'] = str(sg.from_port)
        res['source'] = str(rule)
        res['name'] = name
        return res

    def getAllItems(self, aws_key, aws_secret, Items):
        res = {}
        regions = boto.ec2.regions()
        for region in regions:
            if region.name in self.skipRegions:
                continue
            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            allSGs = conn.get_all_security_groups()
            for sg in allSGs:
                r_key = " ".join([region.name, sg.name])
                res[r_key] = []
                for item in sg.rules:
                    for rule in item.grants:
                        SGDict = self.resultDict(item, sg.name, rule)
                        res[r_key].append(SGDict)
        return res

    def getData(self):
        SGs = {}
        for credential in self.credentials:
            SGs[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return SGs
