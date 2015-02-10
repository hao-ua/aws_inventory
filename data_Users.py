import boto.iam

class data:
    def __init__(self, credentials, Items):
        self.Name = 'Users'
        self.Priority = 7
        self.credentials = credentials
        self.Items = Items
        self.show = True
        self.HeaderNames = ['User name', 'Groups']
        self.HeaderWidths = ['4', '6']
        self.HeaderKeys = ['name', 'groups']
        self.skipRegions = []

    def resultDict(self, item, groups):
        res = {}
        userGroups = groups['list_groups_for_user_response']['list_groups_for_user_result']['groups']
        res['name'] = item['user_name']
        groupsList = []
        for group in userGroups:
            groupsList.append(group['group_name'])
        res['groups'] = ' '.join(groupsList)
        return res

    def getAllItems(self, aws_key, aws_secret, Items):
        result = {}
        result['Global'] = []
        regions = boto.iam.regions()
        conn = regions[0].connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        users = conn.get_all_users()
        for user in users['list_users_response']['list_users_result']['users']:
            groups = conn.get_groups_for_user(user['user_name'])
            userDict = self.resultDict(user, groups)
            result['Global'].append(userDict)
        return result

    def getData(self):
        ECs = {}
        for credential in self.credentials:
            ECs[credential[2]] = self.getAllItems(credential[0], credential[1], self.Items)
        return ECs
