import os
import requests
import argparse
from mdcal import update_calendar


def get_issue(issue_number=None):
    try:
        if issue_number is None:
            issue_number = os.getenv("ISSUE_NUMBER")
        repo_name = os.getenv("GITHUB_REPOSITORY")
        gh_token = os.getenv("GH_TOKEN")

        headers = {"Authorization": f"token {gh_token}"}
        api_url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}"

        response = requests.get(api_url, headers=headers)
        issue = response.json()

        print(api_url)
        print(headers)
        print(issue)

    except Exception as e:
        print(f"Error in get_issue: {e}")
        return None

    return issue


def update_records(issue, issue_number=None):
    if issue_number is None:
        issue_number = os.getenv("ISSUE_NUMBER")

    issue_title = issue["title"]
    issue_labels = ["`" + label["name"] + "`" for label in issue["labels"]]
    issue_link = issue["html_url"]

    with open("README.md", "r") as file:
        lines = file.readlines()

        table_start_index = None
        existing_issue_index = None

        for i in range(len(lines)):
            if lines[i].strip() == "|#|Title|Tag|Date|":
                table_start_index = i + 2
            if lines[i].strip().startswith(f"|{issue_number}|") and table_start_index:
                existing_issue_index = i
            if existing_issue_index:
                break

        new_line = f"|{issue_number}|[{issue_title}]({issue_link})|{' '.join(issue_labels)}|{issue['created_at']}|\n"
        if existing_issue_index is not None:
            lines[existing_issue_index] = new_line
        else:
            lines.insert(table_start_index, new_line)
    with open("README.md", "w") as file:
        file.writelines(lines)

    return "Successfully updated Records of README.md"

def update_star(issue):
    created_at_str = issue['created_at']
    date_str = created_at_str.split("T")[0]
    year, month, day = map(int, date_str.split("-"))
    return update_calendar(year, month, day)

def get_comments(issue_number=None):
    try:
        if issue_number is None:
            issue_number = os.getenv("ISSUE_NUMBER")
            
        repo_name = os.getenv("GITHUB_REPOSITORY")
        gh_token = os.getenv("GH_TOKEN")

        headers = {"Authorization": f"token {gh_token}"}
        comments_api_url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}/comments"

        comments_response = requests.get(comments_api_url, headers=headers)
        comments = comments_response.json()

    except Exception as e:
        print(f"Error in get_comments: {e}")
        return []

    return comments

def backup_issue_as_md(issue, issue_number):
    try:
        if issue_number is None:
            issue_number = os.getenv("ISSUE_NUMBER")
            
        issue_title = issue["title"]
        issue_body = issue['body']
        issue_labels = ["`" + label['name'] + "`" for label in issue['labels']]
        issue_link = issue['html_url']
        issue_date = issue['created_at']

        comments = get_comments(issue_number)

        if not os.path.exists("backup"):
            os.mkdir("backup")

        with open(f"backup/{issue_number}#{issue_title}.md", "w") as file:
            file.write("# " + issue_title + "\n\n")
            file.write(issue_body + "\n\n")
            file.write("---\n\n")
            file.write("* Link: " + issue_link + "\n")
            file.write("* Labels: " + ', '.join(issue_labels) + "\n")
            file.write("* Creation Date: " + issue_date + "\n")
            for i, comment in enumerate(comments, start=1):
                file.write(f"\n---\n\n") 
                file.write(comment['body'])
                file.write("\n\n*\n")

    except Exception as e:
        print(f"Error in backup_issue_as_md: {e}")
        return "Backup failed"
      
    return "Successfully backup records"

def main(issue_number):
    try:
        issue = get_issue(issue_number)
        if issue is not None:
            print(update_records(issue, issue_number))
            print(update_star(issue))
            print(backup_issue_as_md(issue, issue_number))
        else:
            print("Issue could not be retrieved.")
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--issue_number", help="issue_number", default=None, required=False
        )
        args = parser.parse_args()
        main(args.issue_number)
    except Exception as e:
        print(f"Error: {e}")
