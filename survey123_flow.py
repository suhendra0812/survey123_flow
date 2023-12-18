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
        phone_no="+6281322549085", message=message_body, wait_time=5
    )


if __name__ == "__main__":
    send_message.serve(name="survey123-deployment")
