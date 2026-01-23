"""
Podio API client using requests.
Docs: https://developers.podio.com/
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.podio.com"


class PodioClient:
    def __init__(self):
        self.client_id = os.getenv("PODIO_CLIENT_ID")
        self.client_secret = os.getenv("PODIO_CLIENT_SECRET")
        self.username = os.getenv("PODIO_USERNAME")
        self.password = os.getenv("PODIO_PASSWORD")
        self.access_token = None
        self.refresh_token = None

    def authenticate(self):
        """Authenticate using password flow."""
        response = requests.post(
            f"{BASE_URL}/oauth/token",
            data={
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
            },
        )
        response.raise_for_status()
        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        return data

    def _headers(self):
        return {"Authorization": f"OAuth2 {self.access_token}"}

    def get(self, endpoint, params=None):
        """Make a GET request to the Podio API."""
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=self._headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        """Make a POST request to the Podio API."""
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=self._headers(),
            json=data,
        )
        response.raise_for_status()
        return response.json()

    # --- Convenience methods ---

    def get_organizations(self):
        """Get all organizations."""
        return self.get("/org/")

    def get_workspaces(self, org_id):
        """Get all workspaces in an organization."""
        return self.get(f"/org/{org_id}/space/")

    def get_apps(self, space_id):
        """Get all apps in a workspace."""
        return self.get(f"/app/space/{space_id}/")

    def get_items(self, app_id, limit=100, offset=0):
        """Get items from an app."""
        return self.post(f"/item/app/{app_id}/filter/", {
            "limit": limit,
            "offset": offset,
        })

    def get_item(self, item_id):
        """Get a single item by ID."""
        return self.get(f"/item/{item_id}")


def get_client():
    """Create and authenticate a Podio client."""
    client = PodioClient()
    client.authenticate()
    return client


if __name__ == "__main__":
    client = get_client()
    print("Authenticated successfully!\n")

    print("=== Organizations ===")
    orgs = client.get_organizations()
    for org in orgs:
        print(f"  {org['name']} (ID: {org['org_id']})")

    if orgs:
        print("\n=== Workspaces ===")
        for org in orgs:
            print(f"\n{org['name']}:")
            spaces = client.get_workspaces(org['org_id'])
            for space in spaces:
                print(f"  {space['name']} (ID: {space['space_id']})")

                # List apps in each workspace
                apps = client.get_apps(space['space_id'])
                for app in apps:
                    print(f"    - {app['config']['name']} (ID: {app['app_id']})")
