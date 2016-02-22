import boto
import boto.rds
import boto.ec2


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'RDS'
        self.Priority = 5
        self.show = True
        self.HeaderNames = ['Name', 'Endpoint', 'Allocated storage', 'Instance class', 'Status']
        self.HeaderWidths = ['2', '6', '2', '2', '2']
        self.HeaderKeys = ['name', 'endpoint', 'allocated_storage', 'instance_class', 'status']
        self.credentials = credentials
        self.Items = items
        self.skipRegions = []

    def result_dict(self, db_instance):
        res = dict()
        res['name'] = db_instance.id
        res['endpoint'] = ':'.join([db_instance.endpoint[0], str(db_instance.endpoint[1])])
        res['allocated_storage'] = ''.join([str(db_instance.allocated_storage), 'Gb'])
        res['instance_class'] = db_instance.instance_class
        res['status'] = db_instance.status
        return res

    def get_all_items(self, aws_key, aws_secret, items):
        result = dict()
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue

            conn = boto.rds.connect_to_region(region.name, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            db_instances = conn.get_all_dbinstances()
            result[region.name] = []
            for db_instance in db_instances:
                result[region.name].append(self.result_dict(db_instance))

        return result

    def get_data(self):
        rdses = dict()
        for credential in self.credentials:
            rdses[credential[2]] = self.get_all_items(credential[0], credential[1], self.Items)
        return rdses
