import os
from datetime import datetime

import pywhatkit
from prefect import flow


@flow(log_prints=True)
def send_message(
    incident_date: str,
    kawasan: str,
    jalan: str,
    judul: str,
    pelapor: str,
    pelapor_lain: str,
):
    # Convert incident date to datetime object and format it to d MMMM yyyy HH:mm
    incident_date = datetime.fromtimestamp(int(incident_date) / 1e3)
    incident_date_formatted = incident_date.strftime("%d %B %Y %H:%M")

    # Create message body
    message_body = f"""
    Incident Date: {incident_date_formatted}
    Kawasan: {kawasan}
    Jalan: {jalan}
    Judul: {judul}
    Pelapor: {pelapor}
    Pelapor Lain: {pelapor_lain}
    """

    pywhatkit.sendwhatmsg_instantly(
        phone_no=os.getenv("PHONE_NUMBER"), message=message_body, wait_time=5
    )


if __name__ == "__main__":
    send_message.from_source(
        source="https://github.com/suhendra0812/survey123_flow.git",
        entrypoint="survey123_flow.py:send_message",
    ).deploy(name="survey123-response-deploy", work_pool_name="local-subprocess")
