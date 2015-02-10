import boto
import boto.rds
import boto.ec2

class data:
    def __init__(self, credentials, Items):
        self.Name = 'RDS'
        self.Priority = 5
        self.show = True
        self.HeaderNames = ['Name', 'Endpoint', 'Allocated storage', 'Instance class', 'Status']
        self.HeaderWidths = ['2', '6', '2', '2', '2']
        self.HeaderKeys = ['name','endpoint','allocated_storage','instance_class', 'status']
        self.credentials = credentials
        self.Items = Items
        self.skipRegions = []

    def resultDict(self, dbInstance):
        res = {}
        res['name'] = dbInstance.id
        res['endpoint'] = ':'.join([dbInstance.endpoint[0], str(dbInstance.endpoint[1])])
        res['allocated_storage'] = ''.join([str(dbInstance.allocated_storage),'Gb'])
        res['instance_class'] = dbInstance.instance_class
        res['status'] = dbInstance.status
        return res

    def getAllItems(self, aws_key, aws_secret, Items):
        result = {}
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue            
            conn = boto.rds.connect_to_region(region.name, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            dbInstances = conn.get_all_dbinstances()
            result[region.name] = []
            for dbInstance in dbInstances:
                result[region.name].append(self.resultDict(dbInstance))
        return result

    def getData(self):
        rdses = {}
        for credential in self.credentials:
            rdses[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return rdses
