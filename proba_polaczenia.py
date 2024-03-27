import requests

# Adres URL strony do pobrania
url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/direct_frame_top.cgi'

# Dane formularza, które musimy przesłać
form_data = {
    'page_type': 'irdata',
    'DB': 'msj',
    'id': 'fds',
    'view': '1',
    'column': 'filename',
    'start': '0',
    'display_num': '100',
    'spectrum_type': '0',
    'search_type': '1',
    'search_key': 'C2H5OH',
    'ir_submit': 'Search IR Spectra'
}

# Wysłanie żądania POST i pobranie zawartości strony
response = requests.post(url, data=form_data)

# Sprawdzenie, czy żądanie zakończyło się sukcesem (kod odpowiedzi 200)
if response.status_code == 200:
    # Wyświetlenie zawartości strony
    print(response.text)
else:
    print('Wystąpił problem podczas pobierania strony:', response.status_code)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Inicjalizacja przeglądarki
driver = webdriver.Chrome()

# Adres URL strony
url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/direct_frame_top.cgi'

# Otwarcie strony
driver.get(url)

try:
    # Znajdź pole "Compound Name" i wpisz "Hexane"
    compound_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'COMPOUND_NAME')))
    compound_name_input.send_keys('Hexane')

    # Znajdź pole "Spectrum" i wybierz "MS" z rozwijanej listy
    spectrum_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'SPECTRUM')))
    spectrum_select.send_keys('MS')

    # Kliknij przycisk "Search"
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Search IR Spectra"]')))
    search_button.click()

    # Poczekaj na załadowanie wyników
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="frame"]')))

    # Pobierz zawartość wyników
    results_table = driver.find_element(By.XPATH, '//table[@class="frame"]')
    results = results_table.text
    print(results)

except TimeoutException:
    print("Nie można znaleźć elementów na stronie w określonym czasie.")
finally:
    # Zamknij przeglądarkę
    driver.quit()

