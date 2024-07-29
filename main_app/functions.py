from twilio.rest import Client
from email.mime.text import MIMEText
import smtplib
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
import os
load_dotenv()



# print(os.getenv('EMAIL_HOST_USER'))
# print(type(os.getenv('EMAIL_HOST_USER')))
# def send_mail(email, subject, body):
#     sender_email = os.getenv('EMAIL_HOST_USER')
#     receiver_email = email
#     password = os.getenv('EMAIL_HOST_PASSWORD')  # Use an App Password or enable Less Secure Apps

#     # Create the email message
#     message = MIMEText(body)
#     message['From'] = sender_email
#     message['To'] = receiver_email
#     message['Subject'] = subject
    
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.ehlo()
#         server.starttls()
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())
#         print('Email sent successfully!')
#         server.quit()
#     except Exception as e:
#         print(f'An error occurred: {str(e)}')

# send_mail('a.mahaveer5@gmail.com', 'test', 'test')

def send_sms(numbers_to_message, message_body):
    account_sid = os.getenv('SMS_SID')
    auth_token = os.getenv('SMS_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    from_phone_number = os.getenv('SMS_FROM_PH')

    # Ensure numbers_to_message is iterable
    if not isinstance(numbers_to_message, (list, tuple)):
        numbers_to_message = [numbers_to_message]

    for number in numbers_to_message:
        try:
            # Validate and format the phone number
            formatted_number = validate_and_format_phone_number(number)

            # Send the SMS using the formatted number
            message = client.messages.create(
                from_=from_phone_number,
                body=message_body,
                to=formatted_number
            )

            print(f"Message SID for {formatted_number}: {message.sid}")

        except TwilioRestException as e:
            print(f"Twilio error: {e}")

def validate_and_format_phone_number(phone_number):
    
    phone_number=str(phone_number)
    if not phone_number.startswith('+'):
        phone_number = '+91' + phone_number
        print("phone_number:",phone_number)

    return phone_number


# send_sms(9962526764,'hi bro')