from github import Github
import requests

# GitHub access token
ACCESS_TOKEN = 'Admin Token'

# GitHub repository information
REPO_OWNER = 'ofekharpaz'
REPO_NAME = 'varonis-home-exercise'

# Initialize GitHub instance
g = Github(ACCESS_TOKEN)

# Get repository object
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

# Configuration 1: Branch Protection Rules
def check_and_fix_branch_protection():
    print("Checking branch protection rules...")

    # Define critical branches
    critical_branches = ['master', 'main']

    for branch_name in critical_branches:
        branch = repo.get_branch(branch_name)
        if not branch.protected:
            print(f"Branch {branch_name} is not protected. Fixing...")
            branch.edit_protection(
                enforce_admins=True,
                dismiss_stale_reviews=True,
                require_code_owner_reviews=True,
                required_approving_review_count=1,
                allow_force_pushes=False,
                allow_deletions=False
            )
            print(f"Branch {branch_name} is now protected.")
        else:
            print(f"Branch {branch_name} is already protected.")

# Configuration: Access Control via Deploy Keys
def check_and_fix_deploy_keys():
    print("Checking access control settings via deploy keys...")

    deploy_keys = repo.get_keys()
    for deploy_key in deploy_keys:
        # Check permissions for each deploy key
        print(f"Deploy key {deploy_key.id}: {deploy_key.title}, Permissions:")
        if deploy_key.read_only:
            print("- Read only")
        else:
            print("- Read/Write")

# Configuration: Access Control via Collaborators


def _update_collaborator_permission(collaborator_username, permission):
    # URL for the collaborator endpoint
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/collaborators/{collaborator_username}"
    # Headers with authentication
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    }

    # Payload with permission level
    data = {"permission": permission}

    # Send PUT request to update collaborator permission
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 204:
        print("Collaborator permission updated successfully.")
    else:
        print("Failed to update collaborator permission. Status code:", response.status_code)
        print("Response:", response.text)


def check_and_fix_access_control():
    print("Checking access control settings for collaborators...")
    try:
        COLLABORATOR_USERNAME_TO_CHANGE = 'ofek-test-user'
        collaborators = repo.get_collaborators()
        for collaborator in collaborators:
            # Check access level for each collaborator
            if collaborator.login == COLLABORATOR_USERNAME_TO_CHANGE:
                _update_collaborator_permission(COLLABORATOR_USERNAME_TO_CHANGE, 'admin')
            print(f"Collaborator: {collaborator.login}, Access Level: {collaborator.permissions}")
        
    except Exception as e:
        print(f"Error occurred while retrieving collaborators: {str(e)}")

if __name__ == "__main__":
    # Execute checks and fixes
    check_and_fix_branch_protection()
    check_and_fix_deploy_keys()
    check_and_fix_access_control()
