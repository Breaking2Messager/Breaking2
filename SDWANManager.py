#! /usr/bin/env python
"""
Class with REST Api GET and POST libraries

Example: python rest_api_lib.py vmanage_hostname username password

PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage

Note: All the three arguments are manadatory
"""
import time
import json
import requests


class SDWANManager:

    """
    SD-WAN Manager

    Attribute:
    _notify_mgr_: notification manager
    _dnac_host_: DNA Center host
    _dnac_user_: DNA Center username
    _dnac_password_: DNA Center password
    _token_: DNA Center login token
    """

    # construtor
    def __init__(self, notify_mgr, vmanage_ip, username, password):
        self._notify_mgr_ = notify_mgr
        self._vmanage_ip_ = vmanage_ip
        self._username_ = username
        self._password_ = password

        self.session = {}
        self.login(
            self._vmanage_ip_,
            self._username_,
            self._password_)

    # destructor
    def __del__(self):
        pass

    def login(self, vmanage_ip, username, password):

        """
        login function

        Keyword arguments:
        vmanage_ip: vManager ip address
        username: vManager username
        password: vManager password
        """

        base_url_str = "https://%s:8443/" % vmanage_ip
        login_action = "/j_security_check"

        # Format data for loginForm
        login_data = {
            "j_username": username,
            "j_password": password}

        # Url for posting login data
        login_url = base_url_str + login_action

        sess = requests.session()

        print("Start to login vManager ... ")
        err_msg = "ERROR! Fail to login vManager!"
        try:
            login_response = sess.post(
                url=login_url,
                data=login_data,
                verify=False)
            print(login_response.headers)
        except Exception as e:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(err_msg)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            raise AssertionError(err_msg)

        st_code = login_response.status_code
        if int(st_code) != 200:
            err_msg = "Login Failed with response code %s" % st_code
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(err_msg)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            raise AssertionError(err_msg)

        print("Cookie=%s" % login_response.cookies)
        self.session[vmanage_ip] = sess

    def verify_edge_routers(self):

        """
        verify edge router status

        Keyword arguments:
        N/A
        """

        # get device status
        url = "https://%s:8443/dataservice/device" % self._vmanage_ip_

        print("Start to get the device status ...")
        response = self.session[self._vmanage_ip_].get(
            url,
            verify=False)

        if int(response.status_code) != 200:
            print("Fail to get device information %s" % response.status_code)
            print(response.content)
            return

        dev_info = json.loads(response.content)
        for data in dev_info.get("data"):
            sys_ip = data.get("system-ip")

            # verify whether device is reachable
            if data.get("reachability") == "unreachable":
                err = "ERROR! Device %s reachability is unreachable" % sys_ip
                msg = err + "\n" + str(data)
                self._notify_mgr_.send_msg(text=msg)
            else:
                print("%s is reachable" % sys_ip)

            # verify whether device status is normal
            if data.get("status") != "normal":
                err = "ERROR! Device status %s is NOT normal" % sys_ip
                msg = err + "\n" + str(data)
                self._notify_mgr_.send_msg(text=msg)
