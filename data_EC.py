import boto.elasticache

class data:
    def __init__(self, credentials, Items):
        self.Name = 'EC'
        self.Priority = 6
        self.show = True
        self.HeaderNames = ['Name', 'Endpoint', 'Status', 'Node type', 'Maintenance', 'Engine']
        self.HeaderWidths = ['2', '6', '1', '2', '3', '2']
        self.HeaderKeys = ['name', 'endpoint', 'status', 'type', 'maintenance', 'engine']
        self.credentials = credentials
        self.Items = Items
        self.skipRegions = []

    def resultDict(self, item):
        res = {}
        res['name'] = item['CacheClusterId']
        res['engine'] = item['Engine']
        if item['ConfigurationEndpoint'] == None:
            res['endpoint'] = ""
        else:
            res['endpoint'] = ''.join([item['ConfigurationEndpoint']['Address'], ':', str(item['ConfigurationEndpoint']['Port'])])
        res['status'] = item['CacheClusterStatus']
        res['type'] = item['CacheNodeType']
        res['placement'] = item['PreferredAvailabilityZone']
        res['maintenance'] = item['PreferredMaintenanceWindow']
        return res

    def getAllItems(self, aws_key, aws_secret, Items):
        result = {}
        regions = boto.elasticache.regions()
        for region in regions:
            if region.name in self.skipRegions:
                continue 
            conn = region.connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
            cacheClusters = conn.describe_cache_clusters()['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters']
            for cluster in cacheClusters:
                clusterDict = self.resultDict(cluster)
                if clusterDict['placement'] in result:
                    result[clusterDict['placement']].append(clusterDict)
                else:
                    result[clusterDict['placement']] = [clusterDict]
        return result

    def getData(self):
        ECs = {}
        for credential in self.credentials:
            ECs[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return ECs
