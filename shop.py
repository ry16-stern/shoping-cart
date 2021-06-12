from pandas import read_csv
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
load_dotenv()
TAX_RATE = os.getenv("TAX_RATE") 

csv_filepath = "data/products.csv"
products_df = read_csv(csv_filepath)



SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")


def print_receipt_and_send_email(text):
    STORE_NAME = os.getenv("STORE_NAME")
    STORE_WEBSITE= os.getenv("STORE_WEBSITE")
    now = datetime.now()


    print("---------------------------------")
    print(STORE_NAME)
    print(STORE_WEBSITE)
    print("---------------------------------")
    print(now.strftime("%d-%m-%Y %H:%M %p"))
    print("---------------------------------")
    print(text)

loop=1
cart=[]

while loop==1:
    user_input=input("Please input a product identifier:")
    if user_input!="DONE":
        #main code
        pick=products_df.loc[products_df["id"]==int(user_input)].to_dict(orient = 'records')[0]
        pick["quant"]=1
        loop=1
        if(len(cart)>0):
            match=0
            for item in cart:
                if item["id"]==pick["id"]:
                    item["quant"] += 1
                    match += 1
                    break
            if match<1:
              cart.append(pick)  
        else:
            cart.append(pick)
        
    else:
        #exit message
        loop=0
        print(cart)


def email():
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))

    subject = "Your Receipt from the Green Grocery Store"

    html_content = "Hello World"
    print("HTML:", html_content)

    # FYI: we'll need to use our verified SENDER_ADDRESS as the `from_email` param
    # ... but we can customize the `to_emails` param to send to other addresses
    message = Mail(from_email=SENDER_ADDRESS, to_emails=SENDER_ADDRESS, subject=subject, html_content=html_content)

    try:
        response = client.send(message)

        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        print(response.body)
        print(response.headers)

    except Exception as err:
        print(type(err))
        print(err)