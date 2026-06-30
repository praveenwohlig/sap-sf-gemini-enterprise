"""
tools_employee_profile.py
══════════════════════════════════════════════════════════════
ADK Tools — Employee Profile domain

Covers: User, PerPersonal, EmpEmployment, PerEmail, PerPhone,
        PerAddressDEFLT, PerEmergencyContacts, PerNationalId,
        EmpGlobalAssignment, manager lookup, direct reports.

Field lists and entity names live in entity_config.py.
No hardcoded strings here.
══════════════════════════════════════════════════════════════
"""

import os
from . import sf_client
from .entity_config import ENTITY_BY_TOOL

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")


def _fetch(tool_name: str) -> dict:
    cfg    = ENTITY_BY_TOOL[tool_name]
    select = ",".join(cfg["select"])
    key    = cfg["result_key"]

    if cfg["filter_by"] is None:
        data = sf_client.odata_get_single(
            host=HOST, entity=cfg["name"], entity_id=USER_ID,
            api_key=API_KEY, select=select,
        )
    else:
        data = sf_client.odata_get(
            host=HOST, entity=cfg["name"], api_key=API_KEY,
            filter=f"{cfg['filter_by']} eq '{USER_ID}'",
            select=select, top=cfg["top"],
        )
    return {key: data}


# ── Profile & Identity ────────────────────────────────────────────────────────

def get_my_profile() -> dict:
    """Return the employee's SAP SuccessFactors profile (name, email, title, status)."""
    return _fetch("get_my_profile")


def get_my_personal() -> dict:
    """Return the employee's personal info (name, gender, nationality, DOB, marital status)."""
    return _fetch("get_my_personal")


def get_my_employment() -> dict:
    """Return the employee's employment record (start date, seniority, contingent worker flag)."""
    return _fetch("get_my_employment")


# ── Contact Details ───────────────────────────────────────────────────────────

def get_my_email() -> dict:
    """Return the employee's email address records (email type, address, primary flag)."""
    return _fetch("get_my_email")


def get_my_phone() -> dict:
    """Return the employee's phone number records (phone type, number, primary flag)."""
    return _fetch("get_my_phone")


def get_my_address() -> dict:
    """Return the employee's home address (street, city, state, zip, country)."""
    return _fetch("get_my_address")


def get_my_emergency_contacts() -> dict:
    """Return the employee's emergency contacts (name, relationship, phone)."""
    return _fetch("get_my_emergency_contacts")


# ── IDs & Assignments ─────────────────────────────────────────────────────────

def get_my_national_id() -> dict:
    """Return the employee's national / government ID records (country, ID number, card type)."""
    return _fetch("get_my_national_id")


def get_my_global_assignment() -> dict:
    """Return the employee's global assignment records (host company, start/end dates)."""
    return _fetch("get_my_global_assignment")


# ── Org Chart ─────────────────────────────────────────────────────────────────

def get_my_manager() -> dict:
    """Return the employee's manager details by resolving managerId from the job record."""
    job = sf_client.odata_get(
        host=HOST, entity="EmpJob", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'", select="userId,managerId", top=1,
    )
    if not job:
        return {"manager": None}
    manager_id = job[0].get("managerId")
    if not manager_id:
        return {"manager": None}
    profile_cfg = ENTITY_BY_TOOL["get_my_profile"]
    manager = sf_client.odata_get_single(
        host=HOST, entity="User", entity_id=manager_id,
        api_key=API_KEY, select=",".join(profile_cfg["select"]),
    )
    return {"manager": manager}


def list_direct_reports() -> dict:
    """Return the employees who report directly to this employee (org chart)."""
    reports = sf_client.odata_get(
        host=HOST, entity="EmpJob", api_key=API_KEY,
        filter=f"managerId eq '{USER_ID}'",
        select="userId,jobTitle,department,location,emplStatus",
        top=50,
    )
    return {"direct_reports": reports}
