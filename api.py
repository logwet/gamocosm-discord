import json
import requests

class Server:
    def __init__(self, server_id, api_key):
        self.server_id = server_id
        self.api_key = api_key
        self.apiurl = f"https://gamocosm.com/servers/{server_id}/api/{api_key}/"
        self.headers = {}
        self.domain = self._status()['domain']
    def _get(self, endpoint):
        response = requests.get(self.apiurl+endpoint, headers=self.headers)
        return self._parse(response)
    def _post(self, endpoint, data):
        response = requests.post(self.apiurl+endpoint, data, headers=self.headers)
        return self._parse(response)
    def _parse(self, response):
        response.raise_for_status()
        return json.loads(response.content.decode('utf8'))
    def _status(self):
        return self._get("status")
    def start(self):
        return self._post("start", "")['error']
    def stop(self):
        return self._post("stop", "")['error']
    def reboot(self):
        return self._post("reboot", "")['error']
    def pause(self):
        return self._post("pause", "")['error']
    def resume(self):
        return self._post("resume", "")['error']
    def backup(self):
        return self._post("backup", "")['error']
    def online(self):
        return self._status()['server']
    def pending(self):
        return self._status()['status']
    def minecraft(self):
        return self._status()['minecraft']
    def ip(self):
        return self._status()['ip']
    def download(self):
        return self._status()['download']
