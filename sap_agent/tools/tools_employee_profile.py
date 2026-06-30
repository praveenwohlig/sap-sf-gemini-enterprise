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

import os
from . import sf_client

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 1 — Identity & Core Profile
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_profile() -> dict:
    """
    Return the employee's SAP SuccessFactors user profile.
    Includes: full name, email, job title, department, location,
    hire date, employment status, time zone, and locale.
    """
    data = sf_client.odata_get_single(
        host=HOST, entity="User", entity_id=USER_ID, api_key=API_KEY,
        select=(
            "userId,username,firstName,lastName,email,title,department,"
            "location,gender,timeZone,defaultLocale,hireDate,status,"
            "displayName,defaultFullName,lastModifiedDateTime"
        ),
    )
    return {"profile": data}


def get_my_personal_details() -> dict:
    """
    Return the employee's personal / demographic information.
    Includes: full name, gender, nationality, date of birth,
    marital status, preferred language, and salutation.
    """
    data = sf_client.odata_get_single(
        host=HOST, entity="PerPersonal", entity_id=USER_ID, api_key=API_KEY,
        select=(
            "personIdExternal,firstName,lastName,middleName,gender,"
            "nationality,dateOfBirth,maritalStatus,nativePreferredLang,"
            "salutation,lastModifiedDateTime"
        ),
    )
    return {"personal_details": data}


def get_my_employment_record() -> dict:
    """
    Return the employee's employment record.
    Includes: start date, seniority date, end date,
    contingent worker flag, employment ID, and assignment class.
    """
    data = sf_client.odata_get_single(
        host=HOST, entity="EmpEmployment", entity_id=USER_ID, api_key=API_KEY,
        select=(
            "userId,startDate,endDate,seniorityDate,isContingentWorker,"
            "employmentId,assignmentClass,lastModifiedDateTime"
        ),
    )
    return {"employment_record": data}


def get_my_public_profile() -> dict:
    """
    Return the employee's public profile bio and settings.
    Includes: introduction text, badges section enabled flag,
    expressive mode, and profile photo permissions.
    """
    data = sf_client.odata_get(
        host=HOST, entity="EPPublicProfile", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,introduction,hasIntroduction,hasMyName,hasAboutMeVideo,"
            "isBadgesSectionEnabled,isAddBadgeAllowed,isExpressiveMode,"
            "liveProfilePhotoPermission,myNameText"
        ),
        top=1,
    )
    return {"public_profile": data[0] if data else {}}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 2 — Contact Information
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_email_addresses() -> dict:
    """
    Return the employee's email addresses.
    Includes: email type (work/personal), address, and primary flag.
    """
    data = sf_client.odata_get(
        host=HOST, entity="PerEmail", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select="personIdExternal,emailType,emailAddress,isPrimary,lastModifiedDateTime",
        top=10,
    )
    return {"email_addresses": data}


def get_my_phone_numbers() -> dict:
    """
    Return the employee's phone numbers.
    Includes: phone type (mobile/work/home), number, and primary flag.
    """
    data = sf_client.odata_get(
        host=HOST, entity="PerPhone", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select="personIdExternal,phoneType,phoneNumber,isPrimary,lastModifiedDateTime",
        top=10,
    )
    return {"phone_numbers": data}


