import logging

from dateutil.parser import isoparse

logger = logging.getLogger(__name__)


def get_hubstaff_daily_report_table(client, date_):
    for report in get_hubstaff_daily_report(client=client, date_=date_):
        table = list(format_table(report))
        yield report['organization'], table


def format_table(report):
    timelog = report['timelog']
    all_projects = get_projects(timelog)
    yield ['user'] + all_projects
    for user_data in timelog:
        projects = user_data['projects']
        yield [user_data['user']] + [projects.get(project_name, '')
                                     for project_name in all_projects]


def get_projects(timelog):
    projects = set()
    for user_data in timelog:
        projects.update(user_data['projects'].keys())
    return list(projects)


def get_hubstaff_daily_report(client, date_):
    report_data = client.get_custom_report_by_member(start_date=date_,
                                                     end_date=date_)
    for organization_data in report_data['organizations']:
        yield {
            'organization': organization_data['name'],
            'timelog': list(get_user_organization_reports(
                date_, organization_data)),
        }


def get_user_organization_reports(date_, organization_data):
    for user in organization_data['users']:
        yield get_user_project_reports(date_, user)


def get_user_project_reports(date_, user_data):
    username = user_data['name']
    date_report = get_report_for_date(date_, user_data)
    if not date_report:
        logger.debug('No data of user %s on date %s', username, date_)
        return
    return {
        'user': username,
        'projects': {p['name']: p['duration'] for p in date_report['projects']},
    }


def get_report_for_date(required_date, user):
    for report in user['dates']:
        if isoparse(report['date']).date() == required_date:
            return report
