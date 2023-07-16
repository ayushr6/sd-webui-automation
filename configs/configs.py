from enum import Enum

DEFAULT_INPUT_CSV_PATH = "input/animals.csv"
DEFAULT_PROMPT_CSV_PATH = "input/animals_prompts.csv"
DEFAULT_WEBUI_IP = "http://127.0.0.1:7860"
DEFAUT_SAMPLING_METHOD = "DDMI"
DEFAULT_SAMPLING_STEPS = 20
DEFAULT_BATCH_COUNT = 8
DEFAULT_CFG_SCALE = 15
DEFAULT_USE = "webui"
DEFAULT_OUTPUT_DIR_PATH = "output"
SD_CKP_DROPDOWN_XPATH = "//div[@id='setting_sd_model_checkpoint']"
SD_CKP_LIST_XPATH = "//div[@id='setting_sd_model_checkpoint']//ul/li"
SD_CKP_PROGRESS_BAR_XPATH = "//div[@class='wrap default svelte-j1gjts']"
SAMPLE_PROMPT = "Funko pop Yoda figurine, made of plastic, product studio shot, on a white background, diffused lighting, centered"
DEFAULT_MODEL = "sd-v1-4"
PROMPT_TEXTBOX_XPATH = "//div[@id='txt2img_prompt']//textarea"
PROGRESS_BAR_XPATH = "//div[@class='progress']"
SAMPLING_METHOD_DROPDOWN_XPATH = "//div[@id='txt2img_sampling']//label/div/div/div"
SAMPLING_METHOD_LIST_XPATH = "//div[@id='txt2img_sampling']//ul//li"
SAMPLING_STEPS_XPATH = "//div[@id='txt2img_steps']/div/div/input"
BATCH_COUNT_XPATH = "//div[@id='txt2img_batch_count']/div/div/input"
CFG_SCALE_XPATH = "//div[@id='txt2img_cfg_scale']/div/div/input"
GENERATE_BUTTON_XPATH = "//div[@id='txt2img_generate_box']//button[3]"
IMAGES_XPATH = "//div[@id='txt2img_gallery']//img"

class SleepDuration(Enum):
    HALF = 0.5
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5