import requests,os
from dotenv import load_dotenv
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
def send_discord_message(direct_url, status, timestamp, event_id,session_type,device_id):
    content = f"""
-------------------------------------------------------------------------------------------    
    NEW WEBHOOK EVENT!!
    \n EVENT_ID: **{event_id}**
    \n DEVICE ID: **{device_id}**
    \n SESSION TYPE: **{session_type.upper()}**
    \nSTATUS: **{status.upper()}**
    \nTIME: {timestamp}
    \nURL--{direct_url}
--------------------------------------------------------------------------------------------"""
    try: 
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content":content})
        if response.status_code == 204:
            print("Discord Notification Sent")
        else:
            print(f"Discord error: {response.status_code}  {response.text}")
            
    except Exception as e:
        print(f"failed to send Discord message: {e}")
        
        
if __name__ == "__main__":
    send_discord_message("direct_url","status","timestamp","event_id","session_type","device_id")