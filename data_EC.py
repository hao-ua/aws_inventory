import boto.elasticache


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'EC'
        self.Priority = 6
        self.show = True
        self.HeaderNames = ['Name', 'Endpoint', 'Status', 'Node type', 'Maintenance', 'Engine']
        self.HeaderWidths = ['2', '6', '1', '2', '3', '2']
        self.HeaderKeys = ['name', 'endpoint', 'status', 'type', 'maintenance', 'engine']
        self.credentials = credentials
        self.Items = items
        self.skipRegions = []

    def result_dict(self, item):
        res = dict()
        res['name'] = item['CacheClusterId']
        res['engine'] = item['Engine']
        if item['ConfigurationEndpoint'] is None:
            res['endpoint'] = ""
        else:
            res['endpoint'] = ''.join([item['ConfigurationEndpoint']['Address'], ':',
                                       str(item['ConfigurationEndpoint']['Port'])])
        res['status'] = item['CacheClusterStatus']
        res['type'] = item['CacheNodeType']
        res['placement'] = item['PreferredAvailabilityZone']
        res['maintenance'] = item['PreferredMaintenanceWindow']
        return res

    def get_all_items(self, aws_key, aws_secret, items):
        result = {}
        regions = boto.elasticache.regions()
        for region in regions:
            if region.name in self.skipRegions:
                continue 
            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            cache_clusters = conn.describe_cache_clusters()['DescribeCacheClustersResponse']\
                ['DescribeCacheClustersResult']['CacheClusters']
            for cluster in cache_clusters:
                cluster_dict = self.result_dict(cluster)
                if cluster_dict['placement'] in result:
                    result[cluster_dict['placement']].append(cluster_dict)
                else:
                    result[cluster_dict['placement']] = [cluster_dict]
        return result

    def get_data(self):
        ecs = {}
        for credential in self.credentials:
            ecs[credential[2]] = self.get_all_items(credential[0], credential[1], self.Items)
        return ecs
