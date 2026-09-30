import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.core.config import settings
from src.core.utils import utc_to_local
from src.order.entity import BookingEntity
from src.restaurant.entity import RestaurantEntity


class EmailService:
	def __init__(self):
		self.smtp_host = settings.SMTP_HOST
		self.smtp_port = settings.SMTP_PORT
		self.smtp_user = settings.SMTP_USER
		self.smtp_password = settings.SMTP_PASSWORD
		self.email_from = settings.EMAIL_FROM
		self.email_from_name = settings.EMAIL_FROM_NAME
		self.domain = "https://saigourmet-taste-the-soul-of-saigon.vercel.app"

	async def send_otp_email(self, email: str, otp: str) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Password Recovery - Your OTP Code"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body

			html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Password Reset OTP</title>
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
  >
    <table
      role="presentation"
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
    >
      <tr>
        <td style="padding: 20px 0 30px 0">
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              border-collapse: collapse;
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <!-- Header -->
            <tr>
              <td
                align="center"
                style="padding: 30px 0; background-color: #b2744c"
              >
                <h1
                  style="
                    color: #ffffff;
                    font-family: serif;
                    margin: 0;
                    font-size: 28px;
                  "
                >
                  SaiGourmet
                </h1>
              </td>
            </tr>
            <!-- Body -->
            <tr>
              <td bgcolor="#ffffff" style="padding: 40px 30px">
                <div style="text-align: center">
                  <h2 style="color: #333333; margin-top: 0">
                    Password Reset OTP
                  </h2>
                  <p
                    style="
                      color: #666666;
                      font-size: 16px;
                      line-height: 1.5;
                      margin-bottom: 30px;
                    "
                  >
                    Please use the One-Time Password (OTP) below to reset your password.
                  </p>

                  <!-- OTP Box -->
                  <div
                    style="
                      background-color: #f8f9fa;
                      border: 1px solid #eeeeee;
                      border-radius: 6px;
                      padding: 25px;
                      margin: 0 auto 30px auto;
                      display: block;
                      max-width: 300px;
                    "
                  >
                    <span
                      style="
                        font-family: monospace;
                        font-size: 32px;
                        font-weight: bold;
                        letter-spacing: 6px;
                        color: #333333;
                        display: block;
                      "
                      >{otp}</span
                    >
                  </div>

                  <p style="color: #999999; font-size: 13px; margin: 0">
                    Do not share this OTP with anyone. This code is valid for <strong style="color: #FF0000">10 minutes</strong>.<br />
                    If you did not request this, please ignore this email.
                  </p>
                </div>
              </td>
            </tr>
            <!-- Footer -->
            <tr>
              <td
                bgcolor="#333333"
                style="padding: 20px 30px; text-align: center"
              >
                <p style="color: #ffffff; font-size: 12px; margin: 0">
                  &copy; 2025 SaiGourmet. All rights reserved.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""
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

	def send_confirm_email(self, email: str, restaurant: RestaurantEntity, booking: BookingEntity) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Booking Confirmation"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body

			html_content = f"""<!DOCTYPE html>
			<html lang="en">
			<head>
			    <meta charset="UTF-8">
			    <meta http-equiv="X-UA-Compatible" content="IE=edge">
			    <meta name="viewport" content="width=device-width, initial-scale=1.0">
			    <title>Booking Confirmation</title>
			    <style>
			        body {{
			            font-family: Arial, sans-serif;
			            margin: 0;
			            padding: 0;
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
			        p {{
			            line-height: 1.6;
			        }}
			        .details {{
			            margin: 20px 0;
			            border-collapse: collapse;
			            width: 100%;
			        }}
			        .details th, .details td {{
			            border: 1px solid #dddddd;
			            padding: 8px;
			            text-align: left;
			        }}
			        .details th {{
			            background-color: #f2f2f2;
			        }}
			    </style>
			</head>
			<body>
			    <div class="container">
			        <div class="header">
			            <h1>Booking Confirmation</h1>
			        </div>
			        <div class="content">
			            <p>Dear <strong>{booking.customer_name}</strong>,</p>
			            <p>Thank you for your reservation! Your booking details are as follows:</p>
			            <table class="details">
			                <tr>
			                    <th>Booking ID</th>
			                    <td>{booking.booking_id}</td>
			                </tr>
			                <tr>
			                    <th>Restaurant Name</th>
			                    <td>{restaurant.name}</td>
			                </tr>
			                <tr>
			                    <th>Address</th>
			                    <td>{restaurant.address}</td>
			                </tr>
			                <tr>
			                    <th>Time</th>
			                    <td>{utc_to_local(str(booking.reservation_time))}</td>
			                </tr>
			                <tr>
			                    <th>Date</th>
			                    <td>{utc_to_local(str(booking.reservation_time))}</td>
			                </tr>
			                <tr>
			                    <th>Customer Name</th>
			                    <td>{booking.customer_name}</td>
			                </tr>
			                <tr>
			                    <th>Phone</th>
			                    <td>{booking.phone}</td>
			                </tr>
			                <tr>
			                    <th>Number of Guests</th>
			                    <td>{booking.num_of_guests}</td>
			                </tr>
			                <tr>
			                    <th>Note</th>
			                    <td>{booking.note}</td>
			                </tr>
			            </table>
			            <p>If you have need to modify your reservation, please update directly in the Booking Section.</p>
			            <p>We look forward to serving you!</p>
			            <p>Best regards,</p>
			            <p>The {restaurant.name} Team</p>
			        </div>
			        <div class="footer">
			            <p>&copy; 2024 {restaurant.name}. All rights reserved.</p>
			        </div>
			    </div>
			</body>
			</html>
			"""
			# Attach both plain text and HTML versions
			part1 = MIMEText(html_content, "html")
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

	async def send_welcome_email(self, email: str, name: str) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Welcome email"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body

			html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Welcome to SaiGourmet</title>
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
  >
    <table
      role="presentation"
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
    >
      <tr>
        <td style="padding: 20px 0 30px 0">
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <!-- Hero Image -->
            <tr>
              <td width="100%" style="background-color: #333">
                <!-- Placeholder image -->
                <img
                  src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80"
                  alt="Welcome"
                  style="
                    display: block;
                    width: 100%;
                    max-height: 200px;
                    object-fit: cover;
                  "
                />
              </td>
            </tr>
            <tr>
              <td style="padding: 40px 30px">
                <h1 style="color: #333; margin-top: 0">Welcome, {name}!</h1>
                <p style="color: #666; font-size: 16px; line-height: 1.6">
                  Thank you for joining <strong>SaiGourmet</strong>. You are now
                  part of Ho Chi Minh City's premier dining community.
                </p>
                <p style="color: #666; font-size: 16px; line-height: 1.6">
                  From street food gems to Michelin-star dining, finding your
                  next great meal has never been easier.
                </p>

                <div style="margin-top: 35px; text-align: center">
                  <a
                    href="https://yourwebsite.com/login"
                    style="
                      background-color: #b2744c;
                      color: white;
                      padding: 14px 30px;
                      text-decoration: none;
                      border-radius: 50px;
                      font-weight: bold;
                      font-size: 16px;
                    "
                    >Start Booking</a
                  >
                </div>
              </td>
            </tr>
            <tr>
              <td bgcolor="#b2744c" style="padding: 20px; text-align: center">
                <p style="color: #ffffff; margin: 0; font-size: 14px">
                  SaiGourmet - Taste the Soul of Saigon
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""  # Attach both plain text and HTML versions
			part1 = MIMEText(html_content, "html")
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

	async def send_pending_email(self, email, restaurant_name, booking: BookingEntity) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Booking Request Received "
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body

			html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Booking Request Received</title>
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
  >
    <table
      role="presentation"
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
    >
      <tr>
        <td style="padding: 20px 0 30px 0">
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              border-collapse: collapse;
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <!-- Header -->
            <tr>
              <td
                align="center"
                style="padding: 30px 0; background-color: #b2744c"
              >
                <h1
                  style="
                    color: #ffffff;
                    font-family: serif;
                    margin: 0;
                    font-size: 28px;
                  "
                >
                  SaiGourmet
                </h1>
              </td>
            </tr>
            <!-- Body -->
            <tr>
              <td bgcolor="#ffffff" style="padding: 40px 30px">
                <h2 style="color: #333333; margin-top: 0">Request Received</h2>
                <p style="color: #666666; font-size: 16px; line-height: 1.5">
                  Hi {booking.customer_name},<br /><br />
                  We have received your booking request for
                  <strong>{restaurant_name}</strong>. The restaurant manager
                  is currently reviewing your request. You will receive a
                  confirmation email shortly.
                </p>

                <table
                  width="100%"
                  cellpadding="10"
                  cellspacing="0"
                  style="
                    background-color: #f8f9fa;
                    border-radius: 6px;
                    margin: 20px 0;
                  "
                >
                  <tr>
                    <td width="30%" style="font-weight: bold; color: #555">
                      Restaurant:
                    </td>
                    <td style="color: #333">{restaurant_name}</td>
                  </tr>
                  <tr>
                    <td style="font-weight: bold; color: #555">Date & Time:</td>
                    <td style="color: #333">{utc_to_local(str(booking.reservation_time))}</td>
                  </tr>
                  <tr>
                    <td style="font-weight: bold; color: #555">Guests:</td>
                    <td style="color: #333">{booking.num_of_guests} People</td>
                  </tr>
                  <tr>
                    <td style="font-weight: bold; color: #555">Note:</td>
                    <td style="color: #333">{booking.note}</td>
                  </tr>
                </table>

                <p style="color: #999; font-size: 14px; margin-top: 30px">
                  *Please do not arrive until you receive the "Booking Accepted"
                  email.
                </p>
              </td>
            </tr>
            <!-- Footer -->
            <tr>
              <td
                bgcolor="#333333"
                style="padding: 20px 30px; text-align: center"
              >
                <p style="color: #ffffff; font-size: 12px; margin: 0">
                  &copy; 2025 SaiGourmet. All rights reserved.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""  # Attach both plain text and HTML versions
			part1 = MIMEText(html_content, "html")
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

	async def send_reject_email(self, email, restaurant_name, booking: BookingEntity) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Reject Email"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body

			html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Booking Update</title>   
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
  >
    <table
      role="presentation"
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
    >
      <tr>
        <td style="padding: 20px 0 30px 0">
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <tr>
              <td
                align="center"
                style="padding: 30px 0; background-color: #b2744c"
              >
                <h1
                  style="
                    color: #ffffff;
                    font-family: serif;
                    margin: 0;
                    font-size: 28px;
                  "
                >
                  SaiGourmet
                </h1>
              </td>
            </tr>
            <tr>
              <td style="padding: 40px 30px">
                <h2 style="color: #333333; margin-top: 0">
                  Reservation Status
                </h2>
                <p style="color: #666666; font-size: 16px; line-height: 1.5">
                  Dear {booking.customer_name},<br /><br />
                  We sincerely apologize, but
                  <strong>{restaurant_name}</strong> cannot accommodate your
                  reservation for {utc_to_local(str(booking.reservation_time))} due to full capacity or a
                  private event.<br /><br />
                  We know this is inconvenient. We invite you to explore other
                  top-rated restaurants on our platform.
                </p>

                <div style="margin-top: 30px; text-align: center">
                  <a
                    href="https://yourwebsite.com/restaurants/all"
                    style="
                      background-color: #333333;
                      color: white;
                      padding: 12px 25px;
                      text-decoration: none;
                      border-radius: 4px;
                    "
                    >Find Another Table</a
                  >
                </div>
              </td>
            </tr>
            <tr>
              <td
                bgcolor="#f8f9fa"
                style="
                  padding: 20px;
                  text-align: center;
                  font-size: 12px;
                  color: #999;
                "
              >
                If you have questions, please contact support@saigourmet.com
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
			part1 = MIMEText(html_content, "html")
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

	async def send_accept_email(self, email, restaurant: RestaurantEntity, booking: BookingEntity) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Accept Email"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = email

			# Email body

			html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Booking Confirmed</title>
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
  >
    <table
      role="presentation"
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
    >
      <tr>
        <td style="padding: 20px 0 30px 0">
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <tr>
              <td
                align="center"
                style="padding: 30px 0; background-color: #b2744c"
              >
                <h1
                  style="
                    color: #ffffff;
                    font-family: serif;
                    margin: 0;
                    font-size: 28px;
                  "
                >
                  SaiGourmet
                </h1>
              </td>
            </tr>
            <tr>
              <td style="padding: 40px 30px">
                <div style="text-align: center; margin-bottom: 20px">
                  <span
                    style="
                      display: inline-block;
                      width: 50px;
                      height: 50px;
                      background-color: #28a745;
                      color: white;
                      border-radius: 50%;
                      font-size: 30px;
                      line-height: 50px;
                    "
                    >&#10003;</span
                  >
                </div>
                <h2
                  style="color: #333333; margin: 0 0 20px 0; text-align: center"
                >
                  Booking Confirmed!
                </h2>
                <p
                  style="
                    color: #666666;
                    font-size: 16px;
                    line-height: 1.5;
                    text-align: center;
                  "
                >
                  Great news, {booking.customer_name}!
                  <strong>{restaurant.name}</strong> has accepted your
                  reservation.
                </p>

                <hr
                  style="
                    border: 0;
                    border-top: 1px solid #eeeeee;
                    margin: 30px 0;
                  "
                />

                <h3 style="color: #b2744c; margin-bottom: 15px">
                  Your Reservation Details
                </h3>
                <p style="margin: 5px 0; color: #555">
                  <strong>Date:</strong> {utc_to_local(str(booking.reservation_time))}
                </p>
                <p style="margin: 5px 0; color: #555">
                  <strong>Time:</strong> {utc_to_local(str(booking.reservation_time))}
                </p>
                <p style="margin: 5px 0; color: #555">
                  <strong>Address:</strong> {restaurant.address}
                </p>
                <p style="margin: 5px 0; color: #555">
                  <strong>Guests:</strong> {booking.num_of_guests}
                </p>

                <div style="margin-top: 40px; text-align: center">
                  <a
                    href="https://yourwebsite.com/profile"
                    style="
                      background-color: #b2744c;
                      color: white;
                      padding: 12px 25px;
                      text-decoration: none;
                      border-radius: 25px;
                      font-weight: bold;
                    "
                    >View Booking</a
                  >
                </div>
              </td>
            </tr>
            <tr>
              <td
                bgcolor="#333333"
                style="padding: 20px 30px; text-align: center"
              >
                <p style="color: #ffffff; font-size: 12px; margin: 0">
                  &copy; 2025 SaiGourmet. All rights reserved.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
			part1 = MIMEText(html_content, "html")
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

	async def send_announce_admin(self, admin_email, restaurant: RestaurantEntity, booking: BookingEntity) -> bool:
		"""Send OTP via email"""
		try:
			# Create message
			message = MIMEMultipart("alternative")
			message["Subject"] = "Accept Email"
			message["From"] = f"{self.email_from_name} <{self.email_from}>"
			message["To"] = admin_email

			# Email body

			html_content = f"""
			<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>New Booking Request</title>
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
  >
    <table
      role="presentation"
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
    >
      <tr>
        <td style="padding: 20px 0 30px 0">
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              border-collapse: collapse;
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <!-- Header -->
            <tr>
              <td
                align="center"
                style="padding: 30px 0; background-color: #b2744c"
              >
                <h1
                  style="
                    color: #ffffff;
                    font-family: serif;
                    margin: 0;
                    font-size: 28px;
                  "
                >
                  SaiGourmet
                </h1>
              </td>
            </tr>
            <!-- Body -->
            <tr>
              <td bgcolor="#ffffff" style="padding: 40px 30px">
                <div style="text-align: center; margin-bottom: 20px">
                  <span
                    style="
                      background-color: #ffc107;
                      color: #333;
                      padding: 6px 16px;
                      border-radius: 50px;
                      font-size: 12px;
                      font-weight: bold;
                      text-transform: uppercase;
                      letter-spacing: 1px;
                    "
                  >
                    Pending Approval
                  </span>
                </div>

                <h2
                  style="
                    color: #333333;
                    margin-top: 0;
                    text-align: center;
                    margin-bottom: 10px;
                  "
                >
                  New Booking Request
                </h2>
                <p
                  style="
                    color: #666666;
                    font-size: 16px;
                    line-height: 1.5;
                    text-align: center;
                    margin-bottom: 30px;
                  "
                >
                  Hello admin, <strong>{booking.customer_name}</strong> has submitted
                  a new reservation request. Please review the details below.
                </p>

                <table
                  width="100%"
                  cellpadding="12"
                  cellspacing="0"
                  style="
                    background-color: #f8f9fa;
                    border: 1px solid #eeeeee;
                    border-radius: 6px;
                    margin-bottom: 35px;
                  "
                >
                  <tr>
                    <td
                      width="35%"
                      style="
                        font-weight: bold;
                        color: #555;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      Booking ID:
                    </td>
                    <td
                      style="
                        color: #333;
                        font-family: monospace;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      {booking.booking_id}
                    </td>
                  </tr>
                  <tr>
                    <td
                      style="
                        font-weight: bold;
                        color: #555;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      Restaurant:
                    </td>
                    <td
                      style="
                        color: #333;
                        font-weight: bold;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      {restaurant.name}
                    </td>
                  </tr>
                  <tr>
                    <td
                      style="
                        font-weight: bold;
                        color: #555;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      Date & Time:
                    </td>
                    <td style="color: #333; border-bottom: 1px solid #eee">
                      {utc_to_local(str(booking.reservation_time))}
                    </td>
                  </tr>
                  <tr>
                    <td
                      style="
                        font-weight: bold;
                        color: #555;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      Guest Info:
                    </td>
                    <td style="color: #333; border-bottom: 1px solid #eee">
                      {booking.customer_name}<br />
                      <span style="font-size: 13px; color: #777"
                        >{booking.phone}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      style="
                        font-weight: bold;
                        color: #555;
                        border-bottom: 1px solid #eee;
                      "
                    >
                      Party Size:
                    </td>
                    <td style="color: #333; border-bottom: 1px solid #eee">
                      {booking.num_of_guests} People
                    </td>
                  </tr>
                  <tr>
                    <td style="font-weight: bold; color: #555">Note:</td>
                    <td style="color: #333; font-style: italic">{booking.note}</td>
                  </tr>
                </table>

                <div style="text-align: center">
                  <a
                    target="_blank"
                    href="{self.domain}/admin/restaurant/{booking.restaurant_id}/booking/{booking.booking_id}"
                    style="
                      background-color: #b2744c;
                      color: white;
                      padding: 14px 35px;
                      text-decoration: none;
                      border-radius: 50px;
                      font-weight: bold;
                      font-size: 16px;
                      display: inline-block;
                      box-shadow: 0 4px 6px rgba(178, 116, 76, 0.3);
                    "
                    >Manage Booking</a
                  >
                </div>
              </td>
            </tr>
            <tr>
              <td
                bgcolor="#333333"
                style="padding: 20px 30px; text-align: center"
              >
                <p style="color: #ffffff; font-size: 12px; margin: 0">
                  &copy; 2025 SaiGourmet Admin System
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>

			"""
			part1 = MIMEText(html_content, "html")
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
