import email, csv, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from_address = ""
password = ""



# Create the plain-text and HTML version of your message
text = """\
Hello {name}  \n
"""

html = """\
<html>
  <body>
    <p>Hello {name}</p>
  </body>
</html>
"""

filename = "attachment_file.pdf"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        with open("contacts.csv") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for name, org, email in reader:
                if email != "":
                    print("Sending mail to {name} on {email}".format(name=name, email=email))

                    message = MIMEMultipart("alternative")
                    message["Subject"] = "Subject of mail"
                    message["From"] = from_address
                    
                    message.attach(part) # Add attachment to message and convert message to string


                    part1 = MIMEText(text.format(name=name), "plain")
                    part2 = MIMEText(html.format(name=name), "html")

                    message.attach(part1)
                    message.attach(part2)
                    
                    
                    message["To"] = email
                    server.sendmail(
                        from_address,
                        email,
                        message.as_string(),
                    )
except:
    print("An exception occurred")

