import base64
import os
from github import Github
from github import InputGitTreeElement

user = os.environ.get("GITHUB_USER")
password =  os.environ.get("GITHUB_PASSWORD")
g = Github(user,password)
repo = g.get_user().get_repo('DiscordBotMS2NewsUpdater')
file_list = [
  'last_update.txt'
]

file_names = [
  'last_update.txt'    
]

def git_commit():
    commit_message = 'News link update'
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'):
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
