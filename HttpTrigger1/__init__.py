import logging
import azure.functions as func

import json
import pandas as pd
from io import BytesIO

def main(req: func.HttpRequest, articles: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 1. get user id
    user_id = req.route_params.get('id')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('id')
    logging.info(f"user id : {user_id}")

    # 3. get the recommendations for the user
    try:
        user_recommendations = articles[0]["click_article_id"]
        user_recommendations = list(user_recommendations.split(", "))
    except IndexError:
        user_recommendations = ["no recommendation"]

    response = json.dumps({'user_recommendations': user_recommendations})

    logging.info(f"{response}")

    func.HttpResponse.mimetype = 'application/json'
    func.HttpResponse.charset = 'utf-8'

    return func.HttpResponse(response)