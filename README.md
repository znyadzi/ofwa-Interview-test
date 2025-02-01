# Galamsey Data Analysis Tool

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
- **Tools**: Python, Git, Postman (for API testing)

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

