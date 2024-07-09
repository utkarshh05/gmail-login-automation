from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import logging

# Constants
DB_URL = 'postgresql+psycopg2://postgres:utkarsh0508@localhost/credentials_db'
DRIVER_PATH = '/usr/local/bin/chromedriver'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """
    Set up database connection and retrieve session.
    """
    try:
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        return engine, session
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise

def retrieve_single_credentials(engine, session):
    """
    Retrieve a single set of credentials from the database.
    """
    try:
        metadata = MetaData(bind=engine)
        credentials_table = Table('gmail_credentials', metadata, autoload=True)
        query = session.query(credentials_table).first()
        return query.email, query.password
    except Exception as e:
        logger.error(f"Failed to retrieve credentials: {e}")
        raise

def login_to_gmail(email, password):
    """
    Perform Gmail login automation.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    try:
        service = Service(DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get('https://mail.google.com')
        logger.info("Navigated to Gmail login page")

        # Wait for the email input field to be visible and enter the email
        email_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
        logger.info("Entered email and submitted")

        # Wait for the password input field to be visible and enter the password
        password_field = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]'))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        logger.info("Entered password and submitted")

        # Wait for the Gmail inbox page title to confirm successful login
        WebDriverWait(driver, 30).until(EC.title_contains("Inbox"))
        logger.info("Logged in successfully")

    except (NoSuchElementException, TimeoutException) as e:
        logger.error(f"An error occurred with a web element: {e}")
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            logger.info("Browser closed")

def main():
    """
    Main function to execute the script.
    """
    try:
        engine, session = setup_database()
        email, password = retrieve_single_credentials(engine, session)
        login_to_gmail(email, password)
        logger.info("Script execution completed")
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
