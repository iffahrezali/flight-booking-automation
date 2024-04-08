import time
import travel_info
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#Initialize the browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

def openBrowser(input_link):
    driver.get(input_link)
    driver.maximize_window()

def homePage(departure_location, arrival_location, flight_date):
    time.sleep(10)

    #Enter location for "Coming from" for departure
    departure = driver.find_elements(By.ID,'select2--container')
    departure = departure[0]
    actions = ActionChains(driver) 
    actions.move_to_element(departure) 
    actions.send_keys(departure_location)
    time.sleep(5)
    actions.perform()
    departure.click()
    time.sleep(5)
    actions.send_keys(departure_location)
    time.sleep(5)
    actions.perform()
    time.sleep(5)

    #Select the arrival location from the dropdown
    select_departure = driver.find_element(By.ID, 'select2--results')
    select_departure.click()
    time.sleep(10)
    
    #Enter location for "Going to" for arrival
    arrival = driver.find_elements(By.ID,'select2--container')
    arrival = arrival[1]
    actions = ActionChains(driver) 
    actions.move_to_element(arrival) 
    actions.send_keys(arrival_location)
    time.sleep(5)
    actions.perform()
    arrival.click()
    time.sleep(5)
    actions.send_keys(arrival_location)
    actions.perform()
    time.sleep(5)

    #Select the arrival location from the dropdown
    select_arrival = driver.find_element(By.ID, 'select2--results')
    select_arrival.click()
    time.sleep(10)

    #Enter date for flight
    depart_date = driver.find_element(By.ID, "departure")
    actions = ActionChains(driver) 
    actions.move_to_element(depart_date) 
    time.sleep(5)
    actions.perform()
    depart_date.click()
    time.sleep(5)
    depart_date.clear()
    depart_date.click()
    actions.send_keys(flight_date)
    time.sleep(5)
    actions.perform()

    #Input number of passengers based on passenger list in travel_info.py
    target_date = driver.find_element(By.PARTIAL_LINK_TEXT,"Travellers")
    target_date.click()
    target_date = driver.find_element(By.ID,"fadults")
    target_date.click()
    target_date.clear()
    target_date.send_keys(str(len(travel_info.passenger_data)))
    target_date.send_keys(Keys.ENTER)

    '''
    ================================================

    I was not able to make the following steps working as intended, hence the above code. This is for archive purpose.
    time.sleep(10)
    actions = ActionChains(driver)
    #departure = driver.find_elements(By.ID, 'select2--container')[0]

    departure = wait.until(EC.presence_of_element_located((By.ID, "select2--container")))
    #actions.move_to_element(departure).click().send_keys(departure_location).send_keys(Keys.ENTER).perform()
    actions.click().send_keys(departure_location).send_keys(Keys.ENTER).perform()
    #actions.click().send_keys(departure_location).send_keys(Keys.ENTER).perform()
    #departure.click()

    select_departure = wait.until(EC.element_to_be_clickable((By.ID, 'select2--results')))
    select_departure.click()
    #select_departure.perform()
    
    time.sleep(10)
    departure = wait.until(EC.presence_of_all_elements_located((By.ID, "select2--container")[1]))
    actions.move_to_element(departure).click().send_keys(departure_location).perform()

    select_departure = wait.until(EC.visibility_of_all_elements_located((By.ID, 'select2--results')[1]))
    actions = ActionChains(driver)
    actions.click()

    arrival = driver.find_elements(By.ID, 'select2--container')[1]
    actions.move_to_element(arrival).click().send_keys(arrival_location).perform()
    
    select_departure = driver.find_element(By.ID, 'select2--results').click()
    time.sleep(10)

    #Enter departure date
    depart_date = driver.find_element(By.ID, "departure")
    actions = ActionChains(driver).move_to_element(depart_date)
    time.sleep(5)
    actions.click(depart_date)
    depart_date.clear()
    actions.send_keys('03-04-2024').perform()
    time.sleep(5)

    #Enter number of passengers
    target_date = driver.find_element(By.PARTIAL_LINK_TEXT, "Travellers").click()
    target_date = driver.find_element(By.ID, "fadults")
    target_date.clear()
    target_date.send_keys('3', Keys.ENTER)

    ================================================
'''
def resultsPage():   
    #Pick a flight from the results 
    target_result = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="flight--list-targets"]/li[1]/form/div/div[2]/div/button[2]')))
    target_result.click()

def loginPage():
    #Iterate the first passenger info
    for field_name, main_passenger_info in travel_info.main_passenger.items():
        info = wait.until(EC.presence_of_element_located((By.NAME, "user[" + str(field_name) + "]")))
        info.click()
        info.send_keys(main_passenger_info)

    #Select the nationality of passenger
    nationality = wait.until(EC.presence_of_element_located((By.XPATH,"(//button[@title='United States'])[1]")))
    nationality.click()

    scroll_distance = 100
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

    nationality_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dropdown-menu show']//input[@aria-label='Search']")))
    nationality_input.send_keys("Malaysia")

    nationality_input = wait.until(EC.presence_of_element_located((By.ID,"bs-select-1-129")))
    nationality_input.click()

    #Input all the passengers' details from travel_info.py
    for index, passenger_details in enumerate(travel_info.passenger_data):
        first_name = passenger_details["first_name"]
        last_name = passenger_details["last_name"]
        passport_number = passenger_details["passport_number"]

        #first_name_input = driver.find_element(By.NAME,"first_name_" + str(index+1))
        first_name_input= wait.until(EC.presence_of_element_located((By.NAME,"first_name_" + str(index+1))))
        ActionChains(driver).move_to_element(first_name_input).perform()
        first_name_input.send_keys(first_name)

        #last_name_input = driver.find_element(By.NAME,"last_name_" + str(index+1))
        last_name_input = wait.until(EC.presence_of_element_located((By.NAME,"last_name_" + str(index+1))))
        last_name_input.send_keys(last_name)

        #passport_number_input = driver.find_element(By.NAME,"passport_" + str(index+1))
        passport_number_input = wait.until(EC.presence_of_element_located((By.NAME,"passport_" + str(index+1))))
        ActionChains(driver).move_to_element(passport_number_input).perform()
        passport_number_input.send_keys(passport_number)

    scroll_distance = 500
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
    time.sleep(10)

def paymentGateway():
    #Click the 'I've read the terms & conditions' tickbox
    agree = wait.until(EC.presence_of_element_located((By.ID,"agreechb")))
    ActionChains(driver).move_to_element(agree).perform()
    agree.click()

    #Confirm the booking by clicking 'Booking Confirm'
    booking = wait.until(EC.presence_of_element_located((By.ID,"booking")))
    ActionChains(driver).move_to_element(booking).perform()
    booking.submit()

    #Wait for the invoice to load
    booking = wait.until(EC.presence_of_element_located((By.ID,"form")))

    driver.quit()
    
if __name__ == "__main__":
    input_link = 'https://phptravels.net/'
    departure_location = 'Jeddah'
    arrival_location = 'Lahore'
    flight_date = '03-04-2024'
    openBrowser(input_link)
    homePage(departure_location, arrival_location, flight_date)
    resultsPage()
    loginPage()
    paymentGateway()