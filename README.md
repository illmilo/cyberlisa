<img src="logo.png" width="35px" align="right">

# LISA

## Usage
To run database: 
```
docker-compose up -d
```
in terminal 

## Account Details
POSTGRES_USER: lisoon

POSTGRES_PASSWORD: 12345

POSTGRES_DB: fast_api

ports: "5433:5432"

## Demo

[cyberlisa.vercel.app](https://cyberlisa.vercel.app)

## Description

**Cyber Living Infrastructure Simulation Agent** (**CYBERLISA**) is a system that simulates realistic user behavior within an isolated training infrastructure of a cyber range.

## Local Run

### With Django

```bash
git clone https://github.com/illmilo/cyberlisa.git
cd cyberlisa
pip3 install -r requirements.txt
python3 manage.py runserver
```

### With Vercel
```bash
git clone https://github.com/illmilo/cyberlisa.git
cd cyberlisa
vercel dev
```

## License
This project is licensed under MIT License. View [LICENSE](LICENSE) to learn more.