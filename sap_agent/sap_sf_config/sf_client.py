"""
sf_client.py
══════════════════════════════════════════════════════════════
SAP SuccessFactors OData v2 HTTP client.

Auth modes (set AUTH_MODE in .env):
  sandbox    — uses APIKey header + EMAIL_USER_MAP for userId
  production — uses Google OAuth token from Gemini Enterprise
               → calls UserInfo → maps email → SF userId

Environment variables:
  AUTH_MODE           — "sandbox" or "production"
  SF_SANDBOX_HOST     — SF base URL
  SF_SANDBOX_API_KEY  — sandbox APIKey
  SF_SANDBOX_USER_ID  — fallback userId if email not in map
  SF_AUTH_ID          — Gemini Enterprise authorization ID (production)
══════════════════════════════════════════════════════════════
"""

import os
import sys
import requests
from typing import Optional
from google.adk.tools import ToolContext


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)

HOST     = os.environ["SF_SANDBOX_HOST"]
API_KEY  = os.environ["SF_SANDBOX_API_KEY"]
AUTH_MODE = os.environ.get("AUTH_MODE", "sandbox")
AUTH_ID  = os.environ.get("SF_AUTH_ID", "google_oauth")
USERINFO = "https://openidconnect.googleapis.com/v1/userinfo"


# ── Email → SF userId map ─────────────────────────────────────
# Add every team member here: email prefix → SF test userId
EMAIL_USER_MAP = {
    "praveen.kumar":   "106002",
    "vamsi.padmaraju": "103032",
}

USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "106002")  # sandbox default


def get_user_id(tool_context: ToolContext) -> str:
    """
    Resolve the SF userId for the currently logged-in user.

    Sandbox : reads EMAIL_USER_MAP using SF_SANDBOX_USER_ID as fallback.
    Production: reads the Google OAuth token Gemini Enterprise forwards
                via tool_context, calls UserInfo to get the email, then
                maps email prefix → SF userId via EMAIL_USER_MAP.
    """
    if AUTH_MODE == "production":
        # Gemini Enterprise injects the signed-in user's email via tool_context.user_id
        email = tool_context.user_id or ""
        _log(f"[DEBUG] production email from user_id={email!r}")
    else:
        email = os.environ.get("SF_SANDBOX_EMAIL", "")

    if email:
        name = email.split("@")[0].lower()
        uid = EMAIL_USER_MAP.get(name, USER_ID)
        _log(f"[DEBUG] name={name!r} -> uid={uid}")
        return uid

    return USER_ID


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
    if response.status_code == 404:
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
    if response.status_code == 404:
        return {}
    response.raise_for_status()
    return response.json().get("d", {})