import requests,os
from db_handler import list_records
from dotenv import load_dotenv
load_dotenv()
DISCORD_SERVER_LOGGER_URL = os.getenv("DISCORD_SERVER_LOGGER_URL")
def send_discord_message(status):
    if status in "RUNNING":
        content = f"""
------------------------------------------------------------------------------------------- 
                                    @everyone SERVER IS RUNNING   
--------------------------------------------------------------------------------------------"""
        try: 
            response = requests.post(DISCORD_SERVER_LOGGER_URL, json={"content":content})
            if response.status_code == 204:
                print("Discord Notification Sent")
            else:
                print(f"Discord error: {response.status_code}  {response.text}")
                
        except Exception as e:
            print(f"failed to send Discord message: {e}")
    elif status in "RESULTS":
        results = []
        for i in list_records(5):
            results.append(i+"\n")
        formatted = f"{'\n'.join(results)}"
        content = f"""
        
------------------------------------------------------------------------------------------- 
@everyone
RESULTS:
{f"{formatted}\n"}
--------------------------------------------------------------------------------------------"""
        try: 
            response = requests.post(DISCORD_SERVER_LOGGER_URL, json={"content":content})
            if response.status_code == 204:
                print("Discord Notification Sent")
            else:
                print(f"Discord error: {response.status_code}  {response.text}")
                
        except Exception as e:
            print(f"failed to send Discord message: {e}")
        
        
            
    elif status in "OFFLINE":
        content = f"""
        
------------------------------------------------------------------------------------------- 
                                    @everyone SERVER IS OFFLINE   
-------------------------------------------------------------------------------------------"""
        try: 
            response = requests.post(DISCORD_SERVER_LOGGER_URL, json={"content":content})
            if response.status_code == 204:
                print("Discord Notification Sent")
            else:
                print(f"Discord error: {response.status_code}  {response.text}")
                
        except Exception as e:
            print(f"failed to send Discord message: {e}")
                
    else:
        content = f"""
        
------------------------------------------------------------------------------------------- 
@everyone SOMETHING WENT WRONG AND WE DON'T KNOW

!!!!!PLEASE PANIC!!!
--------------------------------------------------------------------------------------------"""
        try: 
            response = requests.post(DISCORD_SERVER_LOGGER_URL, json={"content":content})
            if response.status_code == 204:
                print("Discord Notification Sent")
            else:
                print(f"Discord error: {response.status_code}  {response.text}")
                
        except Exception as e:
            print(f"failed to send Discord message: {e}")
                
if __name__ == "__main__":
    send_discord_message("ONLINE")
    send_discord_message("RESULTS")
    send_discord_message("OFFLINE")