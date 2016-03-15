import boto.ec2
import boto.ec2.volume
import boto.ec2.snapshot


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'Volumes'
        self.Priority = 9
        self.show = True
        self.HeaderNames = ['ID', 'Attachment State', 'IOPS', 'Size', 'Create Time', 'Instance Id', 'Instance name']
        self.HeaderWidths = ['2', '2', '1', '1', '3', '2', '4']
        self.HeaderKeys = ['name', 'attachment_state', 'iops', 'size', 'create_time', 'instance_id', 'instance_name']
        self.credentials = credentials
        self.Items = items
        self.account = ''
        self.skipRegions = []

    def result_dict(self, volume):
        res = dict()
        res['name'] = volume.id
        res['attachment_state'] = volume.attachment_state()
        res['iops'] = str(volume.iops)
        res['size'] = str(volume.size)+'Gb'
        res['placement'] = volume.zone
        res['create_time'] = volume.create_time
        
        if res['attachment_state'] == 'attached':
            res['instance_id'] = volume.attach_data.instance_id
            for region in self.Items['EC2'][self.account].keys():
                for instanceDict in self.Items['EC2'][self.account][region]:
                    if res['instance_id'] == instanceDict['id']:
                        res['instance_name'] = instanceDict['name']
        else:
            res['instance_id'] = 'none'
            res['instance_name'] = 'none'

        return res

    def get_all_items(self, aws_key, aws_secret):
        result = dict()
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue

            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            volumes = conn.get_all_volumes()
            for volume in volumes:
                instance_dict = self.result_dict(volume)
                if region.name in result:
                    result[region.name].append(instance_dict)
                else:
                    result[region.name] = [instance_dict]

        return result

    def get_data(self):
        volumes = {}
        for credential in self.credentials:
            self.account = credential[2]
            volumes[credential[2]] = self.get_all_items(credential[0], credential[1])

        return volumes
