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
admin_email = ['wellwininfotech@yahoo.in','ankesh.maradia@gmail.com', 'ankitjain1790@gmail.com','nayan.xt@outlook.com','vivek.xtremethoughts@outlook.com']
email_user = "trackgaddireports@gmail.com"
email_password = "iwusbsweblwvjgrm"
#log_file = "C:/WT_Services/trackgaddi_server_check_log.txt"
# log_file = "C:/Log/trackgaddi_server_check_log.txt"

async def periodic_task():
    while True:
        get_website_status()
        await asyncio.sleep(180)  # Sleep for 180 seconds (3 minutes)

async def read_root():
    await periodic_task()

@app.get("/")
async def main():
    await read_root()
def get_website_status():
    try:
           response = requests.get('http://52.76.115.44/api/v1/Monitoring/PortVehicleCount',timeout=180)
           api_response = response.json()
           response1 = requests.get('http://www.trackgaddi.com/api/v1/ApiHealthCheck/GetApiHealthCheck',timeout=30)
           api_response1 = response1.json()
           response2 = requests.get('http://gaddi24.com/api/v1/ApiHealthCheck/GetApiHealthCheck',timeout=30)
           api_response2 = response2.json()
           
           if response.status_code != 200:
              send_error("Trackgaddi Server is down.", str(1707168992454683726))
           
           if response.status_code == 200:
                down_apis = []
                error_msg = ","
                size =0
                for api_data in api_response:
                 portNumber = int(api_data['PortNumber'])
                 total_vehicle = int(api_data['TotalDevice'])
                 unreachable = int(api_data['PercentUnreachable'])
                 portNumber = int(api_data['PortNumber'])
                 if portNumber == 111 or portNumber == 222:
                     percent_count = 20
                 elif total_vehicle<10:
                    percent_count = 50
                 elif (total_vehicle < 35 & total_vehicle > 10):
                    percent_count = 35
                 else:
                    percent_count = 40

                 if unreachable >=percent_count:
                    down_apis.append(str(api_data))
                    size =len(down_apis)
                    #error_msg = error_msg.join(down_apis)
                  #   send_error_port("TrackGaddi Port Number is down "+ error_msg +" VTRACK", str(1207161709404513525))
                for api_data in api_response1:
                  dbname=str(api_data['DbName'])
                  tblname=str(api_data['TableName'])
                  percent=int(api_data['percent'])
                  if percent>90:
                   send_error("Database:"+str(dbname)+"\n table Name:"+str(tblname)+"\n percent reach:"+str(percent),0)
                   send_error("Trackgaddi Server is down.", str(1707168992454683726))
                for api_data in api_response2:
                  dbname=str(api_data['DbName'])
                  tblname=str(api_data['TableName'])
                  percent=int(api_data['percent'])
                  if percent>90:
                   send_error("Database:"+str(dbname)+"\n table Name:"+str(tblname)+"\n percent reach:"+str(percent),0)
                   send_error("Trackgaddi Server is down.", str(1707168992454683726))
                if size > 1: 
                    send_email("TrackGaddi Port is down. "+ str(down_apis))
               # if len(down_apis) > 0:
               #   error_msg = error_msg.join(down_apis)
               #   send_error("TrackGaddi Port Number is down "+ error_msg +" VTRACK", str(1207161709404513525))
    except requests.ConnectionError:
       send_error("Connection Error. TrackGaddi", str(1707168992519849614))
    except requests.Timeout:
       send_error("Connection Timeout. TrackGaddi", str(1707168992511656154))
    except Exception as e:
      #  write_log(str(e)) 
       send_error("Trackgaddi Server is down.", str(1707168992454683726))    


def send_error(error_msg, templateId):
   #  write_log(error_msg)
    send_email(error_msg)
    send_sms(error_msg,templateId)

def send_email(email_body):
    msg = MIMEMultipart()
    msg['From'] = email_user
 
    msg['To'] = ", ".join(admin_email)
 
    msg['Subject'] = subject
 
    msg.attach(MIMEText(email_body,'plain'))
 
    text = msg.as_string()
    #server = smtplib.SMTP('smtp.gmail.com',587,timeout=30)
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    #server.starttls()
    server.login(email_user,email_password) 
    server.sendmail(email_user,admin_email,text)
    server.quit()   

def send_sms(msg, templateId):
   #response = requests.get("http://sms.onlinebusinessbazaar.in/api/mt/SendSMS?user=wellwin&password=sms123&senderid=VTRACK&channel=trans&DCS=0&flashsms=0&number=7878548818&text="+ msg +"",timeout=30)
   try:
      response = requests.get("http://mysms.onlinebusinessbazaar.in/api/mt/SendSMS?user=wellwin&password=sms123&senderid=VTRAKK&channel=Trans&DCS=0&flashsms=0&number=8401207238,9137323046,9326852540,7878548818,8160757199&text="+ msg +"&route=06&DLTTemplateId="+templateId+"&PEID=1201159282315113937",timeout=60) 
      print(response.text)
   except Exception as e:
       print("sms error")
      #  write_log(str(e)) 

# def write_log(log_msg):
#     file = open(log_file, "a")
#     date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#     file.write(date + ' : '+ log_msg +'\n')
#     file.close()


if __name__ == '__main__':
    asyncio.run(main())
