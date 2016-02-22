import boto.ec2
import boto.ec2.volume
import boto.ec2.snapshot


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'Snapshots'
        self.Priority = 10
        self.show = True
        self.HeaderNames = ['ID', 'Status', 'Size', 'Volume ID', 'Volume exists', 'Owner ID', 'Image ID']
        self.HeaderWidths = ['2', '2', '1', '2', '1', '4', '4']
        self.HeaderKeys = ['name', 'status', 'size', 'volume_id', 'volume_exists', 'owner_id', 'image_id']
        self.credentials = credentials
        self.Items = items
        self.account = ''
        self.skipRegions = []

    @staticmethod
    def result_dict(snapshot, volumes, images):
        res = dict()
        res['name'] = snapshot.id
        res['owner_id'] = snapshot.owner_id
        res['owner_alias'] = snapshot.owner_alias
        res['status'] = snapshot.status
        res['volume_id'] = snapshot.volume_id
        res['size'] = str(snapshot.volume_size)+'Gb'
        res['placement'] = snapshot.region
        res['volume_exists'] = 'No'
        res['image_id'] = ''
        for volume in volumes:
            if volume.id == snapshot.volume_id:
                res['volume_exists'] = 'Yes'
                break

        for image in images:
            for val in image.block_device_mapping.values():
                if snapshot.id == val.snapshot_id:
                    res['volume_exists'] = 'Yes'
                    res['image_id'] = image.id
                    break

        return res

    def get_all_items(self, aws_key, aws_secret):
        result = dict()
        regions = boto.ec2.regions(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        for region in regions:
            if region.name in self.skipRegions:
                continue

            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            volumes = conn.get_all_volumes()
            snapshots = conn.get_all_snapshots(owner='self')
            images = conn.get_all_images(owners=['self'])
            for snapshot in snapshots:
                instance_dict = self.result_dict(snapshot, volumes, images)
                if instance_dict == {}:
                    continue

                if region.name in result:
                    result[region.name].append(instance_dict)
                else:
                    result[region.name] = [instance_dict]

        return result

    def get_data(self):
        volumes = dict()
        for credential in self.credentials:
            self.account = credential[2]
            volumes[credential[2]] = self.get_all_items(credential[0], credential[1])

        return volumes
