import boto
import boto.s3

class data:
    def __init__(self, credentials, Items):
        self.Name = 'S3'
        self.Priority = 1
        self.show = True
        self.HeaderNames = ['Name', 'Website endpoint', 'Route53 name']
        self.HeaderWidths = ['4', '7', '3']
        self.HeaderKeys = ['name', 'website_endpoint', 'route53_name']
        self.credentials = credentials
        self.Items = Items
        self.skipRegions = []

    def resultDict(self, bucket, zones):
        res = {}
        res['name'] = bucket.name
        res['website_endpoint'] = bucket.get_website_endpoint()
        res['route53_name'] = ''
        try:
            res['website_conf'] = bucket.get_website_configuration()
        except:
            res['website_conf'] = None
        try:
            res['tags'] = bucket.get_tags()
        except:
            res['tags'] = []
        if res['website_conf']:
            for zone_name, records in zones.items():
                if res['website_endpoint'] in records:
                    res['route53_name'] = records[res['website_endpoint']]
                    break
                elif res['website_endpoint']+'.' in records:
                    res['route53_name'] = records[res['website_endpoint']+'.']
                    break
        return res

    def getAllItems(self, aws_key, aws_secret, Items):
        result = {}
        result['Global'] = []
        conn = boto.connect_s3(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        buckets = conn.get_all_buckets()
        for bucket in buckets:
            result['Global'].append(self.resultDict(bucket, Items['Route53']))
        return result

    def getData(self):
        S3 = {}
        for credential in self.credentials:
            S3[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return S3
