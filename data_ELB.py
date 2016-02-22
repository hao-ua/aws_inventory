import boto.ec2.elb
import boto


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'ELB'
        self.Priority = 2
        self.show = True
        self.HeaderNames = ['Name', 'DNS name', 'Count', 'Route53 name']
        self.HeaderWidths = ['2', '6', '1', '4']
        self.HeaderKeys = ['name', 'dns_name', 'instances_count', 'route53_name']
        self.credentials = credentials
        self.Items = items
        self.skipRegions = []

    def result_dict(self, region, elb, zones):
        res = dict()
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

    def update_items(self, items):
        for key, val in items['EC2'].items():
            for instancesList in val.values():
                for instance in instancesList:
                    if instance['elb'] != '':
                        for elbsList in items['ELB'][key].values():
                            for elb in elbsList:
                                if instance['id'] in elb['instances']:
                                    elb['instances_details'].append({'id': instance['id'],
                                                                     'ip_address': instance['ip_address'],
                                                                     'name': instance['name']})

    def get_all_items(self, aws_key, aws_secret, items):
        res = {}
        regions = boto.ec2.elb.regions()
        for region in regions:
            if region.name in self.skipRegions:
                continue

            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            all_elbs = conn.get_all_load_balancers()
            res[region.name] = []
            for item in all_elbs:
                elb_dict = self.result_dict(region.name, item, items['Route53'])
                res[region.name].append(elb_dict)

        return res

    def get_data(self):
        elbs = {}
        for credential in self.credentials:
            elbs[credential[2]] = self.get_all_items(credential[0], credential[1], self.Items)

        return elbs
