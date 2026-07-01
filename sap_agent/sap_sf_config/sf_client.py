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

import os, functools, requests
from typing import Optional
from google.adk.tools import ToolContext
# from google.cloud import secretmanager  # uncomment when deploying PROD (needs google-cloud-secret-manager)

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103032")


# PROD
# HOST = os.environ["SF_HOST"]
# COMPANY_ID = os.environ["SF_COMPANY_ID"]
# CLIENT_ID = os.environ["SF_CLIENT_ID"]
# ISSUER = os.environ["SF_SAML_ISSUER"]
# KEY_SECRET = os.environ["SF_PRIVATE_KEY_SECRET"]
# AUTH_ID = os.environ["SF_AUTH_ID"]  # must match the authorization id set in Step 8
# USERINFO = "https://openidconnect.googleapis.com/v1/userinfo"

# def _private_key():
#     client = secretmanager.SecretManagerServiceClient()
#     return client.access_secret_version(name=KEY_SECRET).payload.data.decode()

# def _caller_email(tool_context: ToolContext) -> str:
#     # Gemini Enterprise forwards the consented user OAuth token when the agent is
#     # registered with an authorization. It is keyed by the authorization id.
#     token = tool_context.state.get(f"temp:{AUTH_ID}")
#     if not token:
#         raise PermissionError("No user authorization present in the session.")
#     r = requests.get(USERINFO, headers={"Authorization": f"Bearer {token}"}, timeout=10)
#     r.raise_for_status()
#     return r.json()["email"]

# def _sf_user_id(email: str) -> str:
#     # Map the corporate email to the SuccessFactors user id. Replace with your
#     # directory lookup or a one time admin query on the User entity by email.
#     return email.split("@")[0]

# def _token_for(tool_context: ToolContext) -> tuple:
#     sf_user = _sf_user_id(_caller_email(tool_context))
#     token = sf_auth.get_user_token(sf_user, HOST, COMPANY_ID, CLIENT_ID,
#                                    _private_key(), ISSUER)
#     return sf_user, token


# ── OAuth identity resolution ─────────────────────────────────────────────────
AUTH_ID  = os.environ.get("SF_AUTH_ID", "")
USERINFO = "https://openidconnect.googleapis.com/v1/userinfo"

# username (part before @wohlig.com) → SAP SF userId
USER_MAP: dict[str, str] = {
    "vamsi.padmaraju": "100602",
    # "praveen.kumar":   "<SF_USER_ID>",
}


def resolve_user_id(tool_context) -> str:
    """Return the caller's SF user ID from their Google OAuth token, or the env fallback."""
    import logging
    log = logging.getLogger(__name__)

    email = tool_context.user_id

    if not email:
        log.warning("[DEBUG] No email found, using fallback USER_ID")
        return USER_ID
    
    username = email.lower().split("@")[0]
    sf_id = USER_MAP.get(username)
    if not sf_id:
        raise PermissionError(f"User '{username}' is not mapped to any SAP SF account.")
    return sf_id


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
    if response.status_code in (400, 404):
        return []
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
    if response.status_code in (400, 404):
        return {}
    response.raise_for_status()
    return response.json().get("d", {})