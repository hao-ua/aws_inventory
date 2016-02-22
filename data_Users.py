import boto.iam


class Data(object):
    def __init__(self, credentials, items):
        self.Name = 'Users'
        self.Priority = 7
        self.credentials = credentials
        self.Items = items
        self.show = True
        self.HeaderNames = ['User name', 'Groups']
        self.HeaderWidths = ['4', '6']
        self.HeaderKeys = ['name', 'groups']
        self.skipRegions = []

    @staticmethod
    def result_dict(item, groups):
        res = dict()
        user_groups = groups['list_groups_for_user_response']['list_groups_for_user_result']['groups']
        res['name'] = item['user_name']
        groups_list = []
        for group in user_groups:
            groups_list.append(group['group_name'])

        res['groups'] = ' '.join(groups_list)
        return res

    def get_all_items(self, aws_key, aws_secret):
        result = dict()
        result['Global'] = []
        regions = boto.iam.regions()
        conn = regions[0].connect(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        users = conn.get_all_users()
        for user in users['list_users_response']['list_users_result']['users']:
            groups = conn.get_groups_for_user(user['user_name'])
            user_dict = self.result_dict(user, groups)
            result['Global'].append(user_dict)

        return result

    def get_data(self):
        ecs = {}
        for credential in self.credentials:
            ecs[credential[2]] = self.get_all_items(credential[0], credential[1])

        return ecs
