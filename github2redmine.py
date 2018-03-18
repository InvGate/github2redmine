import csv
import json
from collections import namedtuple
import requests   # fades


redmine_properties = ['title', 'description', 'status']
RedmineIssue = namedtuple('RedmineIssue', redmine_properties)


def export_issues_to_csv(issues_filepath):
    with open('issues.csv', 'w', newline='') as csvfile:
        issue_writer = csv.writer(csvfile, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        issue_writer.writerow(redmine_properties)

        for redmine_issue in parse_github_issues(issues_filepath):
            print(redmine_issue)
            issue_writer.writerow(redmine_issue)


def parse_github_issues(issues_filepath):
    with open(issues_filepath, 'r') as issues_file:
        issues_data = json.load(issues_file)
    
    for github_issue in issues_data:
        if not exclude_issue(github_issue):
            redmine_issue = get_redmine_issue(github_issue)
            yield redmine_issue

def exclude_issue(github_issue_data):
    if 'pull_request' in github_issue_data:
        return True
    return False

def get_redmine_issue(github_issue_data):
    redmine_issue = RedmineIssue(title=github_issue_data['title'],
                                 description=github_issue_data['body'],
                                 status=github_issue_data['state'])
    return redmine_issue


def main():
    export_issues_to_csv('github_issues.json')


if __name__ == '__main__':
    main()
