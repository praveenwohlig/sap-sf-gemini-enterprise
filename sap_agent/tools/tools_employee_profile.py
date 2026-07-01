"""
tools_employee_profile.py
══════════════════════════════════════════════════════════════
ADK Tools — Employee Profile domain

Entities sourced from two SAP SuccessFactors API specs:
  EC Core (People Profile):
    User                        — login & display info
    PerPersonal                 — personal demographics
    EmpEmployment               — employment record
    PerEmail / PerPhone         — contact details
    PerAddressDEFLT             — home address
    PerEmergencyContacts        — emergency contacts
    PerNationalId               — government / national IDs
    EmpGlobalAssignment         — international assignments
    EmpJob                      — job + org chart position

  Employee Profile (Background Portlets — ECEmployeeProfile API):
    Background_Education            — academic qualifications
    Background_OutsideWorkExperience — previous employers
    Background_InsideWorkExperience  — internal job history
    Background_Certificates         — certifications & licences
    Background_Languages            — language proficiency
    Background_Awards               — recognition & awards
    Background_Memberships          — professional bodies
    Background_SpecialAssign        — special projects
    Background_Courses              — training courses
    Background_Community            — community involvement
    Background_FuncExperience       — functional expertise
    Background_LeadExperience       — leadership experience
    EPPublicProfile                 — public bio & badges flag
    UserBadges                      — recognition badges received
══════════════════════════════════════════════════════════════
"""

from google.adk.tools import ToolContext
from ..sap_sf_config import sf_client


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 1 — Identity & Core Profile
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_profile(tool_context: ToolContext) -> dict:
    """Return the employee's SAP SuccessFactors user profile."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get_single(
        entity="User", entity_id=uid,
    )
    return {"profile": data}


def get_my_personal_details(tool_context: ToolContext) -> dict:
    """Return the employee's personal / demographic information."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="PerPersonal",
        filter=f"personIdExternal eq '{uid}'",
        orderby="startDate desc",
        top=1,
    )
    return {"personal_details": data[0] if data else {}}


def get_my_employment_record(tool_context: ToolContext) -> dict:
    """Return the employee's employment record."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="EmpEmployment",
        filter=f"userId eq '{uid}'",
        top=1,
    )
    return {"employment_record": data[0] if data else {}}


def get_my_public_profile(tool_context: ToolContext) -> dict:
    """Return the employee's public profile bio and settings."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get_single(
        entity="EPPublicProfile", entity_id=uid,
    )
    return {"public_profile": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 2 — Contact Information
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_email_addresses(tool_context: ToolContext) -> dict:
    """Return the employee's email addresses."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="PerEmail",
        filter=f"personIdExternal eq '{uid}'",
        top=10,
    )
    return {"email_addresses": data}


def get_my_phone_numbers(tool_context: ToolContext) -> dict:
    """Return the employee's phone numbers."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="PerPhone",
        filter=f"personIdExternal eq '{uid}'",
        top=10,
    )
    return {"phone_numbers": data}


def get_my_home_address(tool_context: ToolContext) -> dict:
    """Return the employee's home address."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="PerAddressDEFLT",
        filter=f"personIdExternal eq '{uid}'",
        top=10,
    )
    return {"home_address": data}


def get_my_emergency_contacts(tool_context: ToolContext) -> dict:
    """Return the employee's emergency contacts."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="PerEmergencyContacts",
        filter=f"personIdExternal eq '{uid}'",
        top=10,
    )
    return {"emergency_contacts": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 3 — Government IDs & Assignments
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_national_ids(tool_context: ToolContext) -> dict:
    """Return the employee's national / government ID records."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="PerNationalId",
        filter=f"personIdExternal eq '{uid}'",
        top=10,
    )
    return {"national_ids": data}


def get_my_global_assignments(tool_context: ToolContext) -> dict:
    """Return the employee's international / global assignment records."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="EmpGlobalAssignment",
        filter=f"userId eq '{uid}'",
        top=10,
    )
    return {"global_assignments": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 4 — Org Chart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_manager(tool_context: ToolContext) -> dict:
    """Return the employee's direct manager."""
    uid = sf_client.resolve_user_id(tool_context)
    job = sf_client.odata_get(
        entity="EmpJob",
        filter=f"userId eq '{uid}'",
        top=1,
    )
    if not job:
        return {"manager": None}
    manager_id = job[0].get("managerId")
    if not manager_id:
        return {"manager": None}
    manager = sf_client.odata_get_single(
        entity="User", entity_id=manager_id,
    )
    return {"manager": manager}


def get_my_direct_reports(tool_context: ToolContext) -> dict:
    """Return the employees who report directly to this employee."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="EmpJob",
        filter=f"managerId eq '{uid}'",
        top=50,
    )
    return {"direct_reports": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 5 — Education & Qualifications
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_education(tool_context: ToolContext) -> dict:
    """Return the employee's academic / educational background."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Education",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"education": data}


def get_my_certifications(tool_context: ToolContext) -> dict:
    """Return the employee's certifications and professional licences."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Certificates",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"certifications": data}


def get_my_languages(tool_context: ToolContext) -> dict:
    """Return the employee's language proficiency records."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Languages",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"languages": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 6 — Work Experience
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_previous_employers(tool_context: ToolContext) -> dict:
    """Return the employee's external / previous work experience."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_OutsideWorkExperience",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"previous_employers": data}


def get_my_internal_job_history(tool_context: ToolContext) -> dict:
    """Return the employee's internal job history within the company."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_InsideWorkExperience",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"internal_job_history": data}


def get_my_special_projects(tool_context: ToolContext) -> dict:
    """Return the employee's special assignments and project contributions."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_SpecialAssign",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"special_projects": data}


def get_my_training_courses(tool_context: ToolContext) -> dict:
    """Return the employee's completed training courses."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Courses",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"training_courses": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 7 — Skills & Expertise
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_functional_expertise(tool_context: ToolContext) -> dict:
    """Return the employee's declared functional / domain expertise."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_FuncExperience",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"functional_expertise": data}


def get_my_leadership_experience(tool_context: ToolContext) -> dict:
    """Return the employee's leadership and management experience."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_LeadExperience",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"leadership_experience": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 8 — Recognition & Memberships
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_awards(tool_context: ToolContext) -> dict:
    """Return the employee's awards and recognitions."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Awards",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"awards": data}


def get_my_badges(tool_context: ToolContext) -> dict:
    """Return the recognition badges the employee has received."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="UserBadges",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"badges": data}


def get_my_professional_memberships(tool_context: ToolContext) -> dict:
    """Return the employee's professional body / association memberships."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Memberships",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"professional_memberships": data}


def get_my_community_involvement(tool_context: ToolContext) -> dict:
    """Return the employee's community service and volunteer activities."""
    uid = sf_client.resolve_user_id(tool_context)
    data = sf_client.odata_get(
        entity="Background_Community",
        filter=f"userId eq '{uid}'",
        top=20,
    )
    return {"community_involvement": data}
