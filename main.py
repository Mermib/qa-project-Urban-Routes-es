import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    #Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    order_taxi = (By.CLASS_NAME, 'button.round')
    comfort_rate = (By.CSS_SELECTOR, ".tariff-cards .tcard:nth-child(5)")

    order_requirements_blanket = (By.CLASS_NAME, 'r-sw-label')
    phone = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, 'phone')
    number = (By.CLASS_NAME, 'np-text')
    next_button = (By.CLASS_NAME, "button.full")
    set_code = (By.ID, 'code')
    confirmation_code = (By.CSS_SELECTOR, '.section.active>form>.buttons>:nth-child(1)')

    payment_method = (By.CLASS_NAME, 'pp-button.filled')
    card = (By.CLASS_NAME, 'pp-plus-container')
    card_number = (By.CSS_SELECTOR, '#number.card-input')
    code_card_input = (By.CSS_SELECTOR, '#code.card-input')
    click_tab = (By.CSS_SELECTOR, '.plc')
    add_card_button = (By.CSS_SELECTOR, '.pp-buttons button.button.full')
    close_card_button = (By.CSS_SELECTOR, '.payment-picker.open button.close-button')

    driver_message = (By.ID, "comment")
    blankets_handkerchiefs = (By.CSS_SELECTOR,".reqs-body>.r-type-switch .switch > span")
    blanket_check = (By.CSS_SELECTOR, '.r-sw > div > input')
    ice_cream_plus = (By.CSS_SELECTOR, '.r-group-items>:nth-child(1) .r-counter-container .counter .counter-plus')
    get_ice = (By.CSS_SELECTOR, '.r-group-items>:nth-child(1) .r-counter-container .counter .counter-value')
    
    reserve_button = (By.CLASS_NAME, "smart-button")
    details = (By. CLASS_NAME, 'order-body')
    timer = (By.CLASS_NAME, 'order-header-content')


    #Metodos
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def order_taxi_click(self):
        self.driver.find_element(*self.order_taxi).click()

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_comfort(self):
        comfort_element = self.driver.find_element(*self.comfort_rate)
        comfort_element.click()

    def get_comfort(self):
        return self.driver.find_element(*self.order_requirements_blanket).text


    def set_comfort(self):
        self.order_taxi_click()
        self.click_comfort()

    def phone_number(self):
        self.driver.find_element(*self.phone).click()

    def set_phone_number(self):
        self.driver.find_element(*self.phone_input).send_keys(data.phone_number)

    def get_phone_number_value(self):
        return self.driver.find_element(*self.number).text

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def insert_phone_code(self):
        self.driver.find_element(*self.set_code).send_keys(retrieve_phone_code(self.driver))

    def confirmation_phone(self):
        self.driver.find_element(*self.confirmation_code).click()

    def add_new_phone_number(self):
        self.phone_number()
        self.set_phone_number()
        self.click_next_button()
        self.insert_phone_code()
        self.confirmation_phone()

    def click_payment_method(self):
        self.driver.find_element(*self.payment_method).click()

    def credit_card(self):
        self.driver.find_element(*self.card).click()

    def add_card_number(self):
        self.driver.find_element(*self.card_number).send_keys(data.card_number)

    def get_card_number(self):
        return self.driver.find_element(*self.card_number).get_property('value')

    def add_card_code(self):
        self.driver.find_element(*self.code_card_input).send_keys(data.card_code)

    def get_card_code(self):
        return self.driver.find_element(*self.code_card_input).get_property('value')

    def click_space_tab(self):
        self.driver.find_element(*self.click_tab).click()

    def add_new_credit_card(self):
        self.driver.find_element(*self.add_card_button).click()

    def close_add_card(self):
        self.driver.find_element(*self.close_card_button).click()

    def new_credit_card(self):
        self.click_payment_method()
        self.credit_card()
        self.add_card_number()
        self.add_card_code()
        self.click_space_tab()
        self.add_new_credit_card()
        self.close_add_card()

    def send_driver_message(self):
        self.driver.find_element(*self.driver_message).send_keys(data.message_for_driver)

    def get_message(self):
        return self.driver.find_element(*self.driver_message).get_property('value')

    def click_blanket_on(self):
        self.driver.find_element(*self.blankets_handkerchiefs).click()

    def get_blanket_state(self):
        return self.driver.find_element(*self.blanket_check).is_selected()

    def add_ice_cream(self):
        ice_cream_element = WebDriverWait(self.driver, 4).until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus)
        )
        ice_cream_element.click()
        ice_cream_element.click()

    def get_ice_cream(self):
        return self.driver.find_element(*self.get_ice).text

    def reserve_taxi_button(self):
        self.driver.find_element(*self.reserve_button).click()

    def get_order(self):
        return self.driver.find_element(*self.details).is_displayed()

    def driver_info(self):
        #time.sleep(20)
        WebDriverWait(self.driver, 60).until(expected_conditions.visibility_of_element_located(UrbanRoutesPage.details))
        return self.driver.find_element(*self.timer).is_displayed()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(3)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_tariff_picker(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_comfort()
        assert routes_page.get_comfort() == 'Manta y pañuelos' or routes_page.get_comfort() == "Blanket and handkerchiefs"

    def test_setup_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_new_phone_number()
        assert routes_page.get_phone_number_value() == data.phone_number

    def test_new_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.new_credit_card()
        assert routes_page.get_card_number() == data.card_number
        assert routes_page.get_card_code() == data.card_code

    def test_send_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.send_driver_message()
        assert routes_page.get_message() == data.message_for_driver

    def test_blanket(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_on()
        assert routes_page.get_blanket_state() == True

    def test_add_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream()
        assert routes_page.get_ice_cream() == '2'

    def test_click_reserve_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.reserve_taxi_button()
        assert routes_page.get_order() == True
        WebDriverWait(self.driver, 5)

    def test_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        assert routes_page.driver_info() == True
        WebDriverWait(self.driver, 5)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()