"""
tools_employee_profile.py
══════════════════════════════════════════════════════════════
ADK Tools — Employee Profile domain

Covers: User, PerPersonal, EmpEmployment, PerEmail, PerPhone,
        PerAddressDEFLT, PerEmergencyContacts, PerNationalId,
        EmpGlobalAssignment, manager lookup, direct reports.
══════════════════════════════════════════════════════════════
"""

import os
from . import sf_client

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")


# ── Profile & Identity ────────────────────────────────────────────────────────

def get_my_profile() -> dict:
    """Return the employee's SAP SuccessFactors profile (name, email, title, status)."""
    data = sf_client.odata_get_single(
        host=HOST, entity="User", entity_id=USER_ID, api_key=API_KEY,
        select=(
            "userId,username,firstName,lastName,email,title,department,"
            "location,gender,timeZone,defaultLocale,hireDate,status,"
            "displayName,defaultFullName,lastModifiedDateTime"
        ),
    )
    return {"profile": data}


def get_my_personal() -> dict:
    """Return the employee's personal info (name, gender, nationality, DOB, marital status)."""
    data = sf_client.odata_get_single(
        host=HOST, entity="PerPersonal", entity_id=USER_ID, api_key=API_KEY,
        select=(
            "personIdExternal,firstName,lastName,middleName,gender,"
            "nationality,dateOfBirth,maritalStatus,nativePreferredLang,"
            "salutation,lastModifiedDateTime"
        ),
    )
    return {"personal": data}


def get_my_employment() -> dict:
    """Return the employee's employment record (start date, seniority, contingent worker flag)."""
    data = sf_client.odata_get_single(
        host=HOST, entity="EmpEmployment", entity_id=USER_ID, api_key=API_KEY,
        select=(
            "userId,startDate,endDate,seniorityDate,isContingentWorker,"
            "employmentId,assignmentClass,lastModifiedDateTime"
        ),
    )
    return {"employment": data}


# ── Contact Details ───────────────────────────────────────────────────────────

def get_my_email() -> dict:
    """Return the employee's email address records (email type, address, primary flag)."""
    data = sf_client.odata_get(
        host=HOST, entity="PerEmail", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select="personIdExternal,emailType,emailAddress,isPrimary,lastModifiedDateTime",
        top=10,
    )
    return {"emails": data}


def get_my_phone() -> dict:
    """Return the employee's phone number records (phone type, number, primary flag)."""
    data = sf_client.odata_get(
        host=HOST, entity="PerPhone", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select="personIdExternal,phoneType,phoneNumber,isPrimary,lastModifiedDateTime",
        top=10,
    )
    return {"phones": data}


def get_my_address() -> dict:
    """Return the employee's home address (street, city, state, zip, country)."""
    data = sf_client.odata_get(
        host=HOST, entity="PerAddressDEFLT", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select=(
            "personIdExternal,addressType,address1,address2,address3,"
            "city,state,zipCode,county,country,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"addresses": data}


def get_my_emergency_contacts() -> dict:
    """Return the employee's emergency contacts (name, relationship, phone)."""
    data = sf_client.odata_get(
        host=HOST, entity="PerEmergencyContacts", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select=(
            "personIdExternal,firstName,lastName,relationship,"
            "phone,isPrimary,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"emergency_contacts": data}


# ── IDs & Assignments ─────────────────────────────────────────────────────────

def get_my_national_id() -> dict:
    """Return the employee's national / government ID records (country, ID number, card type)."""
    data = sf_client.odata_get(
        host=HOST, entity="PerNationalId", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select=(
            "personIdExternal,country,nationalId,cardType,"
            "isPrimary,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"national_ids": data}


def get_my_global_assignment() -> dict:
    """Return the employee's global assignment records (host company, start/end dates)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmpGlobalAssignment", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,startDate,endDate,assignmentClass,hostCompany,"
            "hostBusinessUnit,hostDivision,hostDepartment,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"global_assignments": data}


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
    manager = sf_client.odata_get_single(
        host=HOST, entity="User", entity_id=manager_id, api_key=API_KEY,
        select=(
            "userId,username,firstName,lastName,email,title,"
            "department,location,displayName,lastModifiedDateTime"
        ),
    )
    return {"manager": manager}


def list_direct_reports() -> dict:
    """Return the employees who report directly to this employee (org chart)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmpJob", api_key=API_KEY,
        filter=f"managerId eq '{USER_ID}'",
        select="userId,jobTitle,department,location,emplStatus",
        top=50,
    )
    return {"direct_reports": data}
