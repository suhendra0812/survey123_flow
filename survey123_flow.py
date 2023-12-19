import json
import tempfile
from datetime import datetime
from pathlib import Path

import pywhatkit
import requests
from prefect import flow, task, variables


@task
def get_message(
    incident_date: datetime,
    kawasan: str,
    alamat: str,
    judul: str,
    uraian: str,
    pelapor: str,
):
    # Format datetime object to d MMMM yyyy HH:mm
    incident_date_formatted = f"{incident_date:%d %B %Y %H:%M}"

    # Create message body
    message = f"""*Sharing informasi lapangan*
Tanggal: {incident_date_formatted}
Kawasan: {kawasan}
Alamat: {alamat}
Judul: {judul}
Uraian: {uraian}
Pelapor: {pelapor}"""

    return message


@task
def send_message(message: str, image_path: str):
    group_id = variables.get("whatsapp_group_id")
    pywhatkit.sendwhats_image(
        receiver=group_id,
        img_path=image_path,
        caption=message,
        tab_close=True,
        close_time=5,
    )
    # pywhatkit.sendwhatmsg_instantly(phone_no=os.getenv("PHONE_NUMBER"), message=message)


@flow(log_prints=True)
def survey123_flow(
    incident_date: str,
    kawasan: str,
    jalan: str,
    detail_lokasi: str,
    judul: str,
    uraian: str,
    pelapor: str,
    pelapor_lain: str,
    attachment_url: str,
    attachment_name: str,
    token: str,
):
    # Save attachment to temporary directory
    with tempfile.TemporaryDirectory(prefix="survey123_flow_") as tmpdir:
        attachment_path = Path(tmpdir) / attachment_name
        response = requests.get(attachment_url, params={"token": token})
        with open(attachment_path, "wb") as f:
            f.write(response.content)

        # Convert incident date to datetime object
        incident_date = datetime.fromtimestamp(int(incident_date) / 1e3)

        # Construct pelapor
        pelapor = pelapor if pelapor != "Lainnya" else pelapor_lain

        # Construct alamat
        alamat = detail_lokasi if jalan == "Lainnya" else jalan

        # Get message text
        message = get_message(
            incident_date=incident_date,
            kawasan=kawasan,
            alamat=alamat,
            judul=judul,
            uraian=uraian,
            pelapor=pelapor,
        )

        # Send message
        send_message(message=message, image_path=str(attachment_path))


if __name__ == "__main__":
    survey123_flow()
