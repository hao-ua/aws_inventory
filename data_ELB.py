import boto.ec2.elb
import boto

class data:
    def __init__(self, credentials, Items):
        self.Name = 'ELB'
        self.Priority = 2
        self.show = True
        self.HeaderNames = ['Name', 'DNS name', 'Count', 'Route53 name']
        self.HeaderWidths = ['2', '6', '1', '4']
        self.HeaderKeys = ['name', 'dns_name', 'instances_count', 'route53_name']
        self.credentials = credentials
        self.Items = Items
        self.skipRegions = []

    def resultDict(self, region, elb, zones):
        res = {}
        res['instances'] = [instance.id for instance in elb.instances]
        res['instances_details'] = []
        res['dns_name'] = elb.dns_name
        res['name'] = elb.dns_name.split('-')[0]
        res['listeners'] = elb.listeners
        res['instances_count'] = len(res['instances'])
        res['route53_name'] = ''
        for zone_name, records in zones.items():
            if res['dns_name']+'.' in records:
                res['route53_name'] = records[res['dns_name']+'.']
                break
            elif res['dns_name'] in records:
                res['route53_name'] = records[res['dns_name']]
                break
        return res

    def updateItems(self, Items):
        for key, val in Items['EC2'].items():
            for region_name, instancesList in val.items():
                for instance in instancesList:
                    if instance['elb'] != '':
                        for region_name, elbsList in Items['ELB'][key].items():
                            for elb in elbsList:
                                if instance['id'] in elb['instances']:
                                    elb['instances_details'].append({'id':instance['id'], 'ip_address':instance['ip_address'], 'name':instance['name']})

    def getAllItems(self, aws_key, aws_secret, Items):
        res = {}
        regions = boto.ec2.elb.regions()
        for region in regions:
            if region.name in self.skipRegions:
                continue
            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            allELBs = conn.get_all_load_balancers()
            res[region.name] = []
            for item in allELBs:
                elbDict = self.resultDict(region.name, item, Items['Route53'])
                res[region.name].append(elbDict)
        return res

    def getData(self):
        ELBs = {}
        for credential in self.credentials:
            ELBs[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return ELBs
