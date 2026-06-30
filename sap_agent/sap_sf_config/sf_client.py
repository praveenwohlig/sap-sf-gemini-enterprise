"""
sf_client.py
══════════════════════════════════════════════════════════════
SAP SuccessFactors OData v2 HTTP client.

Connection config is read once from environment variables:
  SF_SANDBOX_HOST     — base URL
  SF_SANDBOX_API_KEY  — APIKey header value (sandbox / API Hub)
  SF_SANDBOX_USER_ID  — default employee user ID (fallback: 103075)

Common query options exposed:
  select, filter, expand, orderby, top, skip,
  from_date / to_date  (SAP effective-date range params)
══════════════════════════════════════════════════════════════
"""

import os
import requests
from typing import Optional

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")


def _auth_headers() -> dict:
    return {"APIKey": API_KEY, "Accept": "application/json"}


def odata_get(
    entity: str,
    select: Optional[str] = None,
    filter: Optional[str] = None,
    expand: Optional[str] = None,
    orderby: Optional[str] = None,
    top: int = 50,
    skip: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> list:
    """Query an OData v2 collection and return the results list."""
    params: dict = {"$format": "json", "$top": top}

    if select:
        params["$select"] = select
    if filter:
        params["$filter"] = filter
    if expand:
        params["$expand"] = expand
    if orderby:
        params["$orderby"] = orderby
    if skip is not None:
        params["$skip"] = skip
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date

    response = requests.get(
        f"{HOST}/{entity}",
        headers=_auth_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("d", {}).get("results", [])


def odata_get_single(
    entity: str,
    entity_id: str,
    select: Optional[str] = None,
    expand: Optional[str] = None,
) -> dict:
    """Fetch a single entity by its string key."""
    params: dict = {"$format": "json"}
    if select:
        params["$select"] = select
    if expand:
        params["$expand"] = expand

    response = requests.get(
        f"{HOST}/{entity}('{entity_id}')",
        headers=_auth_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("d", {})