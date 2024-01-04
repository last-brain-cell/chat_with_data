import os
import time
from io import BytesIO

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from reportlab.pdfgen import canvas
from email import policy
from email.parser import BytesParser


class EMLHandler(FileSystemEventHandler):
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.eml'):
            print(f"File {event.src_path} created. Converting to PDF...")
            eml_file_path = event.src_path
            output_file_path = os.path.join(self.output_dir, os.path.basename(eml_file_path) + '.pdf')
            convert_eml_to_pdf(eml_file_path, output_file_path)
            os.remove(eml_file_path)
            print("Conversion complete. Original file deleted.")


def extract_text_from_message(message):
    if message.is_multipart():
        text_content = ""
        for part in message.walk():
            if part.get_content_type() in ('text/plain', 'text/html'):
                text_content += part.get_payload()
        return text_content
    else:
        return message.get_payload()


def convert_eml_to_pdf(eml_file_path, output_pdf_path):
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

    subject = msg.get('subject', 'No Subject')
    sender = msg.get('from', 'Unknown Sender')
    date = msg.get('date', 'Unknown Date')

    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(72, 800, f'Subject: {subject}')
    pdf.drawString(72, 780, f'Sender: {sender}')
    pdf.drawString(72, 760, f'Date: {date}')

    text_content = extract_text_from_message(msg)
    if text_content:
        pdf.drawString(72, 740, 'Content:')
        pdf.drawString(72, 720, text_content)

    pdf.save()

    with open(output_pdf_path, 'wb') as pdf_file:
        pdf_file.write(pdf_buffer.getvalue())


def main():
    input_directory = 'data/inbox'
    output_directory = 'data/outbox'

    os.makedirs(input_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)

    eml_handler = EMLHandler(input_directory, output_directory)
    observer = Observer()
    observer.schedule(eml_handler, path=input_directory, recursive=False)

    try:
        print(f"Watching directory: {input_directory}")
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
