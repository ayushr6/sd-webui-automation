import os
from time import sleep
import fire
import pandas as pd
from tqdm import tqdm
import requests
import urllib.request
import io
import base64
from PIL import Image, PngImagePlugin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from configs.configs import (
    PROMPT_TEXTBOX_XPATH,
    SAMPLING_STEPS_XPATH,
    BATCH_COUNT_XPATH,
    CFG_SCALE_XPATH,
    GENERATE_BUTTON_XPATH,
    DEFAULT_INPUT_CSV_PATH,
    DEFAULT_PROMPT_CSV_PATH,
    DEFAULT_WEBUI_IP,
    DEFAULT_MODEL,
    DEFAULT_OUTPUT_DIR_PATH,
    DEFAUT_SAMPLING_METHOD,
    DEFAULT_SAMPLING_STEPS,
    DEFAULT_BATCH_COUNT,
    DEFAULT_CFG_SCALE,
    DEFAULT_USE,
    PROGRESS_BAR_XPATH,
    IMAGES_XPATH,

    SleepDuration,
)

from helpers.helpers import Helper

class Scraper:

    def _init_browser(self, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=options
        )

        
        self.helper = Helper(self.browser)

    def _init_xpaths(self):
        self.prompt_textbox = self.helper._get_element(PROMPT_TEXTBOX_XPATH)
        self.sampling_steps = self.helper._get_element(SAMPLING_STEPS_XPATH)
        self.batch_count = self.helper._get_element(BATCH_COUNT_XPATH)
        self.cfg_scale = self.helper._get_element(CFG_SCALE_XPATH)
        self.generate_button = self.helper._get_element(GENERATE_BUTTON_XPATH)
        return True
    
    def _generate_using_api(
        self,
        webui_url,
        prompt,
        model,
        sampling_method,
        sampling_steps,
        batch_count,
        cfg_scale,
        output_loc,
    ):
        payload = {
            "prompt": prompt,
            "steps": sampling_steps,
            "batch_size": batch_count,
            "cfg_scale": cfg_scale,
            "sampler_index": sampling_method,
        }

        opt = requests.get(url=f"{webui_url}/sdapi/v1/options")
        opt_json = opt.json()
        opt_json["sd_model_checkpoint"] = f"{model}"
        requests.post(url=f"{webui_url}/sdapi/v1/options", json=opt_json)

        response = requests.post(url=f"{webui_url}/sdapi/v1/txt2img", json=payload)

        r = response.json()
        alread_exists = len(os.listdir(output_loc))
        for i, img in enumerate(r["images"]):
            image = Image.open(io.BytesIO(base64.b64decode(img.split(",", 1)[0])))

            png_payload = {"image": "data:image/png;base64," + img}
            response2 = requests.post(
                url=f"{webui_url}/sdapi/v1/png-info", json=png_payload
            )

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save(
                os.path.join(output_loc, str(alread_exists + i + 1) + ".png"),
                pnginfo=pnginfo,
            )


    def _generate_using_webui(
        self,
        prompt,
        model,
        sampling_method,
        sampling_steps,
        batch_count,
        cfg_scale,
        output_loc,
    ):
        if not self.helper._set_sd_ckp(model):
            print(
                f"Either Model is not present or the Model Name ({model}) is incorrect!!"
            )
            return
        if not self.helper._set_sampling_method(sampling_method):
            print(
                f"Either Sampling Method is not present or the Sampling Method Name ({sampling_method})  is incorrect!!"
            )
            return
        self.prompt_textbox.clear()
        self.prompt_textbox.send_keys(prompt)
        self.sampling_steps.clear()
        self.sampling_steps.send_keys(sampling_steps)
        self.batch_count.clear()
        self.batch_count.send_keys(batch_count)
        self.cfg_scale.clear()
        self.cfg_scale.send_keys(cfg_scale)
        self.generate_button.click()
        sleep(SleepDuration.ONE.value)
        while True:
            try:
                progress_bar = self.helper._get_element(PROGRESS_BAR_XPATH)
            except Exception as e:      # TODO: can become an edge case
                break
        images = self.helper._get_elements(IMAGES_XPATH)
        alread_exists = len(os.listdir(output_loc))
        for i, image in enumerate(images):
            image_src = image.get_attribute("src")
            save_loc = os.path.join(output_loc, str(alread_exists + i + 1) + ".jpg")
            urllib.request.urlretrieve(image_src, save_loc)
        return [image.get_attribute("src") for image in images]

    def main(
        self,
        input_csv=DEFAULT_INPUT_CSV_PATH,
        prompt_csv=DEFAULT_PROMPT_CSV_PATH,
        webui_url=DEFAULT_WEBUI_IP,
        model=DEFAULT_MODEL,
        output_dir=DEFAULT_OUTPUT_DIR_PATH,
        sampling_method=DEFAUT_SAMPLING_METHOD,
        sampling_steps=DEFAULT_SAMPLING_STEPS,
        batch_count=DEFAULT_BATCH_COUNT,
        cfg_scale=DEFAULT_CFG_SCALE,
        use=DEFAULT_USE,
        headless=True,
        add_on=False,  # whether to add more images for a prompt, if already exists
    ):
        avail_models = Helper.get_available_models(webui_url)
        if not model in avail_models:
            print(f"Model {model} not download/available!!")

        if use == "webui":
            self._init_browser(headless)
            self.browser.get(webui_url)
            sleep(SleepDuration.TWO.value)
            self._init_xpaths()

        input_df = pd.read_csv(input_csv)
        prompt_df = pd.read_csv(prompt_csv)

        for i, input_row in tqdm(
            input_df.iterrows(), total=input_df.shape[0], desc="Generating Images"
        ):
            x = str(input_row["name"])
            if not add_on and os.path.exists(os.path.join(output_dir, x)):
                continue
            for j, prompt_row in prompt_df.iterrows():
                prompt = prompt_row["prompt"]
                replace_with = str(prompt_row["replace_with"])
                prompt = prompt.replace(replace_with, x)
                if prompt_row["model_name"] is not None:
                    model = prompt_row["model_name"]
                if prompt_row["sampling_method"] is not None:
                    sampling_method = prompt_row["sampling_method"]
                if prompt_row["sampling_steps"] is not None:
                    sampling_steps = prompt_row["sampling_steps"]
                if prompt_row["batch_count"] is not None:
                    batch_count = prompt_row["batch_count"]
                if prompt_row["cfg_scale"] is not None:
                    cfg_scale = prompt_row["cfg_scale"]

                output_loc = os.path.join(output_dir, x, f"style_{str(j+1)}")
                os.makedirs(output_loc, exist_ok=True)

                if use == "webui":
                    self._generate_using_webui(
                        prompt,
                        model,
                        sampling_method,
                        sampling_steps,
                        batch_count,
                        cfg_scale,
                        output_loc,
                    )
                elif use == "api":
                    self._generate_using_api(
                        webui_url,
                        prompt,
                        model,
                        sampling_method,
                        sampling_steps,
                        batch_count,
                        cfg_scale,
                        output_loc,
                    )
                else:
                    print("Invalid 'use' type!!")
                    return

if __name__ == "__main__":
    fire.Fire(Scraper)
