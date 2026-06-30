"""
sf_client.py
══════════════════════════════════════════════════════════════
SAP SuccessFactors OData v2 Client
Method 1: Calls OData with per-user bearer token

SAP returns ONLY what that user is permitted to read
based on their Role Based Permissions (RBP).
══════════════════════════════════════════════════════════════
"""

import requests
from typing import Optional


def _auth_headers(token: Optional[str] = None, api_key: Optional[str] = None) -> dict:
    """Build auth headers — either Bearer token (SAML) or APIKey (sandbox)."""
    if api_key:
        return {"APIKey": api_key, "Accept": "application/json"}
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def odata_get(
    host: str,
    entity: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    select: Optional[str] = None,
    filter: Optional[str] = None,
    top: int = 50,
) -> list:
    """
    Call SAP SuccessFactors OData v2 endpoint with per-user token.

    Args:
        host   : SAP OData host e.g. https://api4.successfactors.com
        token  : Per-user bearer token from sf_auth.get_user_token()
        entity : OData entity e.g. User, EmpJob, EmpEmployment
        select : Comma-separated fields e.g. userId,firstName,lastName
        filter : OData filter e.g. userId eq '12345'
        top    : Max records to return (default 50)

    Returns:
        List of records from OData response
    """
    params = {
        "$format": "json",
        "$top":    top,
    }
    if select:
        params["$select"] = select
    if filter:
        params["$filter"] = filter

    response = requests.get(
        f"{host}/{entity}",
        headers=_auth_headers(token=token, api_key=api_key),
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    return response.json().get("d", {}).get("results", [])


def odata_get_single(
    host: str,
    entity: str,
    entity_id: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    select: Optional[str] = None,
) -> dict:
    """
    Get a single entity by ID.

    Args:
        host      : SAP OData base URL (no trailing slash)
        entity    : OData entity name e.g. User
        entity_id : Entity key e.g. '12345'
        token     : Bearer token (SAML flow)
        api_key   : APIKey header value (sandbox flow)
        select    : Comma-separated fields to return
    """
    params = {"$format": "json"}
    if select:
        params["$select"] = select

    response = requests.get(
        f"{host}/{entity}('{entity_id}')",
        headers=_auth_headers(token=token, api_key=api_key),
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    return response.json().get("d", {})
