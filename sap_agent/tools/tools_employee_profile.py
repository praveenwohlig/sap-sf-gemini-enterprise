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

from sap_sf_config import sf_client


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 1 — Identity & Core Profile
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_profile() -> dict:
    """Return the employee's SAP SuccessFactors user profile."""
    data = sf_client.odata_get_single(
        entity="User", entity_id=sf_client.USER_ID,
    )
    return {"profile": data}


def get_my_personal_details() -> dict:
    """Return the employee's personal / demographic information."""
    data = sf_client.odata_get_single(
        entity="PerPersonal", entity_id=sf_client.USER_ID,
    )
    return {"personal_details": data}


def get_my_employment_record() -> dict:
    """Return the employee's employment record."""
    data = sf_client.odata_get(
        entity="EmpEmployment",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=1,
    )
    return {"employment_record": data[0] if data else {}}


def get_my_public_profile() -> dict:
    """Return the employee's public profile bio and settings."""
    data = sf_client.odata_get_single(
        entity="EPPublicProfile", entity_id=sf_client.USER_ID,
    )
    return {"public_profile": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 2 — Contact Information
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_email_addresses() -> dict:
    """Return the employee's email addresses."""
    data = sf_client.odata_get(
        entity="PerEmail",
        filter=f"personIdExternal eq '{sf_client.USER_ID}'",
        top=10,
    )
    return {"email_addresses": data}


def get_my_phone_numbers() -> dict:
    """Return the employee's phone numbers."""
    data = sf_client.odata_get(
        entity="PerPhone",
        filter=f"personIdExternal eq '{sf_client.USER_ID}'",
        top=10,
    )
    return {"phone_numbers": data}


def get_my_home_address() -> dict:
    """Return the employee's home address."""
    data = sf_client.odata_get(
        entity="PerAddressDEFLT",
        filter=f"personIdExternal eq '{sf_client.USER_ID}'",
        top=10,
    )
    return {"home_address": data}


def get_my_emergency_contacts() -> dict:
    """Return the employee's emergency contacts."""
    data = sf_client.odata_get(
        entity="PerEmergencyContacts",
        filter=f"personIdExternal eq '{sf_client.USER_ID}'",
        top=10,
    )
    return {"emergency_contacts": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 3 — Government IDs & Assignments
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_national_ids() -> dict:
    """Return the employee's national / government ID records."""
    data = sf_client.odata_get(
        entity="PerNationalId",
        filter=f"personIdExternal eq '{sf_client.USER_ID}'",
        top=10,
    )
    return {"national_ids": data}


def get_my_global_assignments() -> dict:
    """Return the employee's international / global assignment records."""
    data = sf_client.odata_get(
        entity="EmpGlobalAssignment",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=10,
    )
    return {"global_assignments": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 4 — Org Chart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_manager() -> dict:
    """Return the employee's direct manager."""
    job = sf_client.odata_get(
        entity="EmpJob",
        filter=f"userId eq '{sf_client.USER_ID}'",
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


def get_my_direct_reports() -> dict:
    """Return the employees who report directly to this employee."""
    data = sf_client.odata_get(
        entity="EmpJob",
        filter=f"managerId eq '{sf_client.USER_ID}'",
        top=50,
    )
    return {"direct_reports": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 5 — Education & Qualifications
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_education() -> dict:
    """Return the employee's academic / educational background."""
    data = sf_client.odata_get(
        entity="Background_Education",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"education": data}


def get_my_certifications() -> dict:
    """Return the employee's certifications and professional licences."""
    data = sf_client.odata_get(
        entity="Background_Certificates",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"certifications": data}


def get_my_languages() -> dict:
    """Return the employee's language proficiency records."""
    data = sf_client.odata_get(
        entity="Background_Languages",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"languages": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 6 — Work Experience
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_previous_employers() -> dict:
    """Return the employee's external / previous work experience."""
    data = sf_client.odata_get(
        entity="Background_OutsideWorkExperience",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"previous_employers": data}


def get_my_internal_job_history() -> dict:
    """Return the employee's internal job history within the company."""
    data = sf_client.odata_get(
        entity="Background_InsideWorkExperience",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"internal_job_history": data}


def get_my_special_projects() -> dict:
    """Return the employee's special assignments and project contributions."""
    data = sf_client.odata_get(
        entity="Background_SpecialAssign",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"special_projects": data}


def get_my_training_courses() -> dict:
    """Return the employee's completed training courses."""
    data = sf_client.odata_get(
        entity="Background_Courses",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"training_courses": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 7 — Skills & Expertise
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_functional_expertise() -> dict:
    """Return the employee's declared functional / domain expertise."""
    data = sf_client.odata_get(
        entity="Background_FuncExperience",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"functional_expertise": data}


def get_my_leadership_experience() -> dict:
    """Return the employee's leadership and management experience."""
    data = sf_client.odata_get(
        entity="Background_LeadExperience",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"leadership_experience": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 8 — Recognition & Memberships
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_awards() -> dict:
    """Return the employee's awards and recognitions."""
    data = sf_client.odata_get(
        entity="Background_Awards",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"awards": data}


def get_my_badges() -> dict:
    """Return the recognition badges the employee has received."""
    data = sf_client.odata_get(
        entity="UserBadges",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"badges": data}


def get_my_professional_memberships() -> dict:
    """Return the employee's professional body / association memberships."""
    data = sf_client.odata_get(
        entity="Background_Memberships",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"professional_memberships": data}


def get_my_community_involvement() -> dict:
    """Return the employee's community service and volunteer activities."""
    data = sf_client.odata_get(
        entity="Background_Community",
        filter=f"userId eq '{sf_client.USER_ID}'",
        top=20,
    )
    return {"community_involvement": data}
