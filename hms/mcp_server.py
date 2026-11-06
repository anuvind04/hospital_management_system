import os
import sys
import json
from pathlib import Path
from asgiref.sync import sync_to_async
from django.db.models import F

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "hms.settings"
)

import django
django.setup()

from mcp.server.fastmcp import FastMCP
from home.models import booking, dept, doctor

mcp = FastMCP("Hospital Management Server")


@sync_to_async
def get_departments():
    return list(
        dept.objects.order_by("dept_name").values(
            "id",
            "dept_name",
            "dept_desc",
        )
    )


@sync_to_async
def get_doctors():
    return list(
        doctor.objects.order_by("doctor_name").values(
            "id",
            "doctor_name",
            "doctor_specialisation",
            department=F("dept_name__dept_name"),
        )[:50]
    )


@sync_to_async
def get_appointment_count():
    return booking.objects.count()


@mcp.tool()
async def list_departments() -> str:
    """List hospital departments and their descriptions."""
    departments = await get_departments()
    return json.dumps(departments)


@mcp.tool()
async def list_doctors() -> str:
    """List doctors with their specialties and departments."""
    doctors = await get_doctors()
    return json.dumps(doctors)


@mcp.tool()
async def count_appointments() -> str:
    """Count appointment bookings without exposing patient details."""
    total = await get_appointment_count()
    return json.dumps({"total_appointments": total})


if __name__ == "__main__":
    mcp.run(transport="stdio")