import json
import glob
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pathlib import Path


def write_jsons_into_mongo():
    try:
        # Create a new client and connect to the server
        uri = "mongodb+srv://newuser:newuserpassword@mycluster.4vebhys.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # new db with name of current dir
        db = client[Path(__file__).resolve().parent.name]
        # new collection for each json file
        file_list = [file for file in glob.glob("*.json")]
        for file in file_list:
            collection = db[file.removesuffix(".json")]
            # read json
            with open(Path(file).absolute(), "r", encoding="utf-8") as f:
                collection_data = json.load(f)
            # get keys
            collection_data_keys = [key for key in collection_data[0].keys()]
            # fill collection
            for el in collection_data:
                collection.insert_one({key: el[key] for key in collection_data_keys})
            print (f"Mongo DB: {Path(__file__).resolve().parent.name}, collection: {file.removesuffix(".json")} --> added.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    write_jsons_into_mongo()