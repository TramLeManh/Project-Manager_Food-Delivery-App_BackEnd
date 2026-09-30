<div align="center">
  <h1>SAIGOURMET: TASTE THE SOUL OF SAIGON</h1>
</div>
<strong>SaiGourmet</strong> is a restaurant discovery and reservation platform designed to connect diners with culinary experiences across Ho Chi Minh City.

This repository contains the <strong>Backend Service</strong> of SaiGourmet (<a href="https://github.com/yeenci/saigourmet-taste-the-soul-of-saigon">Link</a>), providing the RESTful APIs and server-side functionality consumed by the project's separate frontend UI. Built with <strong>FastAPI</strong>, it handles authentication, restaurant discovery, and booking services.

## 📋 Table of Content

1. [Introduction](#introduction)
2. [Getting started](#getting-started)
3. [Technologies Used](#technologies-used)
4. [UI Interface](#ui-interface)
5. [Key Features](#key-features)
6. [Our Team](#our-team)
7. [References](#references)
8. [License](#license)

<!-- Introduction -->
## 🪧 Introduction <a name="introduction"></a>

**SaiGourmet** streamlines the dining experience by allowing users to explore top-tier restaurants and secure tables instantly. The application ensures a seamless user journey—from browsing restaurant details to managing booking history—while providing administrators with robust tools to oversee reservations.

## 🚀 Getting started <a name="getting-started"></a>

## 🎯 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TramLeManh/Project-Manager_Food-Delivery-App_BackEnd.git
cd Project-Manager_Food-Delivery-App_BackEnd
```

### 2. Build the Docker Image

```bash
docker compose build
```

## 💨 Running the Application

### 1. Start the Application

Run the application in detached mode:

```bash
docker compose up -d
```

### 2. Access the API Documentation

Once the application is running, open the FastAPI Swagger UI:

**API Documentation:** http://localhost:1412/docs

If your Docker configuration maps the application to another port (e.g. `1412 `), access it through the corresponding port.

## ⚙️ Technologies Used

| Technology      | Usage                                           |
| --------------- | ----------------------------------------------- |
| **FastAPI**     | Backend web framework for building RESTful APIs |
| **MongoDB**     | NoSQL database for storing application data     |
| **Google SMTP** | Email delivery and notification service         |
| **Docker**      | Containerization and application deployment     |


## 💎 Key Features

* **🔐 Role-Based Access Control:** Provides separate workflows and permissions for **Customers** and **Administrators**, supporting customer bookings and administrative management.

* **📧 Email Notification System:** Sends automated emails for **booking requests, booking confirmations, and OTP verification**.

## 👥 Our Team <a name="our-team"></a>

This project was built with ❤️ by a team of 6 dedicated developers.

| No. | Member Name | Role |
|:---:|:-----------|:-----|
| 1 | **Nguyen Thi Yen Chi** | Frontend Developer |
| 2 | **Tram Le Manh** | Backend Developer |
| 3 | **Chau Thanh Phat** | UI/UX Designer |
| 4 | **Vo Nguyen Thanh Liem** | Backend Developer |
| 5 | **Gonzalez Marcos Delgado** | Backend Developer |
| 6 | **Nguyen Quang Minh Tri** | Backend Developer |

## 📚 References <a name="references"></a>

- [Fast Documentation](https://fastapi.tiangolo.com/)
- [Google SMTP](https://developers.google.com/workspace/gmail/imap/imap-smtp?hl=vi)

## 📜 License <a name="license"></a>

This project is licensed under the [MIT License](LICENSE).