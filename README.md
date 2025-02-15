# Galamsey Data Analysis API

This project is a Django REST API designed to manage and analyze data related to illegal mining (Galamsey) sites in various towns and regions. It provides functionalities to:
- Upload and manage Galamsey site data via CSV files.
- Perform CRUD operations on the data.
- Analyze the data to calculate:
  - The total number of Galamsey sites across all regions.
  - The average number of Galamsey sites per region.
  - The region with the highest number of Galamsey sites.

---

## Why This Project Was Created

Illegal mining (Galamsey) is a significant environmental and social issue in many regions. This project was created to:
1. Provide a centralized platform for storing and managing Galamsey site data.
2. Enable easy analysis of the data to identify trends and hotspots.
3. Support decision-making for environmental and regulatory bodies.

---

## Features

- **CRUD Operations**: Create, Read, Update, and Delete Galamsey site data.
- **CSV Upload**: Upload Galamsey site data via CSV files.
- **Data Analysis**:
  - Total number of Galamsey sites across all regions.
  - Average number of Galamsey sites per region.
  - Region with the highest number of Galamsey sites.

---

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: SQLite
- **Frontend**: Django REST Framework's Browsable API
- **Tools**: Python, Git, django administration (for API testing)

---

## Setup Instructions

### 1. Prerequisites

- Python 3.x
- pip (Python package manager)
- Git (optional, for cloning the repository)

---

### 2. Clone the Repository

If you have Git installed, clone the repository:
```bash
git clone https://github.com/znyadzi/galamsey-data-analysis-tool.git
cd galamsey-data-analysis-tool

# Project Setup Guide

## 3. Set Up a Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

### On Windows:

```bash
venv\Scripts\activate
```

### On macOS/Linux:

```bash
source venv/bin/activate
```
## 4. Install Django and Django Rest Framework
```bash
python install Django
```
```bash
python install djangorestframework
```
## 5. Set Up the Database

Apply migrations to set up the database:

```bash
python3 manage.py migrate
```

Create a superuser (admin) account:

```bash
python3 manage.py createsuperuser
```

## 6. Run the Development Server

Start the Django development server:

```bash
python3 manage.py runserver
```

The API will be available at:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## API Endpoints

### 1. Required Operations
- **API HOMEPAGE**
    ![Root API](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/rootapipage.png)
- **List all uploaded file details:** `GET /api/uploadedfiles/`
    ![Uploaded Files](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/uploadedfiles.png)
- **Retrieve all site records for a specific file:** `GET /api/getsitedata/<id>`
    ![All CSV file Records](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/allsitedatauploaded.png)
- **Retrieve average number of sites for a specific entry:** `GET /api/averagesitesperregion/<id>/`
    ![Average Sites Per Region](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/averagesitesperregion.png)
- **Region with Highest Galamsey Sites:** `GET /api/sitesabovethreshold/1/5/<id>/`
    ![Region With Highest Number of Galamsay Sites](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/regionwithhighestsites.png)
- **Regions with sites Higher than a given Threshold:** `GET /api/sitesabovethreshold/<int:fileID>/<int:Threshold>/`
    ![Regions With Sites Above A Threshold](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/regionsitesabovethreshold.png)
- **Upload csv file via API:** `POST /api/upload/`
    ![CSV file Upload](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/fileupload.png)
### 2. Testing Custom Functions

- **Total Galamsey Sites:** `curl -X GET http://127.0.0.1:8000/api/getsitedata/<int:fileID>/`
- **Average Galamsey Sites per Region:** ` curl -X GET http://127.0.0.1:8000/api/averagesitesperregion/<int:fileID>/`
- **Region with Highest Galamsey Sites:** `curl -X GET /api/region-with-highest-galamsey-sites/`
- **Regions with sites Higher than a given Threshold:** ` curl -X GET http://127.0.0.1:8000/api/sitesabovethreshold/<int:fileID>/<int:Threshold>/`
- **All Uploaded Files:** `curl -X GET http://127.0.0.1:8000/api/uploadedfiles/ `
    ![Tested APIs](https://raw.githubusercontent.com/znyadzi/ofwa-Interview-test/refs/heads/main/galamsey_DStore/TestingImages/testscenarios.png)

### 3. CSV Upload

- **Upload csv file via API:** `GET /api/upload/`

- **Upload CSV Manualy:** 
  - Copy your CSV file into the galamsey\_dataset folder and run:\
    &#x20;python3 manage.py import\_csv galamsey\_dataset/your\_dataset.csv

#### CSV File Requirements

The CSV file must have the following headers:

- `Town`
- `Region`
- `Number_of_Galamsay_Sites`

---

## Contributing

This project is not open for contributions but, if for any reason you want to contribute to this project, see the contact details below.
This project if open-source for whoever wants to copy and use it for learning purposes and for a special funtionality of a broader project.
---

## License

The project requirements was designed for OFWA( The Open Foundations West Africa ) team as an interview test for a Technical coordinator role.
All rights reserved.
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- **Open Foundations West Africa** for structuring an engaging onboarding project for their Technical coordinator
- **Django** and **Django REST Framework** for providing the tools to build this API.
- **The Python community** for their extensive documentation and support.

---

## Contact

For questions or feedback, please contact:

- **Your Name:** [znyadzi1@gmail.com](mailto\:znyadzi1@gmail.com)
- **GitHub:** [znyadzi](https://github.com/znyadzi)
