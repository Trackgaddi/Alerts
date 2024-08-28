import smtplib
import requests
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

subject = 'TrackGaddi'
# admin_email = ['wellwininfotech@yahoo.in', 'ankesh.maradia@gmail.com', 'ankitjain1790@gmail.com',
#                'nayan.xt@outlook.com', 'vivek.xtremethoughts@outlook.com', 'nischay.xt@outlook.com']
admin_email = ['wellwininfotech@yahoo.in', 'ankesh.maradia@gmail.com', 'ankitjain1790@gmail.com','nayan.xt@outlook.com', 'vivek.xtremethoughts@outlook.com', 'dhruti.xt@outlook.com']
email_user = "trackgaddireports@gmail.com"
email_password = "iwusbsweblwvjgrm"

# Disable the automatic shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    pass

async def periodic_task():
    while True:
        print("Entered periodic_task")
        await get_website_status()
        print("Entering sleep")
        await asyncio.sleep(300)  # Sleep for 300 seconds (5 minutes)
        print("Out of sleep")

async def run_periodic_task():
    while True:
        print("Entered run_periodic_task")
        await periodic_task()

asyncio.create_task(run_periodic_task())

@app.get("/")
@app.head("/")
async def read_root():
    return {"message": "Hello, world!"}

async def get_website_status():
    # print("Entered get_website_status")
    try:
        # response0 = requests.get('https://pythonservicext.onrender.com', timeout=180)
        
        response = requests.get('http://52.76.115.44/api/v1/Monitoring/PortVehicleCount', timeout=180)
        api_response = response.json()
        response1 = requests.get('http://www.trackgaddi.com/api/v1/ApiHealthCheck/GetApiHealthCheck', timeout=30)
        api_response1 = response1.json()
        response2 = requests.get('http://gaddi24.com/api/v1/ApiHealthCheck/GetApiHealthCheck', timeout=30)
        api_response2 = response2.json()

        if response.status_code != 200:
            send_error("Trackgaddi Server is down.", str(1707168992454683726))
            # response0 = requests.get('https://pythonservicext.onrender.com', timeout=180)

        if response.status_code == 200:
            # response0 = requests.get('https://pythonservicext.onrender.com', timeout=180)
            down_apis = []
            size = 0
            for api_data in api_response:
                portNumber = int(api_data['PortNumber'])
                total_vehicle = int(api_data['TotalDevice'])
                unreachable = int(api_data['PercentUnreachable'])
                if portNumber == 111 or portNumber == 222:
                    percent_count = 20
                elif total_vehicle < 10:
                    percent_count = 50
                elif 10 < total_vehicle < 35:
                    percent_count = 35
                else:
                    percent_count = 40

                if unreachable >= percent_count:
                    down_apis.append(str(api_data))
                    size = len(down_apis)

            for api_data in api_response1:
                dbname = str(api_data['DbName'])
                tblname = str(api_data['TableName'])
                percent = int(api_data['percent'])
                smsBalanceAlert = str(api_data['SmsBalanceAlert'])                
                if smsBalanceAlert != "":
                    send_error("\n"+str(smsBalanceAlert),"0")
                if percent > 90:
                    send_error("Database:" + str(dbname) + "\n table Name:" + str(tblname) + "\n percent reach:" + str(percent), "0")
                    send_error("Trackgaddi Server is down.", str(1707168992454683726))

            for api_data in api_response2:
                dbname = str(api_data['DbName'])
                tblname = str(api_data['TableName'])
                percent = int(api_data['percent'])
                if percent > 90:
                    send_error("Database:" + str(dbname) + "\n table Name:" + str(tblname) + "\n percent reach:" + str(percent), "0")
                    send_error("Trackgaddi Server is down.", str(1707168992454683726))

            if size > 1:
                # response0 = requests.get('https://pythonservicext.onrender.com', timeout=180)
                
                send_email("TrackGaddi Port is down. " + str(down_apis))
            else:
                # response0 = requests.get('https://pythonservicext.onrender.com', timeout=180)
                
                print("No issues found. Function executed successfully.")  # Add a message to indicate successful execution
                
    except requests.ConnectionError:
        send_error("Connection Error. TrackGaddi", str(1707168992519849614))
    except requests.Timeout:
        send_error("Connection Timeout. TrackGaddi", str(1707168992511656154))
    except Exception as e:
        send_error("Trackgaddi Server is down.", str(1707168992454683726))
    finally:
        try:
            response0 = requests.get('https://system-alerts.onrender.com', timeout=180)
        except Exception as e:
            # If an exception occurs while making the request in the finally block,
            # you may want to log the error or take appropriate action.
            # For example, you can print the error message:
            print("An error occurred in the finally block:", str(e))


def send_error(error_msg, templateId):
    send_email(error_msg)
    send_sms(error_msg, templateId)

def send_email(email_body):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ", ".join(admin_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'plain'))
    text = msg.as_string()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email_user, email_password)
    server.sendmail(email_user, admin_email, text)
    server.quit()

def send_sms(msg, templateId):
    try:
        # response = requests.get("http://mysms.onlinebusinessbazaar.in/api/mt/SendSMS?user=wellwin&password=sms123&senderid=VTRAKK&channel=Trans&DCS=0&flashsms=0&number=8401207238,9137323046,9326852540,7878548818,8160757199&text="+ msg +"&route=06&DLTTemplateId="+templateId+"&PEID=1201159282315113937", timeout=60)
        response = requests.get("http://mysms.onlinebusinessbazaar.in/api/mt/SendSMS?user=wellwin&password=sms123&senderid=VTRAKK&channel=Trans&DCS=0&flashsms=0&number=8401207238,9737213291,9137323046,9326852540,7878548818,8160757199&text="+ msg +"&route=06&DLTTemplateId="+templateId+"&PEID=1201159282315113937", timeout=60)
        print(response.text)
    except Exception as e:
        print("sms error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
