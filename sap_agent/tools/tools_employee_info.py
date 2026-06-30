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

import os
from . import sf_client

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")


# ── EmpEmploymentTermination ──────────────────────────────────────────────────

def get_my_employment_termination(user_id: str = USER_ID) -> dict:
    """Return the employee's employment termination details (end date, event reason, rehire eligibility, benefit end dates).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    # Composite key: (endDate, personIdExternal, userId) — use collection filter
    data = sf_client.odata_get(
        host=HOST, entity="EmpEmploymentTermination", api_key=API_KEY,
        filter=f"userId eq '{user_id}'",
        select=(
            "personIdExternal,userId,endDate,eventReason,"
            "lastDateWorked,okToRehire,regretTermination,"
            "eligibleForSalContinuation,benefitsEndDate,"
            "salaryEndDate,payrollEndDate,bonusPayExpirationDate,"
            "notes,lastModifiedDateTime"
        ),
        top=5,
    )
    return {"employment_termination": data}


# ── EmpPensionPayout ──────────────────────────────────────────────────────────

def get_my_pension_payout(user_id: str = USER_ID) -> dict:
    """Return the employee's pension payout information (payout schedule, planned end date, payroll end date).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    # Key: userId (single string key)
    data = sf_client.odata_get(
        host=HOST, entity="EmpPensionPayout", api_key=API_KEY,
        filter=f"userId eq '{user_id}'",
        select=(
            "personIdExternal,userId,startDate,endDate,"
            "plannedEndDate,payrollEndDate,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"pension_payout": data}


# ── EmpWorkPermit ─────────────────────────────────────────────────────────────

def get_my_work_permits(
    user_id: str = USER_ID,
    country: str = None,
) -> dict:
    """Return the employee's work permit records (country, document type/number/title, issue/expiration dates, issuing authority).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
        country: Filter by country code, e.g. 'USA' (optional).
    """
    # Composite key: (country, documentNumber, documentType, userId)
    filter_expr = f"userId eq '{user_id}'"
    if country:
        filter_expr += f" and country eq '{country}'"

    data = sf_client.odata_get(
        host=HOST, entity="EmpWorkPermit", api_key=API_KEY,
        filter=filter_expr,
        select=(
            "userId,country,documentType,documentNumber,documentTitle,"
            "issueDate,expirationDate,isValidated,"
            "issuePlace,issuingAuthority,notes,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"work_permits": data}


# ── EmpJobRelationships ───────────────────────────────────────────────────────

def get_my_job_relationships(
    user_id: str = USER_ID,
    relationship_type: str = None,
) -> dict:
    """Return the employee's job relationship records (relationship type, related user ID, effective dates, operation).

    Args:
        user_id:           Employee user ID to look up. Defaults to the logged-in user.
        relationship_type: Filter by type, e.g. 'hr manager' (optional).
    """
    # Composite key: (relationshipType, startDate, userId)
    filter_expr = f"userId eq '{user_id}'"
    if relationship_type:
        filter_expr += f" and relationshipType eq '{relationship_type}'"

    data = sf_client.odata_get(
        host=HOST, entity="EmpJobRelationships", api_key=API_KEY,
        filter=filter_expr,
        select=(
            "userId,relationshipType,startDate,endDate,"
            "relUserId,operation,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"job_relationships": data}


# ── HireDateChange ────────────────────────────────────────────────────────────

def get_my_hire_date_changes(user_id: str = USER_ID) -> dict:
    """Return the employee's hire date change records (original hire date, new hire date, processing status, record status).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    # Key: code (single string key); filter by usersSysId for per-user lookup
    data = sf_client.odata_get(
        host=HOST, entity="HireDateChange", api_key=API_KEY,
        filter=f"usersSysId eq '{user_id}'",
        select=(
            "code,originalHireDate,newHireDate,processingStatus,"
            "mdfSystemRecordStatus,usersSysId,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"hire_date_changes": data}


# ── PersonEmpTerminationInfo ──────────────────────────────────────────────────

def get_my_person_emp_termination_info(user_id: str = USER_ID) -> dict:
    """Return the person-level termination summary (active employment count, latest termination date).

    Args:
        user_id: Employee's personIdExternal to look up. Defaults to the logged-in user.
    """
    # Key: personIdExternal (single string key)
    data = sf_client.odata_get_single(
        host=HOST, entity="PersonEmpTerminationInfo", entity_id=user_id,
        api_key=API_KEY,
        select=(
            "personIdExternal,activeEmploymentsCount,latestTerminationDate"
        ),
    )
    return {"person_emp_termination_info": data}
