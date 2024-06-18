#!/usr/bin/env python3
""" Defines `top_students` function """


def top_students(mongo_collection):
    """ Returns all students sorted by average score """
    top = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top
