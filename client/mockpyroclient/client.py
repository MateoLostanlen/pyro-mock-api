import io

import requests
from mockpyroclient.utils import convertToNumber


class Client:
    def __init__(
        self, api_url: str, credentials_login: str, credentials_password: str
    ) -> None:
        self.api = api_url
        self.device_id = convertToNumber(credentials_login)

    def heartbeat(self):

        url = f"{self.api}/device/heartbeat/{self.device_id}"
        return requests.put(url)

    def create_media_from_device(self):

        url = f"{self.api}/device/create_media_from_device/{self.device_id}"
        return requests.post(url)

    def send_alert_from_device(self, latitude, longitude, media_id):

        url = f"{self.api}/device/send_alert_from_device/{media_id}"
        return requests.post(url)

    def upload_media(self, media_id, media_data):

        url = f"{self.api}/device/upload_media/{media_id}"
        return requests.post(url, files={"file": io.BytesIO(media_data)})
