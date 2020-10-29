import json
import time
import requests

class MerakiManager():

    """
    Meraki Manager

    Attribute:
    _notify_mgr_: notification manager
    _url_: Meraki URL
    _api_key_: Meraki API key
    """

    def __init__(self, notify_mgr, url, apikey):
        self._notify_mgr_ = notify_mgr
        self._url_ = url
        self._api_key_ = apikey

    #
    # destructor
    #
    def __del__(self):

        pass

    #
    # verify ssid status in the network
    #
    def verify_ssid_status(self, network):

        """
        verify ssid status

        Keyword arguments:
        network: network id
        """

        print("MerakiManager verify_ssid_status enters")
        print("MerakiManager network id=%s" % network)

        url = self._url_ + "/networks/%s/ssids" % network

        # Get Orgs that entered Meraki API Key has access to
        try:
            ssids = requests.get(
                url,
                headers={
                    "X-Cisco-Meraki-API-Key": MERAKI_API_KEY,
                    }
                )
        except Exception as e:
            print(e)

        if ssids.status_code == 200:
            ssids = json.loads(ssids.text)
        else:
            print(ssids.status_code)
            print(ssids.text)
            return

        enable_flag = 1
        enable_ssid_name_list = []
        enable_ssid_data_list = []
        print("They are: ")
        for ssid in ssids:
            print("ssid=%s will be verified" % ssid)
            if ssid['enabled'] is False:
                enable_flag = 0
                enable_ssid_name_list.append(ssid['name'])
                enable_ssid_data_list.append(str(ssid))

        print(enable_ssid_name_list)
        msg = 'WARNING! Following SSID is disabled: %s' % enable_ssid_name_list
        if enable_flag == 1:
            pass
        else:
            self._notify_mgr_.send_msg(text=msg)

        return
