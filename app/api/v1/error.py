# -*- coding: UTF-8 -*-
from flask import jsonify


def data_wrong(status=1001, message=""):
    return jsonify(
        {
            "status": status,
            "message": message
        }
    )


def data_process_error(status=1002, message=""):
    return jsonify(
        {
            "status": status,
            "message": message
        }
    )


def no_person(status=1003, message=""):
    return jsonify(
        {
            "status": status,
            "message": message
        }
    )


def data_duplication(status=1004, message=""):
    return jsonify(
        {
            "status": status,
            "message": message
        }
    )
