import urllib.request
from pathlib import Path

from django.conf import settings
from home.models import doctor

# Save images inside media/doctor/
BASE_DIR = Path(settings.BASE_DIR)
MEDIA_ROOT = Path(settings.MEDIA_ROOT) if settings.MEDIA_ROOT else BASE_DIR / "media"

image_folder = MEDIA_ROOT / "doctor"
image_folder.mkdir(parents=True, exist_ok=True)

doctor = doctor.objects.order_by("id")
updated = 0
failed = 0

for index, doctor in enumerate(doctor, start=1):

    # Preserve any picture already uploaded
    if doctor.doctor_image:
        print(f"Already has image: {doctor.doctor_name}")
        continue

    # Use different fictional profile portraits
    gender = "men" if index % 2 else "women"
    photo_id = ((index - 1) % 99) + 1

    image_name = f"doctor_{doctor.id}.jpg"
    image_path = image_folder / image_name

    url = f"https://randomuser.me/api/portraits/{gender}/{photo_id}.jpg"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ClinicDemo/1.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            image_data = response.read()

        # Check that the response resembles a JPEG file
        if not image_data.startswith(b"\xff\xd8\xff"):
            raise ValueError("Downloaded file is not a JPEG image")

        image_path.write_bytes(image_data)

        # Store a path relative to MEDIA_ROOT
        doctor.doctor_image = f"doctor/{image_name}"
        doctor.save(update_fields=["doctor_image"])

        updated += 1
        print(f"Added image: {doctor.doctor_name}")

    except Exception as error:
        failed += 1
        print(f"Failed: {doctor.doctor_name}: {error}")

print("\nImage assignment completed.")
print("New images:", updated)
print("Failed:", failed)
print("doctor with images:", doctor.objects.exclude(doctor_image="").count())
print("Image folder:", image_folder)