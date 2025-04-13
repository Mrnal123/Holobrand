import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional

# Load environment variables
load_dotenv()

class GitHubIntegration:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def check_token_validity(self) -> bool:
        """Check if the GitHub token is valid"""
        if not self.token or self.token == "your_github_personal_access_token_here":
            return False
            
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_repositories(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get repositories for the authenticated user or a specific user"""
        try:
            if username:
                url = f"{self.base_url}/users/{username}/repos"
            else:
                url = f"{self.base_url}/user/repos"
                
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Error fetching repositories: {str(e)}")
            return []
    
    def get_repository_details(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get details for a specific repository"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            print(f"Error fetching repository details: {str(e)}")
            return {}
    
    def search_repositories(self, query: str) -> List[Dict[str, Any]]:
        """Search for repositories based on a query"""
        try:
            url = f"{self.base_url}/search/repositories?q={query}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get("items", [])
            else:
                return []
        except Exception as e:
            print(f"Error searching repositories: {str(e)}")
            return []