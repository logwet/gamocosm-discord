import json

import requests


class Server:
    """API Wrapper Object that connects to one server"""

    def __init__(self, server_id, api_key):
        self.server_id = server_id
        self.api_key = api_key
        self.apiurl = f"https://gamocosm.com/servers/{server_id}/api/{api_key}/"
        self.headers = {}

    def _get(self, endpoint):
        """Sends a GET request to the specifed endpoint"""
        response = requests.get(self.apiurl + endpoint, headers=self.headers)
        return self._parse(response)

    def _post(self, endpoint, data):
        """Sends a POST request to the specified endpoint"""
        response = requests.post(self.apiurl + endpoint, data, headers=self.headers)
        return self._parse(response)

    def _parse(self, response):
        """Parses JSON response from endpoint"""
        response.raise_for_status()
        return json.loads(response.content.decode('utf8'))

    def _status(self):
        """Sends GET request to get raw status of server"""
        return self._get("status")

    def start(self):
        """Sends POST request to start the DO server"""
        return self._post("start", "")['error']

    def stop(self):
        """Sends POST request to stop the DO server"""
        return self._post("stop", "")['error']

    def reboot(self):
        """Sends POST request to reboot the DO server"""
        return self._post("reboot", "")['error']

    def pause(self):
        """Sends POST request to stop the Minecraft server"""
        return self._post("pause", "")['error']

    def resume(self):
        """Sends POST request to start the Minecraft server"""
        return self._post("resume", "")['error']

    def backup(self):
        """Sends POST request to remotely backup the world of the server"""
        return self._post("backup", "")['error']

    def online(self):
        """Is the DO server online?"""
        return self._status()['server']

    def pending(self):
        """Are there any pending operations?"""
        return self._status()['status']

    def minecraft(self):
        """Is the Minecraft server running?"""
        return self._status()['minecraft']

    def domain(self):
        """Whats the Cloudflare hostname of the server"""
        return self._status()['domain']

    def ip(self):
        """Has an ip been assigned?"""
        return self._status()['ip']

    def download(self):
        """Grabs a download link for the world"""
        return self._status()['download']
