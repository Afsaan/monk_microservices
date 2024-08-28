# exceptions.py

import logging
from fastapi import status
from azure.cosmos import exceptions

def handle_file_not_found_error(e):
    logging.exception(f"FileNotFoundError: {e}")
    response = {
        "status_msg": False,
        "status_code": status.HTTP_404_NOT_FOUND,
        "message": str(e),
    }
    return response

def handle_key_error(e):
    logging.exception(f"KeyError: {e}")
    response = {
        "status_msg": False,
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": str(e),
    }
    return response

def handle_cosmos_not_found_exception(e):
    logging.exception(f"Item not found: {e}")
    response = {
        "status_msg": False,
        "status_code": status.HTTP_404_NOT_FOUND,
        "message": str(e),
    }
    return response

def handle_generic_exception(e):
    logging.exception(f"Error: {e}")
    response = {
        "status_msg": False,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,  
        "message": str(e),
    }
    return response

def handle_exception(e):
    if isinstance(e, FileNotFoundError):
        return handle_file_not_found_error(e)

    elif isinstance(e, KeyError):
        return handle_key_error(e)
    
    elif isinstance(e, exceptions.CosmosResourceNotFoundError):
        return handle_cosmos_not_found_exception(e)

    else:
        return handle_generic_exception(e)
