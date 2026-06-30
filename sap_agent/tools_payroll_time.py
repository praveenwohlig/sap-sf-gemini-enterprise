"""
tools_payroll_time.py
══════════════════════════════════════════════════════════════
ADK Tools — Payroll & Time domain

Covers: EmpJob, EmpCompensation, EmpPayCompRecurring,
        EmployeeTime, TimeAccount, EmpBeneficiary.

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


# ── Job Info ──────────────────────────────────────────────────────────────────

def get_my_job() -> dict:
    """Return the employee's current job info (title, department, pay grade, manager)."""
    return _fetch("get_my_job")


# ── Compensation ──────────────────────────────────────────────────────────────

def get_my_compensation() -> dict:
    """Return the employee's compensation info (pay grade, bonus target, benefits eligibility)."""
    return _fetch("get_my_compensation")


def get_my_pay_components() -> dict:
    """Return the employee's recurring pay components (base salary, allowances, currency)."""
    return _fetch("get_my_pay_components")


def get_my_beneficiaries() -> dict:
    """Return the employee's beneficiary records (benefit type, name, relationship, percentage)."""
    return _fetch("get_my_beneficiaries")


# ── Time Off & Leave ──────────────────────────────────────────────────────────

def get_my_time_off() -> dict:
    """Return the employee's time-off / absence records (vacation, sick leave, approval status)."""
    return _fetch("get_my_time_off")


def get_my_leave_balance() -> dict:
    """Return the employee's leave account balances (vacation balance, sick leave balance)."""
    return _fetch("get_my_leave_balance")
