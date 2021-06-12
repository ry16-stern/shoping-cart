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
now = datetime.now()


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

def to_usd(my_price):
    return f"${my_price:,.2f}"

def save_to_file(string):
    #function accepts the string and saves it in a text file
    date=now.strftime("%Y-%m-%d-%H-%M-%p")
    text_file = open("receipts/"+str(date)+".txt", "x")
    n = text_file.write(string)
    text_file.close()

def email(email_body,sn):
    #function accepts string and emails via sendgrid API
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))

    subject = "Your Receipt from the " + str(sn) + " store." 

    html_content = email_body
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

    save_to_file(email_body)


def print_receipt():
    #function prints the receipt and sends the receipt string to email function
    STORE_NAME = os.getenv("STORE_NAME")
    STORE_WEBSITE= os.getenv("STORE_WEBSITE")
    
    #print the header
    sp="\n----------------------------\n"
    nl="\n"
    header=sp+STORE_NAME+nl+STORE_WEBSITE+sp+"CHECKOUT AT: "+now.strftime("%d-%m-%Y %H:%M %p")+sp

    
    #print the list of items
    subtot=0
    body=""
    for item in cart:
      price=item["price"]
      quant=item["quant"]
      
      space1=" " * (50-len(item["name"]))
      if item["price_per"]=="item":
          tot=int(quant)*float(price)
      else:
          tot=item["price"]
      line=" ... "+item["name"]+space1+"quantity: "+str(quant)+" X "+ to_usd(float(products_df.loc[products_df["id"]==int(item["id"])].to_dict(orient = 'records')[0]["price"]))+"  ("+to_usd(float(tot))+")"
     
      body=body+line+nl
      subtot=subtot+tot
    #print taxes and totals
    tax=subtot*float(TAX_RATE)

    footer=sp+"SUBTOTAL: "+str(to_usd(float(subtot)))+nl+"TAX:      "+to_usd(float(tax))+nl+"TOTAL:    "+to_usd(float(subtot+tax))+sp+"THANKS, SEE YOU AGAIN SOON!"+sp
    print(header)
    print(body)
    print(footer)

    email_body=header+nl+body+nl+footer
    #send email
    email(email_body,STORE_NAME)   



#--------------- MAIN LOOP -----------
'''Main loop of the app allows user to enter an id of the item and adds an item to cart object. 
   The loop checks if the item already in the cart and if so increments quant for items.
   For items that are charged per pound it will ask the user to indicate the number of pounds and 
   calculate the total amoun by multiplying pounds and price per pound. 
   After the input is done the cart will be sent to print_receipt_and_send_email function.
'''
loop=1
cart=[]
# get the list of id's for further exist check
ids=products_df["id"]
while loop==1:
    user_input=input("Please input a product identifier or enter DONE to finish:")
    #check if user is entering a proper ID
    if user_input=="":
        print("No products were entered, exiting the checkout")
        break
    if int(user_input) in ids:

        if user_input!="DONE":
            #main code
            pick=products_df.loc[products_df["id"]==int(user_input)].to_dict(orient = 'records')[0]
            pick["quant"]=1
            loop=1
            if pick["price_per"]=="item": #if an item added is counted per item
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
            else: #if an item added is counted per pound, checks if item is new or existing and calculates increments
                pounds=input("How many pounds?")
                price=pick["price"]*float(pounds)
                if(len(cart)>0):
                    match=0
                    for item in cart:
                        if item["id"]==pick["id"]:
                            item["quant"] += float(pounds)
                            item["price"] += float(price)
                            match += 1
                            break
                    if match<1:
                        pick["quant"] = float(pounds)
                        pick["price"] = float(price)
                        cart.append(pick)  
                else:
                    cart.append(pick)

        else:
            #exit message
            loop=0
            if len(cart)>0:
                print_receipt()
    else: #id does not exist in the product inventory
        print("Product does not exist")


