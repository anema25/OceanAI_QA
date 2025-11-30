# examples/sample_selenium_TC001.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Adjust this to the absolute file path of checkout.html
HTML_PATH = "file:///absolute/path/to/assets/checkout.html"

driver = webdriver.Chrome()
driver.get(HTML_PATH)
wait = WebDriverWait(driver, 5)

# Add first product
add_btn = driver.find_element(By.CSS_SELECTOR, ".add-to-cart[data-id='p1']")
add_btn.click()
time.sleep(0.5)

# Apply discount
discount_input = driver.find_element(By.ID, "discount")
discount_input.clear()
discount_input.send_keys("SAVE15")
driver.find_element(By.ID, "apply-discount").click()
time.sleep(0.5)

# Read totals and validate 15% discount
total_text = driver.find_element(By.ID, "total").text
total_value = float(total_text)
# (For a single item of $20, subtotal=20, discounted=17, shipping standard=0 => 17.0)
assert abs(total_value - 17.0) < 0.01

# Fill user details
driver.find_element(By.ID, "name").send_keys("Test User")
driver.find_element(By.ID, "email").send_keys("test@example.com")
driver.find_element(By.ID, "address").send_keys("Some Address")
driver.find_element(By.ID, "pay-now").click()

# Verify success message visible
success = driver.find_element(By.ID, "payment-success")
assert success.is_displayed()

print("TC-001 passed")
driver.quit()
