"""
tools_payroll_time.py
══════════════════════════════════════════════════════════════
ADK Tools — Payroll & Time Sheet domain

Entities sourced from ECPayrollTimeSheets.json (Swagger spec):
  EmployeeTimeSheet         — weekly/period timesheet header
  EmployeeTimeSheetEntry    — individual time entries per day
  EmployeeTimeValuationResult — valuation (hours, pay type)
  TimeCollector             — running time collector balances
  TimeRecording             — clock-in/clock-out records
  AllowanceRecording        — on-call / overtime allowances
  ExternalAllowance         — externally imported allowances
  ExternalTimeData          — externally imported time data

Plus existing EC payroll entities:
  EmpJob                    — job info (foundational for payroll)
  EmpCompensation           — compensation snapshot
  EmpPayCompRecurring       — recurring pay components
  EmployeeTime              — absence/time-off records
  TimeAccount               — leave balances
  EmpBeneficiary            — beneficiary records
══════════════════════════════════════════════════════════════
"""

from sap_sf_config import sf_client


# ── Job Info ──────────────────────────────────────────────────────────────────

def get_my_job() -> dict:
    """Return the employee's current job info (title, department, pay grade, manager)."""
    data = sf_client.odata_get(
        entity="EmpJob",
        filter=f"userId eq '{sf_client.USER_ID}'",
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
    """Return the employee's compensation snapshot (pay grade, bonus target, benefits eligibility)."""
    data = sf_client.odata_get(
        entity="EmpCompensation",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "userId,startDate,endDate,seqNumber,payType,payGrade,payGroup,"
            "bonusTarget,benefitsRate,isEligibleForBenefits,isEligibleForCar,"
            "isHighlyCompensatedEmployee,event,eventReason,lastModifiedDateTime"
        ),
        top=1,
    )
    return {"compensation": data}


def get_my_pay_components() -> dict:
    """Return the employee's recurring pay components (base salary, allowances, currency, frequency)."""
    data = sf_client.odata_get(
        entity="EmpPayCompRecurring",
        filter=f"userId eq '{sf_client.USER_ID}'",
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
        entity="EmpBeneficiary",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "userId,startDate,endDate,benefitType,firstName,lastName,"
            "relationship,percentage,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"beneficiaries": data}


# ── Time Off & Leave ──────────────────────────────────────────────────────────

def get_my_time_off() -> dict:
    """Return the employee's absence / time-off records (vacation, sick leave, approval status)."""
    data = sf_client.odata_get(
        entity="EmployeeTime",
        filter=f"userId eq '{sf_client.USER_ID}'",
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
        entity="TimeAccount",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "userId,timeAccountType,balance,bookingEndDate,"
            "accountClosed,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"leave_balances": data}


# ── Time Sheets (ECPayrollTimeSheets API) ─────────────────────────────────────

def get_my_timesheets() -> dict:
    """Return the employee's timesheet headers (period, planned vs recorded hours, approval status)."""
    data = sf_client.odata_get(
        entity="EmployeeTimeSheet",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "externalCode,userId,startDate,endDate,period,"
            "approvalStatus,plannedWorkingTime,plannedWorkingTimeInDays,"
            "plannedHoursAndMinutes,recordedWorkingTime,recordedWorkingTimeInDays,"
            "recordedHoursAndMinutes,workingTimeAccount,workingTimeAccountHoursAndMinutes,"
            "timeRecordingMethod,manualEntriesExist,absencesExist,"
            "editable,lastModifiedDateTime"
        ),
        top=10,
    )
    return {"timesheets": data}


def get_my_timesheet_entries() -> dict:
    """Return the employee's individual timesheet entries (date, time type, start/end time, hours worked)."""
    data = sf_client.odata_get(
        entity="EmployeeTimeSheetEntry",
        filter=f"EmployeeTimeSheet_externalCode ne ''",
        select=(
            "externalCode,EmployeeTimeSheet_externalCode,startDate,"
            "startTime,endTime,physicalStartDate,physicalEndDate,"
            "timeType,timeTypeName,quantityInHours,quantityInHoursAndMinutes,"
            "durationInDays,costCenter,approvalStatus,timeRecordOrigin,"
            "lastModifiedDateTime"
        ),
        top=20,
    )
    return {"timesheet_entries": data}


def get_my_time_valuation() -> dict:
    """Return the employee's time valuation results (hours valued, pay type, allowance type, posting target)."""
    data = sf_client.odata_get(
        entity="EmployeeTimeValuationResult",
        filter=f"EmployeeTimeSheet_externalCode ne ''",
        select=(
            "externalCode,EmployeeTimeSheet_externalCode,bookingDate,"
            "hours,hoursAndMinutes,allowanceType,approvalStatus,"
            "payTypeName,payTypeExternalName,postingTarget,"
            "timeTypeGroup,costCenter,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"time_valuation": data}


def get_my_time_collector() -> dict:
    """Return the employee's time collector balances (overtime bank, flexi-time balance, collector value)."""
    data = sf_client.odata_get(
        entity="TimeCollector",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "externalCode,userId,timeCollectorType,startDate,endDate,"
            "bookingDate,collectorValue,changeValue,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"time_collectors": data}


def get_my_time_recordings() -> dict:
    """Return the employee's clock-in/clock-out time recording entries (date, start time, end time, time type)."""
    data = sf_client.odata_get(
        entity="TimeRecording",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "externalCode,userId,date,startTime,endTime,"
            "physicalStartDate,physicalEndDate,timeType,"
            "durationInMinutes,durationInDays,costCenter,"
            "approvalPeriodStatus,timeRecordOrigin,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"time_recordings": data}


def get_my_allowance_recordings() -> dict:
    """Return the employee's allowance recordings (on-call, overtime, allowance type, date, value)."""
    data = sf_client.odata_get(
        entity="AllowanceRecording",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "externalCode,userId,date,allowanceType,value,"
            "costCenter,approvalPeriodStatus,pendingCancellation,"
            "lastModifiedDateTime"
        ),
        top=20,
    )
    return {"allowance_recordings": data}


def get_my_external_allowances() -> dict:
    """Return the employee's externally imported allowances (allowance type, date, value, status)."""
    data = sf_client.odata_get(
        entity="ExternalAllowance",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "externalCode,userId,date,allowanceType,value,"
            "costCenter,status,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"external_allowances": data}


def get_my_external_time_data() -> dict:
    """Return the employee's externally imported time data (date, time type, hours, start/end time, status)."""
    data = sf_client.odata_get(
        entity="ExternalTimeData",
        filter=f"userId eq '{sf_client.USER_ID}'",
        select=(
            "externalCode,userId,startDate,endDate,startTime,endTime,"
            "timeType,hours,costCenter,status,category,"
            "externalApprovalStatus,lastModifiedDateTime"
        ),
        top=20,
    )
    return {"external_time_data": data}