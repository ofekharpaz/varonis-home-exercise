from github import Github

# GitHub access token
ACCESS_TOKEN = 'Admin Token'

# GitHub repository information
REPO_OWNER = 'ofekharpaz'
REPO_NAME = 'varonis-home-exercise'

def exploit_unprotected_branch():
    print("Exploiting unprotected branch...")
    
    # Initialize GitHub instance
    g = Github(ACCESS_TOKEN)
    
    # Get repository object
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    # Define the name of the unprotected branch to exploit
    branch_name = 'main'  # Change this to the name of your unprotected branch
    
    # Get the unprotected branch
    branch = repo.get_branch(branch_name)
    
    # Perform unauthorized changes (e.g., create a new file)
    file_content = "Malicious content"
    file_path = "exploit.txt"
    commit_message = "Exploiting unprotected branch"
    
    try:
        # Create a new file in the unprotected branch
        repo.create_file(file_path, commit_message, file_content, branch_name)
        print("Unauthorized changes made successfully.")
    except Exception as e:
        print(f"Failed to exploit unprotected branch: {e}")

if __name__ == "__main__":
    exploit_unprotected_branch()
