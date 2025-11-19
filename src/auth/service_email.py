import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.core.config import settings


class EmailService:
	def __init__(self):
		self.smtp_host = settings.SMTP_HOST
		self.smtp_port = settings.SMTP_PORT
		self.smtp_user = settings.SMTP_USER
		self.smtp_password = settings.SMTP_PASSWORD
		self.email_from = settings.EMAIL_FROM
		self.email_from_name = settings.EMAIL_FROM_NAME

	def send_otp_email(self, email: str, otp: str) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Password Recovery - Your OTP Code"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body


			# html = "<!DOCTYPE html>" + "<html lan" +"g=\"en\">" + "<head>" + "<meta charset=\"UTF-8\">" + "<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">" + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">" + "<title>OTP Email</title>" + "<style>" + "body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f6f6f6; }" + ".container { max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 20px; border: 1px solid #dddddd; }" + ".header { background-color: #b2744c; color: white; text-align: center; padding: 10px 0; }" + ".content { padding: 20px; }"+ ".footer { text-align: center; color: #888888; font-size: 12px; padding: 20px; margin-top: 20px; border-top: 1px solid #dddddd; }"+ "p { line-height: 1.6; }" + "</style>" + "</head>" + "<body>" + "<div class=\"container\">"+ "  <div class=\"header\">" + "    <h1>Dev</h1>" + "  </div>" + "  <div class=\"content\">"+ "    <h2>Password Reset OTP</h2>" + "    <p>Dear <strong>" + email + "</strong></p>"+ "    <p>Your OTP is: <strong style=\"color: red;\">" + otp + "</strong></p>" + "    <p>Do not share this OTP with anyone. This OTP is <strong style=\"color: red;\">valid for 10 minutes</strong> .</p>"+ "    <p>If you did not request this OTP, please contact our support team.</p>" + "    <p>Best regards,</p>"+ "    <p>The Dev Team</p>" + "  </div>" + "  <div class=\"footer\">" + "    <p>Dev Inc. &copy; 2024</p>"+ "    <p>This email was sent to " + email + ". If you have any issues, please contact <a href=\"mailto:lemanh1412@gmail.com\">support@Dev.com</a>.</p>"+ "  </div>" + "</div>" + "</body>" + "</html>";
			html = f"""
			<!DOCTYPE html>
			<html lang="en">
			<head>
			    <meta charset="UTF-8">
			    <meta http-equiv="X-UA-Compatible" content="IE=edge">
			    <meta name="viewport" content="width=device-width, initial-scale=1.0">
			    <title>OTP Email</title>
			    <style>
			        body {{
			            font-family: Arial, sans-serif;
			            margin: 0; padding: 0;
			            background-color: #f6f6f6;
			        }}
			        .container {{
			            max-width: 600px;
			            margin: 20px auto;
			            background-color: #ffffff;
			            padding: 20px;
			            border: 1px solid #dddddd;
			        }}
			        .header {{
			            background-color: #b2744c;
			            color: white;
			            text-align: center;
			            padding: 10px 0;
			        }}
			        .content {{
			            padding: 20px;
			        }}
			        .footer {{
			            text-align: center;
			            color: #888888;
			            font-size: 12px;
			            padding: 20px;
			            margin-top: 20px;
			            border-top: 1px solid #dddddd;
			        }}
			        p {{ line-height: 1.6; }}
			    </style>
			</head>

			<body>
			    <div class="container">
			        <div class="header">
			            <h1>Dev</h1>
			        </div>

			        <div class="content">
			            <h2>Password Reset OTP</h2>
			            <p>Dear <strong>{email},</strong></p>
			            <p>Your OTP is:
			                <strong style="color: red;">{otp}</strong>
			            </p>
			            <p>
			                Do not share this OTP with anyone.
			                This OTP is <strong style="color: red;">valid for {settings.OTP_EXPIRY_MINUTES}minutes</strong>.
			            </p>
			            <p>If you did not request this OTP, please contact our support team.</p>
			            <p>Best regards,</p>
			            <p>The Dev Team</p>
			        </div>

			        <div class="footer">
			            <p>Dev Inc. © 2025</p>
			            <p>
			                This email was sent to {email}.
			                If you have any issues, please contact
			                <a href="mailto:lemanh1412@gmail.com">support@Dev.com</a>.
			            </p>
			        </div>
			    </div>
			</body>
			</html>
			"""

			# Attach both plain text and HTML versions
			part1 = MIMEText(html, "html")
			message.attach(part1)

			# Send email
			with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
				server.starttls()
				server.login(self.smtp_user, self.smtp_password)
				server.send_message(message)

			return True

		except Exception as e:
			print(e)
			return False
