import time

from NotifyManager import NotifyManager
from DNACManager import DNACManager
from MerakiManager import MerakiManager
from SDWANManager import SDWANManager

# environment
sdwan_flag = 1
dnac_flag = 1
meraki_flag = 1
notify_webex_flag = 1
notify_email_flag = 1

# SD-WAN environment
try:
    from env_device import vManager_HOST
    from env_user_credentials import vManager_USERNAME, vManager_PASSWORD
except Exception as e:
    sdwan_flag = 0
    print("=================================================")
    print("SD-WAN environment is incomplete. Please view the environment")
    print("setup guide from the readme.MD")
    print(e)
    print("=================================================")

# DNA Center environment
try:
    from env_device import DNAC_HOST
    from env_user_credentials import DNAC_USER, DNAC_PASSWORD
except Exception as e:
    dnac_flag = 0
    print("=================================================")
    print("DNAC environment is incomplete. Please view the environment")
    print("setup guide from the readme.MD")
    print(e)
    print("=================================================")

# Meraki environment
try:
    from env_device import MERAKI_URL, MERAKI_NETWORK_ID
    from env_user_credentials import MERAKI_API_KEY
except Exception as e:
    meraki_flag = 0
    print("=================================================")
    print("Meraki environment is incomplete. Please view the environment")
    print("setup guide from the readme.MD")
    print(e)
    print("=================================================")

# Notification environment for Webex teams
try:
    from env_device import WEBEX_TEAMS_URL
    from env_user_credentials import WEBEX_TEAMS_SPACE
    from env_user_credentials import WEBEX_TEAMS_TOKEN
except Exception as e:
    notify_webex_flag = 0
    print("=================================================")
    print("Webex environment is incomplete. Please view the environment")
    print("setup guide from the readme.MD")
    print(e)
    print("=================================================")

# Notification environment for e-mail
try:
    from env_device import EMAIL_HOST
    from env_device import EMAIL_SEND_MAILBOX
    from env_device import EMAIL_RECV_MAILBOX
    from env_user_credentials import EMAIL_USERNAME, EMAIL_PASSWORD
except Exception as e:
    notify_email_flag = 0
    print("=================================================")
    print("E-mail environment is incomplete. Please view the environment")
    print("setup guide from the readme.MD")
    print(e)
    print("=================================================")


#
# main function
#
if __name__ == "__main__":

    notifyMgr = NotifyManager()

    if notify_webex_flag == 1:
        webex = {}
        webex["webex_url"] = WEBEX_TEAMS_URL
        webex["webex_space"] = WEBEX_TEAMS_SPACE
        webex["webex_token"] = WEBEX_TEAMS_TOKEN
        notifyMgr.set_webex_para(webex_dict=webex)

    if notify_email_flag == 1:
        email = {}
        email["email_host"] = EMAIL_HOST
        email["email_recv_list"] = EMAIL_RECV_MAILBOX
        email["email_sender_mailbox"] = EMAIL_SEND_MAILBOX
        email["email_username"] = EMAIL_USERNAME
        email["email_password"] = EMAIL_PASSWORD
        notifyMgr.set_email_para(email_dict=email)

    if dnac_flag == 1:
        dnacMgr = DNACManager(
            notifymgr=notifyMgr,
            host=DNAC_HOST,
            username=DNAC_USER,
            password=DNAC_PASSWORD)

    if meraki_flag == 1:
        merakiMgr = MerakiManager(
            notify_mgr=notifyMgr,
            url=MERAKI_URL,
            apikey=MERAKI_API_KEY)

    if sdwan_flag == 1:
        sdwanMgr = SDWANManager(
            notify_mgr=notifyMgr,
            vmanage_ip=vManager_HOST,
            username=vManager_USERNAME,
            password=vManager_PASSWORD)

    for it in range(1, 3):

        if sdwan_flag == 1:
            sdwanMgr.verify_edge_routers()

        if meraki_flag == 1:
            merakiMgr.verify_ssid_status(
                network=MERAKI_NETWORK_ID)

        if dnac_flag == 1:
            dnacMgr.verify_devices()
            dnacMgr.verify_key_ports(
                ep_mac_list=["cc:d8:c1:15:d2:80", "50:61:bf:ec:07:84"])

        time.sleep(60)
