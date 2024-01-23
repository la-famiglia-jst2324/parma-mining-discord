"""Main entrypoint for the API routes in of parma-analytics."""
import json
import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, status

from parma_mining.discord.analytics_client import AnalyticsClient
from parma_mining.discord.api.dependencies.auth import authenticate
from parma_mining.discord.client import DiscordClient
from parma_mining.discord.helper import collect_errors
from parma_mining.discord.model import (
    CompaniesRequest,
    DiscoveryRequest,
    ErrorInfoModel,
    FinalDiscoveryResponse,
    ResponseModel,
)
from parma_mining.discord.normalization_map import DiscordNormalizationMap
from parma_mining.mining_common.exceptions import ClientInvalidBodyError, CrawlingError

env = os.getenv("DEPLOYMENT_ENV", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

authorization_key = str(os.getenv("DISCORD_AUTH_KEY"))
base_url = str(os.getenv("DISCORD_BASE_URL"))

app = FastAPI()

discord_client = DiscordClient(authorization_key, base_url)
analytics_client = AnalyticsClient()
normalization = DiscordNormalizationMap()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-discord"}


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize(source_id: int, token: str = Depends(authenticate)) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "daily"
    normalization_map = DiscordNormalizationMap().get_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        token=token, mapping=normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post("/companies", status_code=status.HTTP_200_OK)
def get_organization_details(body: CompaniesRequest):  # don't forget to add the token
    """Endpoint to get detailed information about a dict of servers."""
    errors: dict[str, ErrorInfoModel] = {}

    all_server_details = []

    for company_id, company_data in body.companies.items():
        for data_type, handles in company_data.items():
            for handle in handles:
                try:
                    server_details = discord_client.get_server_details(handle)
                except CrawlingError as e:
                    logger.error(f"Can't fetch company details from GitHub. Error: {e}")
                    collect_errors(company_id, errors, e)
                    continue

                _ = ResponseModel(
                    source_name="discord",
                    company_id=company_id,
                    raw_data=server_details,
                )

                all_server_details.append(server_details)
    return all_server_details


@app.post(
    "/discover",
    response_model=FinalDiscoveryResponse,
    status_code=status.HTTP_200_OK,
)
def discover_companies(
    request: list[DiscoveryRequest],  # token: str = Depends(authenticate)
):
    """Endpoint to discover organizations based on provided names."""
    if not request:
        msg = "Request body cannot be empty for discovery"
        logger.error(msg)
        raise ClientInvalidBodyError(msg)

    response_data = {}
    for company in request:
        logger.debug(
            f"Discovering with name: {company.name} for company_id {company.company_id}"
        )
        print(company.name)
        response = discord_client.search_organizations(company.name)
        response_data[company.company_id] = response

    current_date = datetime.now()
    valid_until = current_date + timedelta(days=180)

    return FinalDiscoveryResponse(identifiers=response_data, validity=valid_until)
