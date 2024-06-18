#!/usr/bin/env python3
""" Provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    nLogs = nginx_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(nLogs, "logs")
    print("Methods:")
    for m in methods:
        nDocs = nginx_collection.count_documents({'method': m})
        print(f"\tmethod {m}: {nDocs}")
    sc = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(sc, "status check")
