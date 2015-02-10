import boto.ec2

class data:
    def __init__(self, credentials, Items):
        self.Name = 'EIP'
        self.Priority = 4
        self.show = True
        self.HeaderNames = ['IP address', 'Instance ID', 'Instance name', 'Route53 name']
        self.HeaderWidths = ['2', '2', '5', '4']
        self.HeaderKeys = ['ip_address', 'instance_id', 'name', 'route53_name']
        self.credentials = credentials
        self.Items = Items
        self.account = ''
        self.skipRegions = []

    def resultDict(self, address, instances, zones):
        res = {}
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

    def getAllItems(self, aws_key, aws_secret, Items):
        addr = {}
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue            
            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            addresses = conn.get_all_addresses()
            addr[region.name] = []
            for address in addresses:
                addrDict = self.resultDict(address, Items['EC2'][self.account], Items['Route53'])
                addr[region.name].append(addrDict)
        return addr

    def getData(self):
        EIPs = {}
        for credential in self.credentials:
            self.account = credential[2]
            EIPs[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return EIPs
