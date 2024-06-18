#!/usr/bin/env python3
""" Defines `list_all` function """


def list_all(mongo_collection):
    """ Lists all documents in a collection """
    return mongo_collection.find()
