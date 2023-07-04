import select
import socket
import struct
import re 
import time
from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
db = client["hackathon"]
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 6452  # The port used by the server
count = 0

dict={}
def contract_exists(data,coll):
    query = {"Strike_Amount":data["Strike_Amount"],"expiry_date":data["expiry_date"],"Contract_type":data["Contract_type"]} 
    existing_contract=db[coll].find_one(query)
    return existing_contract,query

def check_insert_table(data):
    date = False
    coll=""
    if data["expiry_date"] !="":
        for coll in db.list_collection_names():
        
            if data["expiry_date"]==coll :
                date = True
                break
            else:date=False
        if not date :
            print(0)
            db[data["expiry_date"]].insert_one(data) #data here is all the data of the packet
            #print(data["expiry_date"],coll,db.list_collection_names())
        else: # to check if the contract already exists if it exists then update it instead of inserting new contract
            contract,query = contract_exists(data,coll)
            print(contract,query)
            if contract:
                print(1)
                db[coll].replace_one(contract,data)
                
                
            else: 
                print(2)
                db[data["expiry_date"]].insert_one(data)
    else:
        db["no_expiry_date"].insert_one(data)

    
                
    

def unique_values(data):
    
    t_symbol = ''
    expiry_date = ''
    strike_amount = ''
    type_of_contract = ''
    
    y=0
    for x in data:
        if not re.search("[0-9]", x):
            t_symbol += x
        else:
            y = data.index(x)
            expiry_date=data[y:y+7]
            break
   
    for z in range(y+7, len(data)):
        if  re.search("[0-9]", data[z]):
            strike_amount += data[z]
        else:
            type_of_contract=data[z:]
            break

        

        
    
    return t_symbol,expiry_date,strike_amount,type_of_contract
        
        

    
def socket_data(data):
    all_data_dict = {}
    encoded_data = data
# Define the format string for decoding
    format_string = '<i30sq11q'

# Check if the encoded data has the minimum required size
    expected_size = struct.calcsize(format_string)
    print(len(encoded_data),expected_size)
    if len(encoded_data) >= expected_size:
        # Unpack the data
        decoded_data = struct.unpack(format_string, encoded_data[:expected_size])
        

        # Extract the fields
        packet_length, trading_symbol, sequence_number, timestamp, ltp, last_traded_qty, volume, bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = decoded_data

        # Convert trading symbol from bytes to string
        trading_symbol = trading_symbol.decode().rstrip('\x00')
        type_of_symbol,expiry_date,strike_amount,type_of_contract  = unique_values(trading_symbol)
        all_data_dict["Symbol"]=type_of_symbol
        all_data_dict["expiry_date"]=expiry_date
        all_data_dict["Strike_Amount"]=strike_amount
        all_data_dict["Contract_type"]=type_of_contract
        all_data_dict["Packet Length"]=packet_length
        all_data_dict["Trading Symbol"]=trading_symbol
        all_data_dict["Sequence Number"]=sequence_number
        all_data_dict["Timestamp"]=timestamp
        all_data_dict["Last Traded Price (LTP)"]=ltp
        all_data_dict["Last Traded Quantity"]=last_traded_qty
        all_data_dict["Volume"]=volume
        all_data_dict["Bid Price"]=bid_price
        all_data_dict["Bid Quantity"]=bid_qty
        all_data_dict["Ask Price"]=ask_price
        all_data_dict["Ask Quantity"]=ask_qty
        all_data_dict["Open Interest (OI)"]=open_interest
        all_data_dict["Previous Close Price"]=prev_close_price
        all_data_dict["Previous Open Interest"]=prev_open_interest

        # Print the extracted fields
        """print("Packet Length:", packet_length)
        print("Trading Symbol:", trading_symbol)
        print("Sequence Number:", sequence_number)
        print("Timestamp:", timestamp)
        print("Last Traded Price (LTP):", ltp)
        print("Last Traded Quantity:", last_traded_qty)
        print("Volume:", volume)
        print("Bid Price:", bid_price)
        print("Bid Quantity:", bid_qty)
        print("Ask Price:", ask_price)
        print("Ask Quantity:", ask_qty)
        print("Open Interest (OI):", open_interest)
        print("Previous Close Price:", prev_close_price)
        print("Previous Open Interest:", prev_open_interest)"""
        #print(all_data_dict)
        

    else:
        print("Incomplete data. Expected at least", expected_size, "bytes.")
    
    return all_data_dict

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        while True and count<1000:
            count +=1
            data = s.recv(130)
            
                
            
            dictionary_data=socket_data(data)
            print(f"count : {count }")
            print(dictionary_data)
            check_insert_table(dictionary_data)
            
            
            """print(f"type of symbol is : {dictionary_data["Symbol"]}")
            print(f"expiry date is  : {dictionary_data["expiry_date"]}")
            print(f"strike amount  is  : {dictionary_data["strike_amount"]}")
            print(f"type of contract  : {dictionary_data["Contract_type"]}")"""
            print('-------------------------------------------------------------')


# Example encoded data
"""encoded_data = data
# Define the format string for decoding
format_string = '<i30sq11q'

# Check if the encoded data has the minimum required size
expected_size = struct.calcsize(format_string)
print(len(encoded_data),expected_size)
if len(encoded_data) >= expected_size:
    # Unpack the data
    decoded_data = struct.unpack(format_string, encoded_data[:expected_size])
    

    # Extract the fields
    packet_length, trading_symbol, sequence_number, timestamp, ltp, last_traded_qty, volume, bid_price, bid_qty, ask_price, ask_qty, open_interest, prev_close_price, prev_open_interest = decoded_data

    # Convert trading symbol from bytes to string
    trading_symbol = trading_symbol.decode().rstrip('\x00')

    # Print the extracted fields
    print("Packet Length:", packet_length)
    print("Trading Symbol:", trading_symbol)
    print("Sequence Number:", sequence_number)
    print("Timestamp:", timestamp)
    print("Last Traded Price (LTP):", ltp)
    print("Last Traded Quantity:", last_traded_qty)
    print("Volume:", volume)
    print("Bid Price:", bid_price)
    print("Bid Quantity:", bid_qty)
    print("Ask Price:", ask_price)
    print("Ask Quantity:", ask_qty)
    print("Open Interest (OI):", open_interest)
    print("Previous Close Price:", prev_close_price)
    print("Previous Open Interest:", prev_open_interest)
else:
    print("Incomplete data. Expected at least", expected_size, "bytes.")"""
