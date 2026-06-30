"""
sf_client.py
══════════════════════════════════════════════════════════════
SAP SuccessFactors OData v2 HTTP client.

Supports both auth modes:
  • api_key  → APIKey header (sandbox / API Hub)
  • token    → Bearer token  (SAML / OIDC production)

Common query options exposed:
  select, filter, expand, orderby, top, skip,
  from_date / to_date  (SAP effective-date range params)
══════════════════════════════════════════════════════════════
"""

import requests
from typing import Optional


def _auth_headers(token: Optional[str] = None, api_key: Optional[str] = None) -> dict:
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
    expand: Optional[str] = None,
    orderby: Optional[str] = None,
    top: int = 50,
    skip: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> list:
    """
    Query an OData v2 collection and return the results list.

    Args:
        host      : Base URL, e.g. https://sandbox.api.sap.com/successfactors/odata/v2
        entity    : Entity set name, e.g. EmpJob, EmpEmployment
        token     : Bearer token (SAML/OIDC flow)
        api_key   : APIKey value (sandbox flow)
        select    : $select — comma-separated field names
        filter    : $filter — OData filter expression
        expand    : $expand — comma-separated navigation properties
        orderby   : $orderby — e.g. "startDate desc"
        top       : $top   — max records (default 50)
        skip      : $skip  — records to skip (pagination)
        from_date : SAP fromDate param for effective-dated entities (YYYY-MM-DD)
        to_date   : SAP toDate  param for effective-dated entities (YYYY-MM-DD)

    Returns:
        List of record dicts from the OData response.
    """
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
    expand: Optional[str] = None,
) -> dict:
    """
    Fetch a single entity by its string key.

    Args:
        host      : Base URL
        entity    : Entity name, e.g. HireDateChange
        entity_id : Key value, e.g. 'testCode'
        token     : Bearer token
        api_key   : APIKey value
        select    : $select fields
        expand    : $expand navigation properties

    Returns:
        Single record dict, or empty dict if not found.
    """
    params: dict = {"$format": "json"}
    if select:
        params["$select"] = select
    if expand:
        params["$expand"] = expand

    response = requests.get(
        f"{host}/{entity}('{entity_id}')",
        headers=_auth_headers(token=token, api_key=api_key),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("d", {})
