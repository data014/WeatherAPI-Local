from datetime import datetime
import pytz
import pymongo
from urllib.parse import quote_plus

def upload_to_cloud(data:dict, password:str, db_name="IITB", collection_name="weather"):
    try:
        client =  pymongo.MongoClient(
            f"mongodb+srv://chandankr014:{password}@cluster0.cfw5xma.mongodb.net/?retryWrites=true&w=majority"
        )
        db = client[db_name] #IITB
        collection = db[collection_name] #weather

        india_timezone = pytz.timezone('Asia/Kolkata')
        dt = datetime.now(india_timezone).strftime('%Y-%m-%d %H:%M:%S')
        data['uploaded_at'] = dt  

        collection.insert_one(data)
        print(f"Uploaded to {db_name}.{collection_name} collection in MongoDB")

    except Exception as e:
        print(f"An error occurred: {e}")