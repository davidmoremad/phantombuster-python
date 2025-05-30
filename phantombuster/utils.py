import json
import yaml
import requests
import os

def script_settings_loader(script_id):
    """Load default script settings from a YAML file.
    Args:
        script_id (str): The ID of the script to load settings for.
    Raises:
        FileNotFoundError: If the configuration file is not found.
    Returns:
        dict: The script settings for the specified script ID, or an empty dictionary if not found.
    """
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'scripts.yaml')
        with open(config_path, 'r') as file:
            scripts = yaml.safe_load(file)

        # Return script settings if script_id exists, otherwise return an empty dict
        for script in scripts:
            if str(script.get('id')) == str(script_id):
                return script
        return {}
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file 'phantombuster/config/scripts.yaml' not found.")


class RequestHandler(object):
    def __init__(self, endpoint, headers={}, key=None, secret=None):
        self.endpoint = endpoint
        self.headers = headers
        self.key = key or ''
        self.secret = secret or ''

    def _request(self, method, route, payload=None):
        res = url = err = jsonObject = None
        _payload = json.dumps(payload)
        url = '{}{}'.format(self.endpoint, route)

        try:
            if method == 'get':
                res = requests.get(
                    url=url, params=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'post':
                res = requests.post(
                    url=url, data=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'patch':
                res = requests.patch(
                    url=url, json=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'put':
                res = requests.put(
                    url=url, data=_payload, headers=self.headers, auth=(self.key, self.secret))
            elif method == 'delete':
                res = requests.delete(
                    url=url, params=_payload, headers=self.headers, auth=(self.key, self.secret))
                return bool(res.status_code == 204)
        except requests.ConnectionError as ex:
            raise ConnectionError(url, ex.args[0])

        if str(res.status_code)[0] == '2':
            try:
                if res.content:
                    try:
                        jsonObject = res.json()
                    except json.JSONDecodeError:
                        jsonObject = {'content': res.content.decode('utf-8')}
            except Exception as ex:
                err = {'code': res.status_code, 'message': getattr(ex, 'message', ''), 'content': res.content}
        else:
            err = {'code': res.status_code,
                   'message': res.reason, 'content': res.content}

        if err:
            raise Exception(err)
        return jsonObject

    def get(self, *args, **kwargs):
        """Make a GET request"""
        return self._request('get', *args, **kwargs)
    
    def post(self, *args, **kwargs):
        """Make a POST request"""
        return self._request('post', *args, **kwargs)
    
    def patch(self, *args, **kwargs):
        """Make a PATCH request"""
        return self._request('patch', *args, **kwargs)
    
    def put(self, *args, **kwargs):
        """Make a PUT request"""
        return self._request('put', *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Make a DELETE request"""
        return self._request('delete', *args, **kwargs)