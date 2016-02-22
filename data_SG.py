import boto.ec2
import boto


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'SG'
        self.Priority = 8
        self.show = True
        self.HeaderNames = ['Protocol', 'Port', 'Source']
        self.HeaderWidths = ['1', '2', '6']
        self.HeaderKeys = ['protocol', 'port', 'source']
        self.credentials = credentials
        self.Items = items
        self.skipRegions = []

    def result_dict(self, sg, name, rule):
        res = dict()
        res['protocol'] = str(sg.ip_protocol)
        if sg.from_port != sg.to_port:
            res['port'] = "-".join([str(sg.from_port), str(sg.to_port)])
        else:
            res['port'] = str(sg.from_port)

        res['source'] = str(rule)
        res['name'] = name
        return res

    def get_all_items(self, aws_key, aws_secret, items):
        res = dict()
        regions = boto.ec2.regions()
        for region in regions:
            if region.name in self.skipRegions:
                continue

            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            all_sgs = conn.get_all_security_groups()
            for sg in all_sgs:
                r_key = " ".join([region.name, sg.name])
                res[r_key] = []
                for item in sg.rules:
                    for rule in item.grants:
                        sg_dict = self.result_dict(item, sg.name, rule)
                        res[r_key].append(sg_dict)

        return res

    def get_data(self):
        sgs = dict()
        for credential in self.credentials:
            sgs[credential[2]] = self.get_all_items(credential[0], credential[1], self.Items)

        return sgs
