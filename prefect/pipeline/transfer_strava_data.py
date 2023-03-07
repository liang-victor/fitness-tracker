from prefect import flow, task
import os
from stravalib.client import Client
from prefect.blocks.system import Secret, DateTime
import pendulum

STRAVA_ACCESS_TOKEN = "strava-access-token"
STRAVA_REFRESH_TOKEN = "strava-refresh-token"
STRAVA_TOKEN_EXPIRY = "strava-token-expiry"

@task
def authenticate_strava_client():

    client = Client()

    try: 
        client.access_token = Secret.load(STRAVA_ACCESS_TOKEN).get()
        client.refresh_token = Secret.load(STRAVA_REFRESH_TOKEN).get()
        client.token_expires_at = DateTime.load(STRAVA_TOKEN_EXPIRY).value.timestamp()
    except ValueError:
        manual_authorization(client)

    if pendulum.now().timestamp() > client.token_expires_at:
        client = refresh_access_token(client)
    return client

def manual_authorization(client):
        authorize_url = client.authorization_url(client_id=os.environ.get("STRAVA_CLIENT_ID"), redirect_uri='http://localhost/authorized', scope="activity:read_all")
        print(f"\nAuthorize here and return the authorization code:\n {authorize_url}\n")
        authorization_code = input('Paste authorization code here: ')
        token_response = client.exchange_code_for_token(client_id=os.environ.get("STRAVA_CLIENT_ID"), 
                                                        client_secret=os.environ.get("STRAVA_CLIENT_SECRET"), 
                                                        code=authorization_code)
        store_token_response_in_blocks(token_response)

def refresh_access_token(client):
    token_response = client.refresh_access_token(client_id=os.environ.get("STRAVA_CLIENT_ID"), 
                                    client_secret=os.environ.get("STRAVA_CLIENT_SECRET"),
                                    refresh_token=client.refresh_token)
    store_token_response_in_blocks(token_response)
    client.access_token = token_response["access_token"]
    client.refresh_token = token_response["refresh_token"]
    client.expiry = token_response["expires_at"]
    return client

def store_token_response_in_blocks(token_response):
        Secret(value=token_response['access_token']).save(STRAVA_ACCESS_TOKEN, overwrite=True)
        Secret(value=token_response['refresh_token']).save(STRAVA_REFRESH_TOKEN, overwrite=True)
        DateTime(value=pendulum.from_timestamp(token_response['expires_at'])).save(STRAVA_TOKEN_EXPIRY, overwrite=True)

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