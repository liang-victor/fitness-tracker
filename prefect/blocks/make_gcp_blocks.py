from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from pathlib import Path

SERVICE_ACCOUNT_FILE_PATH=Path("~/keys/fitness-data-377915-0e084f60d1d1.json")


credentials_block = GcpCredentials(
    service_account_path=SERVICE_ACCOUNT_FILE_PATH 
)
credentials_block.save("fitness-data-gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("fitness-data-gcp-creds"),
    bucket="strava_archive", 
)

bucket_block.save("strava-archive-gcs", overwrite=True)
