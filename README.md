# Clinical Trials Data Scraper and Visualization

## Overview

This project scrapes clinical trial data from EU and US websites, stores it in a PostgreSQL database, and visualizes the data using a Next.js frontend application.

## Architecture

1. **Backend**:
    - **Python Script**: Scrapes data from clinical trial websites and stores it in a PostgreSQL database.
    - **Crontab**: Schedules the Python script to run every 12 hours.

2. **Frontend**:
    - **Next.js Application**: Visualizes the data using charts.

## Setup Instructions

### Prerequisites

- PostgreSQL
- Python3
- Node.js

### Backend Setup

1. **Navigate to the Backend Directory**:
    ```
    cd backend
    ```

2. **Install Python Dependencies**:
    ```
    pip install -r requirements.txt
    ```

3. **Set Up PostgreSQL Database**:
    Create a PostgreSQL database and update the `DATABASE_URL` in `webscraper.py` with your database credentials.

    **Commands To Setup PostgreSQL Daabase from terminal**:
    brew update
    brew install postgresql

    brew services start postgresql
    sudo -i -u postgres
    psql
    CREATE DATABASE databaseNameOfYourChoice;
    CREATE USER myuser WITH ENCRYPTED PASSWORD 'passwordOfYourChoice';
    GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

    **Connect to Database by running the following commands**;
    psql -U myuser -d mydatabase


4. **Run the Python Script**:
    ```
    python3 webscraper.py
    ```

5. **Set Up Crontab to Run the Script Every 12 Hours**:
    ```
    crontab -e
    ```
    Add the following line to the crontab:
    ```
    0 */12 * * * /usr/bin/python3 /path/to/webscraper.py
    ```

### Frontend Setup

1. **Navigate to the Next.js App Directory**:
    ```
    cd client/miracle-interview
    ```

2. **Install Node.js Dependencies**:
    ```
    npm install
    npm install dotenv
    npm install axios
    npm install recharts pg
    npm install chart.js react-chartjs-2
    npm install -D tailwindcss postcss autoprefixer
    npx tailwindcss init -p
    ```

3. **Create a `.env.local` File**:
    Create a `.env.local` file and add your environment variables, e.g., database connection string.

4. **Run the Application Locally**:
    ```
    npm run dev
    ```

## Code Structure

### Server

- `webscraper.py`: Contains the Python script for scraping data from EU and US clinical trials websites and storing it in the PostgreSQL database.
- `requirements.txt`: Lists the Python dependencies required for the project.

### Client

- `nextjs-app/`: Contains the Next.js application for visualizing the data.
  - `pages/`: Contains the pages of the application.
  - `components/`: Contains the reusable components used in the application.
  - `styles/`: Contains the CSS files for styling the application.
  - `.env.local`: Example environment variables file.

## Running the Application

1. **Start the PostgreSQL Database**.
2. **Run the Backend Script**:
    ```
    python3 server/webscraper.py
    ```
3. **Start the Frontend Application**:
    ```
    cd client/miracle-interview
    npm run dev
    ```

### Notes

- Ensure that all environment variables are correctly set in the `.env` files.
- The backend script is scheduled to run every 12 hours using `crontab`.