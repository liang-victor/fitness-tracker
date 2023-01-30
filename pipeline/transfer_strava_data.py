from prefect import flow, task
import os
from stravalib.client import Client


@task
def get_or_update_token():

    client = Client()

    # can we use prefect blocks to help manage secrets storage instead of ENV variables?
    if not os.environ.get("STRAVA_ACCESS_TOKEN"):
        authorize_url = client.authorization_url(client_id=os.environ.get("CLIENT_ID"), redirect_uri='http://localhost:8282/authorized', scope="activity:read_all")
        print(f"Authorize here and return the authorization code {authorize_url}")
        authorization_code = input('Paste authorization code here')
        token_response = client.exchange_code_for_token(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET", code=authorization_code))
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']
        expires_at = token_response['expires_at']
    else:
        access_token = os.environ.get("STRAVA_ACCESS_TOKEN")
        refresh_token = os.environ.get("STRAVA_REFRESH_TOKEN")
        expires_at = os.environ.get("STRAVA_TOKEN_EXPIRY")

    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at

    client.refresh_access_token

    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))


    return token

@task
def get_list_of_activities():
    activities = [1,2,3,4]
    return activities

@task
def fetch_activity_file(id):
    file = "asdg.doc"
    return file

@flow()
def transfer_strava_data():
    token = get_or_update_token()
    activities = get_list_of_activities()
    for id in activities:
        print(id)
    



if __name__ == "__main__":
    transfer_strava_data()