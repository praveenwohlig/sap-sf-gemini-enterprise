"""
tools_employee_info.py
══════════════════════════════════════════════════════════════
ADK Tools — Employee Information domain

Entities covered (add more below following the same pattern):
  EmpEmploymentTermination  get_my_employment_termination()
  EmpPensionPayout          get_my_pension_payout()
  EmpWorkPermit             get_my_work_permits()
  EmpJobRelationships       get_my_job_relationships()
  HireDateChange            get_my_hire_date_changes()
  PersonEmpTerminationInfo  get_my_person_emp_termination_info()

Field lists match the ECEmploymentInformation OData spec ($select enums).
══════════════════════════════════════════════════════════════
"""

from google.adk.tools import ToolContext
from ..sap_sf_config import sf_client


# ── EmpEmploymentTermination ──────────────────────────────────────────────────

def get_my_employment_termination(tool_context: ToolContext, user_id: str | None = None) -> dict:
    """Return the employee's employment termination details (end date, event reason, rehire eligibility, benefit end dates).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="EmpEmploymentTermination",
        filter=f"userId eq '{uid}'",
        top=5,
    )
    return {"employment_termination": data}


# ── EmpPensionPayout ──────────────────────────────────────────────────────────

def get_my_pension_payout(tool_context: ToolContext, user_id: str | None = None) -> dict:
    """Return the employee's pension payout information (payout schedule, planned end date, payroll end date).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get_single(
        entity="EmpPensionPayout",
        entity_id=uid,
    )
    return {"pension_payout": data}


# ── EmpWorkPermit ─────────────────────────────────────────────────────────────

def get_my_work_permits(
    tool_context: ToolContext,
    user_id: str | None = None,
    country: str | None = None,
) -> dict:
    """Return the employee's work permit records (country, document type/number/title, issue/expiration dates, issuing authority).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
        country: Filter by country code, e.g. 'USA' (optional).
    """
    uid = user_id or sf_client.resolve_user_id(tool_context)
    filter_expr = f"userId eq '{uid}'"
    if country:
        filter_expr += f" and country eq '{country}'"

    data = sf_client.odata_get(
        entity="EmpWorkPermit",
        filter=filter_expr,
        top=10,
    )
    return {"work_permits": data}


# ── EmpJobRelationships ───────────────────────────────────────────────────────

def get_my_job_relationships(
    tool_context: ToolContext,
    user_id: str | None = None,
    relationship_type: str | None = None,
) -> dict:
    """Return the employee's job relationship records (relationship type, related user ID, effective dates, operation).

    Args:
        user_id:           Employee user ID to look up. Defaults to the logged-in user.
        relationship_type: Filter by type, e.g. 'hr manager' (optional).
    """
    uid = user_id or sf_client.resolve_user_id(tool_context)
    filter_expr = f"userId eq '{uid}'"
    if relationship_type:
        filter_expr += f" and relationshipType eq '{relationship_type}'"

    data = sf_client.odata_get(
        entity="EmpJobRelationships",
        filter=filter_expr,
        top=20,
    )
    return {"job_relationships": data}


# ── HireDateChange ────────────────────────────────────────────────────────────

def get_my_hire_date_changes(tool_context: ToolContext, user_id: str | None = None) -> dict:
    """Return the employee's hire date change records (original hire date, new hire date, processing status, record status).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="HireDateChange",
        filter=f"usersSysId eq '{uid}'",
        top=10,
    )
    return {"hire_date_changes": data}


# ── PersonEmpTerminationInfo ──────────────────────────────────────────────────

def get_my_person_emp_termination_info(tool_context: ToolContext, user_id: str | None = None) -> dict:
    """Return the person-level termination summary (active employment count, latest termination date).

    Args:
        user_id: Employee's personIdExternal to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get_single(
        entity="PersonEmpTerminationInfo", entity_id=uid,
    )
    return {"person_emp_termination_info": data}
