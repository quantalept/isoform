import asyncio
import getpass
import random
from email.message import EmailMessage
import aiosmtplib

async def send_email_async():
    otp = ''.join(str(random.randint(0, 9)) for _ in range(6))

    sender_email = input("SENDER EMAIL: ")
    receiver_email = input("RECEIVER EMAIL: ")
    subject = input("SUBJECT: ")
    message = input("MESSAGE: ")    
    password = getpass.getpass("ENTER YOUR GMAIL APP PASSWORD: ")

    full_message = f"{message}\n\nYour OTP is: {otp}"

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(full_message)

    try:
        await aiosmtplib.send(
            message=msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=sender_email,
            password=password
        )
        print("OTP sent successfully.")

        entered_otp = input("Enter the OTP you received: ")
        if entered_otp == otp:
            print("OTP verified successfully.")
        else:
            print("Invalid OTP. Verification failed.")

    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    asyncio.run(send_email_async())
