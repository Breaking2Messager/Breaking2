import requests
from requests.auth import HTTPBasicAuth


class DNACManager:

    """
    DNA Center Manager

    Attribute:
    _notify_mgr_: notification manager
    _dnac_host_: DNA Center host
    _dnac_user_: DNA Center username
    _dnac_password_: DNA Center password
    _token_: DNA Center login token
    """

    # construtor
    def __init__(self, notifymgr, host, username, password):
        self._notify_mgr_ = notifymgr

        self._dnac_host_ = host
        self._dnac_user_ = username
        self._dnac_password_ = password
        self._token_ = ""

        self._base_url_ = "https://%s:443" % host
        self._token_url_ = self._base_url_ + "/dna/system/api/v1/auth/token"
        self._intf_url_ = self._base_url_ + "/dna/intent/api/v1/interface"
        self._dev_url_ = self._base_url_ + "/dna/intent/api/v1/network-device"

        self.get_auth_token()

    # destructor
    def __del__(self):
        pass
    
    def get_auth_token(self):

        """
        get the token from DNA Center

        Keyword arguments:
        N/A
        """

        print("DNACManager.get_auth_token enters")
        print("DNACManager.get_auth_token token url = %s"
              % self._token_url_)

        auth = HTTPBasicAuth(
            self._dnac_user_,
            self._dnac_password_)
        token = ""
        success = True

        err_msg = "Error!DNACManager is failed to get the authorization token."
        try:
            resp = requests.post(self._token_url_,
                                 auth=auth,
                                 verify=False)
            token = resp.json()["Token"]
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(err_msg)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)
            success = False

        if success:
            self._token_ = token
            print("DNACManager.get_auth_token is successful")
        else:
            self._notify_mgr_.send_msg(text=err_msg)
            raise AssertionError(err_msg)

        print("DNACManager.get_auth_token ends")
        return

    def verify_key_ports(self, ep_mac_list):

        """
        verify whether ports are UP in the DNA network
        if interface is DOWN, then, one message is sent for notification
        if interface is UP, then, pass

        Keyword arguments:
        ep_mac_list: endpoint mac address to be verified

        """

        print("DNACManager.verify_key_ports enters")
        print("DNACManager.verify_key_ports token url = %s"
              % self._intf_url_)

        print("DNACManager.verify_key_ports following switchport are verified")
        for mac in ep_mac_list:
            print("mac address = %s" % mac)
        print("")

        header = {"x-auth-token": self._token_,
                  "content-type": "application/json"}

        try:
            response = requests.get(
                self._intf_url_,
                headers=header,
                verify=False)
        except Exception as e:
            print("ERROR! Exceptions are found to run verify_key_ports")
            print(e)
            return

        if response.status_code == 200:
            intf_list = response.json()
        else:
            print("ERROR! response is NOT 200 in verify_key_ports()")
            print(response)
            return

        for mac in ep_mac_list:
            flag = 0
            for intf in intf_list["response"]:
                if intf["macAddress"] == mac:
                    status = intf["status"]
                    port = intf["portName"]
                    srn = intf["serialNo"]
                    pid = intf["pid"]

                    print("=====================================")
                    print("Device PID=%s, SN=%s, port=%s, MAC=%s, status=%s"
                          % (pid, srn, port, mac, status))
                    print("=====================================")
                    flag = 1

                    if status == "down":
                        msg = "ERROR! Device with %s is offline" % mac
                        self._notify_mgr_.send_msg(text=msg)
                    else:
                        pass

                    break

            if flag == 0:
                print("WARNING! %s mac address is NOT found." % mac)

        return

    def verify_devices(self):

        """
        verify device error reported by DNA Center

        Keyword arguments:
        N/A

        """

        print("DNACManager.verify_devices enters")
        print("DNACManager.verify_devices url = %s"
              % self._dev_url_)

        header = {"x-auth-token": self._token_,
                  "content-type": "application/json"}

        try:
            response = requests.get(self._dev_url_,
                                    headers=header,
                                    verify=False)
        except Exception as e:
            print("ERROR! Exceptions are found to run verify_devices")
            print(e)
            return

        if response.status_code == 200:
            dev_list = response.json()
        elif response.status_code == 401:
            self.get_auth_token()
        else:
            print("ERROR! response is NOT 200 in verify_devices()")
            print(response)
            return

        for device in dev_list["response"]:
            code = device["errorCode"]
            hostname = device["hostname"]

            if code == "null" or code is None:
                print("%s is OK without exceptions" % hostname)
            else:
                err = "ERROR! %s has error code: %s" % (hostname, code)
                msg = err + "\n" + str(device)
                self._notify_mgr_.send_msg(text=msg)

        print("DNACManager.verify_devices ends")


