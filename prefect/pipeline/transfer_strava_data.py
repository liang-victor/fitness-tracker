from prefect import flow, task
import os
from stravalib.client import Client


@task
def authenticate_strava_client():

    client = Client()

    # can we use prefect blocks to help manage secrets storage instead of ENV variables?
    if not os.environ.get("STRAVA_ACCESS_TOKEN"):
        authorize_url = client.authorization_url(client_id=os.environ.get("STRAVA_CLIENT_ID"), redirect_uri='http://localhost/authorized', scope="activity:read_all")
        print(f"\nAuthorize here and return the authorization code:\n {authorize_url}\n")
        authorization_code = input('Paste authorization code here: ')
        token_response = client.exchange_code_for_token(client_id=os.environ.get("STRAVA_CLIENT_ID"), client_secret=os.environ.get("STRAVA_CLIENT_SECRET"), code=authorization_code)
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

    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))


    return client

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
    client = authenticate_strava_client()
    activities = get_list_of_activities()
    for id in activities:
        print(id)
    



if __name__ == "__main__":
    transfer_strava_data()