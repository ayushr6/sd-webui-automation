import fire
from time import sleep
import requests

from configs.configs import (
    SD_CKP_DROPDOWN_XPATH,
    SD_CKP_LIST_XPATH,
    SD_CKP_PROGRESS_BAR_XPATH,
    SAMPLING_METHOD_DROPDOWN_XPATH,
    SAMPLING_METHOD_LIST_XPATH,

    SleepDuration,
)

from selenium.webdriver.common.by import By

class Helper:

    def __init__(self, browser):
        self.browser = browser

    def get_available_models(url):
        response = requests.get(f'{url}/sdapi/v1/sd-models')
        if response.status_code == 200:
            models_data = response.json()
            model_names = [model.get('model_name') for model in models_data]
            return model_names
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
        
    def _set_sd_ckp(self, model):
        sd_ckp_dropdown = self._get_element(SD_CKP_DROPDOWN_XPATH)
        sd_ckp_dropdown.click()
        sleep(SleepDuration.TWO.value)
        sd_ckp_list = self._get_elements(SD_CKP_LIST_XPATH)
        for sd_ckp in sd_ckp_list:
            sd_ckp_name = sd_ckp.get_attribute("aria-label")
            if model in sd_ckp_name:
                sd_ckp.click()
                sleep(SleepDuration.HALF.value)
                while True:
                    try:
                        progress_bar = self._get_element(SD_CKP_PROGRESS_BAR_XPATH)
                    except Exception as e:
                        break
                return True
        return False
    
    def _set_sampling_method(self, sampling_method):
        sm_dropdown = self._get_element(SAMPLING_METHOD_DROPDOWN_XPATH)
        sleep(SleepDuration.HALF.value)
        sm_dropdown.click()
        sleep(SleepDuration.HALF.value)
        sm_list = self._get_elements(SAMPLING_METHOD_LIST_XPATH)
        for sm in sm_list:
            sm_name = sm.get_attribute("aria-label")
            if sampling_method == sm_name:
                sm.click()
                sleep(SleepDuration.ONE.value)
                return True
        return False

    def _get_element(self, xpath):
        sleep(SleepDuration.ONE.value)
        return self.browser.find_element(By.XPATH, xpath)

    def _get_elements(self, xpath):
        sleep(SleepDuration.ONE.value)
        return self.browser.find_elements(By.XPATH, xpath)