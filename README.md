# The backend of the Me0w00f Blogger

Me0w00f blogger is a project to create a blog site for the team.

To provide data management service, we create the repository of the backend.

# Technology Stack 

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Installation


## Directly running on Linux

Firstly, we have to install the python packages of the dependencies.
```commandline
pip install -r requirements.txt
```

Then create a file called `admin_list.json` to define the list of administrators to publish content of the organization.
```json
[
  {
    "user_name": "admin1",
    "password": "123456",
    "email": "admin1@gmail.com"
  },
  {
    "user_name": "admin2",
    "password": "123456",
    "email": "admin2@gmail.com"
  },
  {
    "user_name": "admin3",
    "password": "123456",
    "email": "admin3@gmail.com"
  }
]
```

It can be simply ran by uvicorn on Linux:
```commandline
./run.sh
```

Finally, configure proxy pass in nginx to set up the http server.

## Deploy by Docker Container.

