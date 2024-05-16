import csv
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Setting Up Database
DATABASE_URL = 'postgresql://shan:password123@localhost:5432/miracleclinicaltrails'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Class creation to properly organize webscraping from EU Clinical Trials Website.
class ClinicalTrial(Base):
    __tablename__ = 'eu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    eudract_number = Column(String)
    sponsor_name = Column(String)
    full_title = Column(String)
    medical_condition = Column(String)

# Class to combine EU and US Clinical Trials together in one table called "combined."
class CombinedTrial(Base):
    __tablename__ = 'combined'
    id = Column(Integer, primary_key=True, autoincrement=True)
    study_identifier = Column(String)
    sponsor_name = Column(String)
    study_title = Column(String)
    medical_condition = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_clinical_trials_data(driver):
    """
    Function to scrape clinical trial data from the EU website.
    """
    trials = []
    driver.get("https://www.clinicaltrialsregister.eu/ctr-search/search?query=")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.results.grid_8plus")))
    trial_tables = driver.find_elements(By.CSS_SELECTOR, "table.result")

    for table in trial_tables:
        trial = {}
        eudract_number_element = table.find_element(By.XPATH, ".//span[contains(text(), 'EudraCT Number:')]/..")
        trial["Eudract Number"] = eudract_number_element.text.split(":", 1)[1].strip() if eudract_number_element else "N/A"

        sponsor_name_element = table.find_element(By.XPATH, ".//span[contains(text(), 'Sponsor Name:')]/..")
        trial["Sponsor Name"] = sponsor_name_element.text.split(":", 1)[1].strip() if sponsor_name_element else "N/A"
        
        full_title_element = table.find_element(By.XPATH, ".//span[contains(text(), 'Full Title:')]/..")
        trial["Full Title"] = full_title_element.text.split(":", 1)[1].strip() if full_title_element else "N/A"

        medical_condition_element = table.find_element(By.XPATH, ".//span[contains(text(), 'Medical condition:')]/..")
        trial["Medical Condition"] = medical_condition_element.text.split(":", 1)[1].strip() if medical_condition_element else "N/A"

        trials.append(trial)
    return trials

def save_trials_to_db(session, trials):
    """
    Function to save clinical trials data to the database.
    """
    for trial in trials:
        new_trial = ClinicalTrial(
            eudract_number=trial["Eudract Number"],
            sponsor_name=trial["Sponsor Name"],
            full_title=trial["Full Title"],
            medical_condition=trial["Medical Condition"]
        )
        session.add(new_trial)
    session.commit()

def download_clinical_trials_csv(driver, download_dir):
    """
    Function to download clinical trials data from the US website as a CSV file.
    """
    filename = "ctg-studies.csv.crdownload"
    filepath = os.path.join(download_dir, filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    driver.get("https://clinicaltrials.gov/search")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.action-bar-button")))
    download_button = driver.find_element(By.CSS_SELECTOR, "button.action-bar-button")
    download_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ng-star-inserted")))
    deselect_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-ga-label='De-select all']"))
    )
    deselect_all_button.click()

    columns = [
        "download-field-NCT Number",
        "download-field-Study Title",
        "download-field-Conditions",
        "download-field-Sponsor"
    ]

    for column_id in columns:
        checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, column_id)))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", checkbox)

    final_download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.primary-button"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", final_download_button)
    time.sleep(1)
    driver.execute_script("arguments[0].style.backgroundColor = 'yellow'; arguments[0].style.border = '3px solid red';", final_download_button)
    time.sleep(1)
    final_download_button.click()
    time.sleep(60)

    if not os.path.exists(filepath):
        raise Exception(f"File {filename} not found in {download_dir}")
    
    return filepath

def save_csv_to_db(filepath, engine):
    """
    Function to save clinical trials data from CSV file to the database.
    """
    df = pd.read_csv(filepath)
    df.to_sql('us', engine, if_exists='replace', index=False)

def combine_and_transform_data(session):
    """
    Function to combine and transform clinical trials data from the EU and US sources.
    """
    us_trials = session.execute(text("SELECT * FROM us")).fetchall()
    eu_trials = session.execute(text("SELECT * FROM eu")).fetchall()
    
    combined_trials = []
    
    for trial in us_trials:
        combined_trial = {
            'study_identifier': f"US_{trial[0]}",
            'sponsor_name': trial[3],
            'study_title': trial[1].lower(),
            'medical_condition': trial[2]
        }
        combined_trials.append(combined_trial)
    
    for trial in eu_trials:
        combined_trial = {
            'study_identifier': f"EU_{trial.eudract_number}",
            'sponsor_name': trial.sponsor_name,
            'study_title': trial.full_title.lower(),
            'medical_condition': trial.medical_condition
        }
        combined_trials.append(combined_trial)
    
    return combined_trials

def save_combined_trials_to_db(session, combined_trials):
    """
    Function to save combined clinical trials data to the database.
    """
    for trial in combined_trials:
        new_combined_trial = CombinedTrial(
            study_identifier=trial['study_identifier'],
            sponsor_name=trial['sponsor_name'],
            study_title=trial['study_title'],
            medical_condition=trial['medical_condition']
        )
        session.add(new_combined_trial)
    session.commit()

def scrape_eu_clinical_trials(session):
    """
    Function to scrape clinical trials data from the EU website.
    """
    driver = webdriver.Chrome()
    try:
        trials = get_clinical_trials_data(driver)
        save_trials_to_db(session, trials)
    finally:
        driver.quit()

def scrape_us_clinical_trials(engine):
    """
    Function to scrape clinical trials data from the US website.
    """
    download_dir = os.path.expanduser("~/Desktop/downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    try:
        filepath = download_clinical_trials_csv(driver, download_dir)
        save_csv_to_db(filepath, engine)
    finally:
        driver.quit()

def main():
    """
    Main function to run the entire process.
    """
    session = Session()
    try:
        scrape_eu_clinical_trials(session)
    finally:
        session.close()
    
    scrape_us_clinical_trials(engine)

    # Combine data and save to the combined table
    session = Session()
    try:
        combined_trials = combine_and_transform_data(session)
        save_combined_trials_to_db(session, combined_trials)
    finally:
        session.close()

if __name__ == "__main__":
    main()
