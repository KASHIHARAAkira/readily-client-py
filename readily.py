#!/usr/bin/env python3

from array import array
from copyreg import constructor
import json
import logging
import urllib.request
import urllib.error
import time

class Readily:
    """
    This class includes methods to upload data to Readily(https://readily.online).
    You need authorized information(access token and refresh token) is issued from Readily.
    """

    HOST = "https://api.readily.online"
    HEADER = {"Content-Type": "application/json"}

    def __init__(self, path_token, ti = 300000):
        """
        Initialization function.
        Parameters
        ----------
        path_token : str
            The path of credential includes access_token, refresh_token and expiry_date
        ti : int (Optional)
            The time interval to upload data. This is used to estimate when access_token will be expired.
        """
        file = open(path_token)
        data = file.read()
        file.close()
        self.cred = json.loads(data)
        self.access_token = self.cred["access_token"]
        self.refresh_token = self.cred["refresh_token"]
        self.expiry_date = self.cred["expiry_date"]
        self.ti = ti
        self.path_token = path_token
        
    def _refresh_access_token(self):
        """
        Refresh access_token.
        Save new access_token and expiry_date to credential file (overwrite).
        """
        data = {"refresh_token": self.cred["refresh_token"]}
        request = urllib.request.Request(f"{self.HOST}/refresh_token", headers=self.HEADER,data=json.dumps(data).encode("utf-8"))
        try:
            with urllib.request.urlopen(request, timeout=1) as response:
                response_data = json.loads(response.read())
            logging.info(response_data)
            self.access_token = response_data["access_token"]
            self.expiry_date = response_data["expiry_at"]
            self._update_cred()
        except urllib.error.HTTPError as e:
            logging.exception(
                f'Server returned error: '
                f'status = {e.code} reason = {e.reason}'
            )
        except urllib.error.URLError as e:
            logging.exception(
                f'Handler returned error: '
                f'reason = {e.reason}'
            )

    def _update_cred(self):
        """
        Update credential file. Overwrite new credential information(access_token and expiry_date) to credential file.
        """
        file = open(self.path_token, "w")
        self.cred["access_token"] = self.access_token
        self.cred["expiry_date"] = self.expiry_date
        file.write(json.dumps(self.cred))
        file.close()

    def _check_access_token_expired(self):
        """
        Check access_token which will be expired or not.
        """
        if int(time.time()*1000) + self.ti > self.expiry_date:
            self._refresh_access_token()
        else:
            pass

    def put(self, data, chart_id):
        """
        This function only put data to spreadsheet via Readily WITHOUT check access_token expired.
        Parameters
        ----------
        data : array
            Upload data. Example; [[3.4, 2, 10.1],[4, 3, 2]]
        chart_id : str
            You get chart_id from Readily after sign in. 
        """
        data = {"access_token": self.access_token, "data": data}
        request = urllib.request.Request(f"{self.HOST}/upload?chartId={chart_id}", headers=self.HEADER,data=json.dumps(data).encode("utf-8"))
        try:
            with urllib.request.urlopen(request, timeout=1) as response:
                response_data = json.loads(response.read())
            logging.info(response_data)
            return response_data
        except urllib.error.HTTPError as e:
            logging.exception(
                f'Server returned error: '
                f'status " {e.code} reason : {e.reason}'
            )
            raise Exception(f'status code: {e.code}, reason: {e.reason}')
        except urllib.error.URLError as e:
            logging.exception(
                f'Handler returned error: '
                f'reason : {e.reason}'
            )
            raise Exception(f'Handler returned error. reason: {e.reason}')

    def upload(self, data, chart_id):
        """
        This function upload data to spreadsheet via Readily.
        Parameters
        ----------
        data : array
            Upload data. Example; [[3.4, 2, 10.1]] or [[3.4, 2, 10.1],[4, 3, 2]]
        chart_id : str
            You get chart_id from Readily after sign in. 
        """
        try:
            self._check_access_token_expired()
            return self.put(data, chart_id)
        except Exception as e:
            return {"result": "error"}