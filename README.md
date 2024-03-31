# The backend of the Me0w00f Blogger

Welcome to the Me0w00f Blogger project! This endeavor aims to create a blog site that is both feature-rich and visually appealing for our team.

## Technology Stack 

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Installation

### 1. Cloning the Repository
```bash
git clone https://github.com/me0w00f/me0w00f_organization_blogger_backend.git me0w00f_backend
```
```bash
cd me0w00f_backend
```

### 2. Installing Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```
### 3. Database Configuration

Ensure **MariaDB** is installed and configured on your system. Then, proceed to set up the `me0w00f` database and user:

```bash
mysql -u root -p
```
```sql
CREATE DATABASE me0w00f;
GRANT ALL PRIVILEGES ON me0w00f.* TO 'me0w00f'@'localhost' IDENTIFIED BY 'secure_password';
FLUSH PRIVILEGES;
```
**Replace `secure_password` with a strong, secure password of your choice.**

### 4. Application Configuration

Edit the `config.py` file to set your database connection details:
```python
......
# Database
DATABASE_URL = "mysql://me0w00f:secure_password@localhost/me0w00f"
......
```
### 5. Admin Setup

Create a `admin_list.json` file to define the administrators responsible for publishing content:

```json
[
  {
    "user_name": "admin1",
    "password": "secure_password_1",
    "email": "admin1@example.com"
  },
  {
    "user_name": "admin2",
    "password": "secure_password_2",
    "email": "admin2@example.com"
  },
  {
    "user_name": "admin3",
    "password": "secure_password_3",
    "email": "admin3@example.com"
  }
]
```
Make sure to replace the placeholder **passwords** and **email addresses** with ***actual secure credentials***.

### 6. Running the Application
To start the application using `uvicorn` on Linux, execute the provided shell script:

```bash
./run.sh
```

Alternatively, you can create and edit a systemd service to manage the `run.sh` script as a service.

1. Create a systemd service file:

Usually, systemd service files are stored in` /etc/systemd/system/`. You'll need to create a new service file here.
```
sudo vim /etc/systemd/system/me0w00f_backend.service
```
2. Edit the service file:

Add the following content to your service file, which defines the service and how it should be managed.

```service
[Unit]
Description=Me0w00f Blogger Backend Service
After=network.target
[Service]
User=<username>
Group=<group>
WorkingDirectory=/path/to/me0w00f_backend
ExecStart=/path/to/me0w00f_backend/run.sh
Restart=always
[Install]
WantedBy=multi-user.target
```

Replace `<username>` and `<group>` with the user and group that should run the service, and `/path/to/me0w00f_backend` with the actual path to your backend directory.

3. Enable and start the service:

After saving and closing the service file, you can enable the service to start on boot and then start the service immediately.

```bash
sudo systemctl enable me0w00f_backend.service
sudo systemctl start me0w00f_backend.service
```
4. Check the service status:

To ensure that the service is running properly, you can check its status with the following command:

```bash
sudo systemctl status me0w00f_backend.service
```
5. Managing the service:

You can use standard `systemctl` commands to start, stop, restart, and check the status of your service.

```bash
sudo systemctl start me0w00f_backend.service    # To start the service
sudo systemctl stop me0w00f_backend.service     # To stop the service
sudo systemctl restart me0w00f_backend.service  # To restart the service
sudo systemctl status me0w00f_backend.service   # To check the service
```
