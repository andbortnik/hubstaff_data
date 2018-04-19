from urllib.parse import urljoin

import requests


class HubstaffClient(object):
    BASE_API_URL = 'https://api.hubstaff.com/'
    API_V1_URL = urljoin(BASE_API_URL, 'v1/')
    AUTH_URL = urljoin(API_V1_URL, 'auth/')
    CUSTOM_REPORTS_URL = urljoin(API_V1_URL, 'custom/')
    CUSTOM_REPORTS_BY_MEMBER_URL = urljoin(CUSTOM_REPORTS_URL, 'by_member/')
    CUSTOM_REPORTS_BY_MEMBER_TEAM_URL = urljoin(
        CUSTOM_REPORTS_BY_MEMBER_URL, 'team/')

    def __init__(self, app_token, email, password):
        self.app_token = app_token
        self.email = email
        self.password = password
        self.auth_token = None

    def authenticate(self):
        payload = {
            'email': self.email,
            'password': self.password,
        }
        headers = {'App-Token': self.app_token}
        response = requests.post(self.AUTH_URL, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_auth_headers(self):
        return {
            'App-Token': self.app_token,
            'Auth-Token': self.get_auth_token(),
        }

    def get_auth_token(self):
        if not self.auth_token:
            self.auth_token = self.authenticate()['user']['auth_token']
        return self.auth_token

    def get_custom_report_by_member(self, start_date, end_date,
                                    organizations=(), projects=(),
                                    users=None, show_tasks=False,
                                    show_notes=False, show_activity=False,
                                    include_archived=False):
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'organizations': organizations,
            'projects': projects,
            'users': users,
            'show_tasks': show_tasks,
            'show_notes': show_notes,
            'show_activity': show_activity,
            'include_archived': include_archived,
        }
        response = requests.get(self.CUSTOM_REPORTS_BY_MEMBER_TEAM_URL,
                                headers=self.get_auth_headers(),
                                params=params)
        response.raise_for_status()
        return response.json()
