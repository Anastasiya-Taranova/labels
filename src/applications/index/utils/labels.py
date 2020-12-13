import requests
from utils import get_setting

token = get_setting("GITHUB_ACCESS_TOKEN")

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}",
}


def create_label(name_label, description, color, owner, repo):
    data = {
        "name": f"{name_label}",
        "description": f"{description}",
        "color": f"{color}",
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    response = requests.post(url, json=data, headers=headers)
    return response


def list_labels(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    response = requests.get(url, headers=headers).json()
    return response


def view_label(owner, repo, name_label):
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{name_label}"
    response = requests.get(url, headers=headers).json()
    return response


def update_label(owner, repo, name_label):
    data = {"new_name": "xxxx", "description": "xxxxx", "color": "b01f26"}
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{name_label}"
    response = requests.patch(url, json=data, headers=headers)
    return response


def delete_label(owner, repo, name_label):
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{name_label}"
    response = requests.delete(url, headers=headers).json()
    return response


def list_labels_for_issue(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
    response = requests.get(url, headers=headers).json()
    return response


def add_label_for_issue(name_label, owner, repo, issue_number):
    data = {
        "labels": [f"{name_label}"],
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
    response = requests.post(url, json=data, headers=headers)
    return response


def remove_label_from_issue(owner, repo, issue_number, name_label):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels/{name_label}"
    response = requests.delete(url, headers=headers).json()
    return response


def set_label_for_issue(name_label, owner, repo, issue_number):
    """ Removes any previous labels and sets the new labels for an issue """

    data = {
        "labels": [f"{name_label}"],
    }
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
    response = requests.put(url, json=data, headers=headers).json()
    return response


def remove_all_labels_from_issue(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
    response = requests.delete(url, headers=headers).json()
    return response
