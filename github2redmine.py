import csv
import json
from collections import namedtuple
import requests   # fades


redmine_properties = ['title', 'description', 'status']
RedmineIssue = namedtuple('RedmineIssue', redmine_properties)


api_key = "replace me"
user = "InvGate"
repo = "neo-assets-front"


def fetch_github_issues(issue_url=None):
    if issue_url is None:
        issue_url = "https://api.github.com/repos/{}/{}/issues?access_token={}&per_page=1000&page=1".format(user, repo, api_key)
        write_csv_header()
    data = requests.get(issue_url)

    next_url = data.links.get('next')

    export_issues_to_csv(data.json())

    if next_url is not None:
        fetch_github_issues(next_url.get('url'))


def write_csv_header():
    with open('issues.csv', 'a') as csvfile:
        issue_writer = csv.writer(csvfile, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)

        issue_writer.writerow(redmine_properties)


def export_issues_to_csv(issues_filepath):
    with open('issues.csv', 'a') as csvfile:
        issue_writer = csv.writer(csvfile, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for redmine_issue in parse_github_issues(issues_filepath):
            print(redmine_issue)
            issue_writer.writerow(redmine_issue)


def parse_github_issues(issues_data):
    for github_issue in issues_data:
        if not exclude_issue(github_issue):
            redmine_issue = get_redmine_issue(github_issue)
            yield redmine_issue


def exclude_issue(github_issue_data):
    if 'pull_request' in github_issue_data:
        return True
    return False


def get_redmine_issue(github_issue_data):
    title = github_issue_data['title'].encode('utf-8') if github_issue_data['title'] else ''
    description = get_redmine_description(github_issue_data)
    status = github_issue_data['state'].encode('utf-8') if github_issue_data['state'] else ''
    redmine_issue = RedmineIssue(title=title,
                                 description=description,
                                 status=status)
    return redmine_issue


def get_redmine_description(github_issue_data):
    description = github_issue_data['body'].encode('utf-8') if github_issue_data['body'] else ''
    comments = fetch_github_comments(github_issue_data)
    return "{}{}".format(description, comments)


def fetch_github_comments(github_issue_data):
    comments = ""
    comments_url = github_issue_data['comments_url']
    request = requests.get(comments_url+'?access_token='+api_key)
    if request.status_code == 200:
        for comment in request.json():
            comments = comments + "\n" + comment["body"]

    return comments.encode('utf-8') if comments else ''

def main():
    fetch_github_issues()


if __name__ == '__main__':
    main()