def get_my_home_address() -> dict:
    """
    Return the employee's home address.
    Includes: street lines, city, state, zip code, county, and country.
    """
    data = sf_client.odata_get(
        host=HOST, entity="PerAddressDEFLT", api_key=API_KEY,
        filter=f"personIdExternal eq '{USER_ID}'",
        select=(
            "personIdExternal,addressType,address1,address2,address3,"
            "city,state,zipCode,county,country,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"home_address": data}


def get_my_emergency_contacts() -> dict:
    """
    Return the employee's emergency contacts.
    Includes: name, relationship, phone number, and primary flag.
    """
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 3 — Government IDs & Assignments
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_national_ids() -> dict:
    """
    Return the employee's national / government ID records.
    Includes: country, ID number, card type, and primary flag.
    """
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


def get_my_global_assignments() -> dict:
    """
    Return the employee's international / global assignment records.
    Includes: host company, business unit, division, department,
    start and end dates, and assignment class.
    """
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 4 — Org Chart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_manager() -> dict:
    """
    Return the employee's direct manager.
    Resolves the managerId from the job record, then fetches the
    manager's profile (name, title, department, email).
    """
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


def get_my_direct_reports() -> dict:
    """
    Return the employees who report directly to this employee.
    Includes: userId, job title, department, location, and employment status.
    """
    data = sf_client.odata_get(
        host=HOST, entity="EmpJob", api_key=API_KEY,
        filter=f"managerId eq '{USER_ID}'",
        select="userId,jobTitle,department,location,emplStatus",
        top=50,
    )
    return {"direct_reports": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 5 — Education & Qualifications
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_education() -> dict:
    """
    Return the employee's academic / educational background.
    Includes: school name, degree, major, start/end dates,
    degree date, school city, state, and country.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Education", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,school,degree,major,"
            "startDate,endDate,degreeDate,schoolType,"
            "schoolCity,schoolState,schoolCountry,lastModifiedDate"
        ),
        top=20,
    )
    return {"education": data}


def get_my_certifications() -> dict:
    """
    Return the employee's certifications and professional licences.
    Includes: certificate name, issuing institution, licence number,
    licence country/state, validity start/end dates, and description.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Certificates", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,name,institution,description,"
            "startDate,endDate,licenseName,licenseNumber,"
            "licenseCountry,licenseState,lastModifiedDate"
        ),
        top=20,
    )
    return {"certifications": data}


def get_my_languages() -> dict:
    """
    Return the employee's language proficiency records.
    Includes: language, reading proficiency, speaking proficiency,
    writing proficiency, and language variant.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Languages", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,language,variant,"
            "readingProf,speakingProf,writingProf,lastModifiedDate"
        ),
        top=20,
    )
    return {"languages": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 6 — Work Experience
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_previous_employers() -> dict:
    """
    Return the employee's external / previous work experience.
    Includes: employer name, start/end dates, job title at start,
    employer city, country, and contact information.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_OutsideWorkExperience", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,employer,startTitle,"
            "startDate,endDate,presentEmployer,"
            "employerCity,employerState,employerCountry,"
            "employerPhone,employerEmail,businessType,lastModifiedDate"
        ),
        top=20,
    )
    return {"previous_employers": data}


def get_my_internal_job_history() -> dict:
    """
    Return the employee's internal job history within the company.
    Includes: previous job title, department, start date, and end date.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_InsideWorkExperience", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,title,department,"
            "startDate,endDate,lastModifiedDate"
        ),
        top=20,
    )
    return {"internal_job_history": data}


def get_my_special_projects() -> dict:
    """
    Return the employee's special assignments and project contributions.
    Includes: project name, description, start and end dates.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_SpecialAssign", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,project,description,"
            "startDate,endDate,lastModifiedDate"
        ),
        top=20,
    )
    return {"special_projects": data}


def get_my_training_courses() -> dict:
    """
    Return the employee's completed training courses.
    Includes: course name, institution, instruction type,
    course length, and end date.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Courses", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,course,institution,"
            "instructionType,length,endDate,lastModifiedDate"
        ),
        top=20,
    )
    return {"training_courses": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 7 — Skills & Expertise
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_functional_expertise() -> dict:
    """
    Return the employee's declared functional / domain expertise.
    Includes: experience area, years of experience, and comments.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_FuncExperience", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,experience,years,"
            "comments,lastModifiedDate"
        ),
        top=20,
    )
    return {"functional_expertise": data}


def get_my_leadership_experience() -> dict:
    """
    Return the employee's leadership and management experience.
    Includes: leadership experience type, years led, number of people
    managed, budget managed (dollars), and comments.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_LeadExperience", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,experience,years,"
            "people,dollars,comments,lastModifiedDate"
        ),
        top=20,
    )
    return {"leadership_experience": data}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section 8 — Recognition & Memberships
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_my_awards() -> dict:
    """
    Return the employee's awards and recognitions.
    Includes: award name, issuing institution, issue date, and description.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Awards", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,name,institution,"
            "issueDate,description,lastModifiedDate"
        ),
        top=20,
    )
    return {"awards": data}


def get_my_badges() -> dict:
    """
    Return the recognition badges the employee has received.
    Includes: badge title, giver name, comment, and badge ID.
    """
    data = sf_client.odata_get(
        host=HOST, entity="UserBadges", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "badgeInstanceId,userId,badgeId,badgeTitle,"
            "badgeCreatorName,creatorUserID,comment,lastModified"
        ),
        top=20,
    )
    return {"badges": data}


def get_my_professional_memberships() -> dict:
    """
    Return the employee's professional body / association memberships.
    Includes: organization name, role, start date, and end date.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Memberships", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,organization,role,"
            "startDate,endDate,lastModifiedDate"
        ),
        top=20,
    )
    return {"professional_memberships": data}


def get_my_community_involvement() -> dict:
    """
    Return the employee's community service and volunteer activities.
    Includes: community name, role, start date, and end date.
    """
    data = sf_client.odata_get(
        host=HOST, entity="Background_Community", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "backgroundElementId,userId,name,role,"
            "startDate,endDate,lastModifiedDate"
        ),
        top=20,
    )
    return {"community_involvement": data}
