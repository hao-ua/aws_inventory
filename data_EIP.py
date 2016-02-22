import boto.ec2


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'EIP'
        self.Priority = 4
        self.show = True
        self.HeaderNames = ['IP address', 'Instance ID', 'Instance name', 'Route53 name']
        self.HeaderWidths = ['2', '2', '5', '4']
        self.HeaderKeys = ['ip_address', 'instance_id', 'name', 'route53_name']
        self.credentials = credentials
        self.Items = items
        self.account = ''
        self.skipRegions = []

    @staticmethod
    def result_dict(address, instances, zones):
        res = dict()
        res['ip_address'] = address.public_ip
        res['instance_id'] = address.instance_id
        res['name'] = 'Empty'
        res['route53_name'] = ''
        for region_name, instancesList in instances.items():
            for instance in instancesList:
                if instance['id'] == address.instance_id:
                    res['name'] = instance['name']
                    break

        for zone_name, records in zones.items():
            if res['ip_address'] in records:
                res['route53_name'] = records[res['ip_address']]
                break

        return res

    def get_all_items(self, aws_key, aws_secret):
        addr = dict()
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue

            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            addresses = conn.get_all_addresses()
            addr[region.name] = []
            for address in addresses:
                addr_dict = self.result_dict(address, self.Items['EC2'][self.account], self.Items['Route53'])
                addr[region.name].append(addr_dict)

        return addr

    def get_data(self):
        eips = {}
        for credential in self.credentials:
            self.account = credential[2]
            eips[credential[2]] = self.get_all_items(credential[0], credential[1])

        return eips
