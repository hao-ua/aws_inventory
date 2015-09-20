import boto.ec2

class data:
    def __init__(self, credentials, Items):
        self.Name = 'EC2'
        self.Priority = 3
        self.show = True
        self.HeaderNames = ['ID', 'Name', 'ELB name', 'IP address', 'State', 'Route53 name', 'Private IP', 'Public DNS', 'Instance type', 'Security groups']
        self.HeaderWidths = ['2', '5', '2', '2', '1', '4', '2', '6', '2', '4']
        self.HeaderKeys = ['id', 'name', 'elb', 'ip_address', 'state', 'route53_name', 'private_ip_address', 'public_dns', 'type', 'sg']
        self.credentials = credentials
        self.Items = Items
        self.account = ''
        self.skipRegions = []

    def resultDict(self, instance, zones, elb_name=''):
        res = dict()
        if 'Name' in instance.tags:
            res['name'] = instance.tags['Name']
        else:
            res['name'] = 'Empty'
        res['ip_address'] = instance.ip_address
        res['id'] = instance.id
        res['public_dns'] = instance.public_dns_name
        res['state'] = instance.state
        res['type'] = instance.instance_type
        res['ssh_key'] = instance.key_name
        res['image_id'] = instance.image_id
        res['sg'] = ','.join([group.name for group in instance.groups])
        res['placement'] = instance.placement
        res['private_ip_address'] = instance.private_ip_address
        res['elb'] = elb_name.split('.')[0].rsplit('-', 1)[0]
        res['route53_name'] = ''
        for zone_name, records in zones.items():
            if res['ip_address'] in records:
                res['route53_name'] = records[res['ip_address']]
                break
            elif res['public_dns'] in records:
                res['route53_name'] = records[res['public_dns']]
                break
            elif res['public_dns']+'.' in records:
                res['route53_name'] = records[res['public_dns']+'.']
                break
        return res

    def getAllItems(self, aws_key, aws_secret, Items):
        result = dict()
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue            
            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            reservations = conn.get_all_instances()
            for reservation in reservations:
                for instance in reservation.instances:
                    elb_name = ''
                    if region.name in Items['ELB'][self.account]:
                        for elb in Items['ELB'][self.account][region.name]:
                            if instance.id in elb['instances']:
                                elb_name = elb['dns_name']
                                break
                    instanceDict = self.resultDict(instance, Items['Route53'], elb_name)
                    if instanceDict['placement'] in result:
                        result[instanceDict['placement']].append(instanceDict)
                    else:
                        result[instanceDict['placement']] = [instanceDict]
        return result

    def getData(self):
        EC2s = dict()
        for credential in self.credentials:
            self.account = credential[2]
            EC2s[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return EC2s
