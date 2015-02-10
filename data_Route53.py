import boto
import boto.route53

class data:
    def __init__(self, credentials, Items):
        self.Priority = 0
        self.Name = 'Route53'
        self.Items = Items
        self.show = False
        self.credentials = credentials
        self.skipRegions = []

    def getAllItems(self, aws_key, aws_secret, Items):
        result = {}
        zoneParams = {}
        conn = boto.route53.connection.Route53Connection(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        res = conn.get_all_hosted_zones()
        for item in res['ListHostedZonesResponse']['HostedZones']:
            zoneParams[item['Name']] = item['Id'].split('/')[-1]
        for zone_name,zone_id in zoneParams.items():
            zone = {}
            tmpRec = conn.get_all_rrsets(zone_id, name=zone_name)
            for rec in tmpRec:
                if rec.type == 'A' or rec.type == 'CNAME':
                    if len(rec.resource_records) != 0:
                        for ip in rec.resource_records:
                            if ip not in zone:
                                zone[ip] = rec.name
                            else:
                                zone[ip] = zone[ip] + " " + rec.name
                    else:
                        if rec.alias_dns_name not in zone:
                            zone[rec.alias_dns_name] = rec.name
                        else:
                            zone[rec.alias_dns_name] = zone[rec.alias_dns_name] + " " + rec.name
            result[zone_name] = zone
        return result

    def getData(self):
        zones = {}
        for credential in self.credentials:
            zone = self.getAllItems(credential[0], credential[1], self.Items)
            zones.update(zone)
        return zones
