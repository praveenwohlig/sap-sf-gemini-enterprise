"""
tools_payroll_time.py
══════════════════════════════════════════════════════════════
ADK Tools — Payroll & Time domain

Covers: EmpJob, EmpCompensation, EmpPayCompRecurring,
        EmployeeTime, TimeAccount, EmpBeneficiary.
══════════════════════════════════════════════════════════════
"""

import os
from . import sf_client

HOST    = os.environ["SF_SANDBOX_HOST"]
API_KEY = os.environ["SF_SANDBOX_API_KEY"]
USER_ID = os.environ.get("SF_SANDBOX_USER_ID", "103075")


# ── Job Info ──────────────────────────────────────────────────────────────────

def get_my_job() -> dict:
    """Return the employee's current job info (title, department, pay grade, manager)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmpJob", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,jobTitle,department,location,startDate,emplStatus,"
            "position,jobCode,payGrade,payGroup,managerId,companyId,"
            "businessUnit,division,costCenter,fullPartTime,regularTemp"
        ),
        top=1,
    )
    return {"job": data}


# ── Compensation ──────────────────────────────────────────────────────────────

def get_my_compensation() -> dict:
    """Return the employee's compensation info (pay grade, bonus target, benefits eligibility)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmpCompensation", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,startDate,endDate,seqNumber,payType,payGrade,payGroup,"
            "bonusTarget,benefitsRate,isEligibleForBenefits,isEligibleForCar,"
            "isHighlyCompensatedEmployee,event,eventReason,lastModifiedDateTime"
        ),
        top=1,
    )
    return {"compensation": data}


def get_my_pay_components() -> dict:
    """Return the employee's recurring pay components (base salary, allowances, currency)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmpPayCompRecurring", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,startDate,endDate,payComponent,payComponentValue,"
            "currency,frequencyCode,seqNumber,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"pay_components": data}


def get_my_beneficiaries() -> dict:
    """Return the employee's beneficiary records (benefit type, name, relationship, percentage)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmpBeneficiary", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,startDate,endDate,benefitType,firstName,lastName,"
            "relationship,percentage,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"beneficiaries": data}


# ── Time Off & Leave ──────────────────────────────────────────────────────────

def get_my_time_off() -> dict:
    """Return the employee's time-off / absence records (vacation, sick leave, approval status)."""
    data = sf_client.odata_get(
        host=HOST, entity="EmployeeTime", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,startDate,endDate,timeType,quantityInDays,"
            "quantityInHours,approvalStatus,deductionQuantity,"
            "comment,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"time_off": data}


def get_my_leave_balance() -> dict:
    """Return the employee's leave account balances (vacation balance, sick leave balance)."""
    data = sf_client.odata_get(
        host=HOST, entity="TimeAccount", api_key=API_KEY,
        filter=f"userId eq '{USER_ID}'",
        select=(
            "userId,timeAccountType,balance,bookingEndDate,"
            "accountClosed,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"leave_balances": data}
