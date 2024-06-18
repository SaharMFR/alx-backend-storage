#!/usr/bin/env python3
"""
Improving `12-log_stats.py` by adding the top 10 of the most present
IPs in the collection `nginx` of the database `logs`.
"""
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

    ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "totalRequests": {"$sum": 1}}},
        {"$sort": {"totalRequests": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "ip": "$_id", "totalRequests": 1}}
    ])

    print("IPs:")
    for ip in ips:
        print(f"\t{ip.get('ip')}: {ip.get('totalRequests')}")
