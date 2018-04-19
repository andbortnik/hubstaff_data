#!/usr/bin/env python3
import argparse
import configparser
import os
from datetime import date, timedelta

from dateutil.parser import isoparse

from html_renderer import render_html_table
from hubstaff.hubstaff_client import HubstaffClient
from hubstaff.utils import get_hubstaff_daily_report_table


def get_hubstaff_report_and_render_html(client, date_):
    for organization_name, table in get_hubstaff_daily_report_table(client,
                                                                    date_):
        yield organization_name, render_html_table(table)


def get_hubstaff_report_and_save_html(client, date_):
    for organization_name, html in get_hubstaff_report_and_render_html(client,
                                                                       date_):
        filename = '{}_{}.html'.format(date_, organization_name)
        with open(filename, 'w') as f:
            f.write(html)


def parse_config_file(file_path):
    config = configparser.ConfigParser()
    with open(file_path) as f:
        config.read_file(f)
        return config


def get_options():
    yesterday = date.today() - timedelta(days=1)
    parser = argparse.ArgumentParser(description='Hubstaff data')
    parser.add_argument('--config', '-c', default='hubstaff_data.ini',
                        help='Config file path')
    parser.add_argument('--date', '-d', default=yesterday.isoformat(),
                        type=lambda d: isoparse(d).date(),
                        help='Report date in YYYY-MM-DD format')
    validate_options(parser)
    return parser.parse_args()


def validate_options(parser):
    options = parser.parse_args()
    if not os.path.exists(options.config):
        parser.error('Config file does not exist')


def main():
    options = get_options()
    hubstaff_config = parse_config_file(options.config)
    client = HubstaffClient(**dict(hubstaff_config['hubstaff']))
    get_hubstaff_report_and_save_html(client, options.date)


if __name__ == '__main__':
    main()
