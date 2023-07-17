
# Automatic1111-webui Automation

A python automation script to automate the sd-webui, so to ease the task to generate thousands of images, in one go, with the help of `csv`.

## Step 1 - Clone:

- for HTTPS:
```
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
```

- for SSH:
```
    git clone git@github.com:AUTOMATIC1111/stable-diffusion-webui.git
```


## Step 2 - Installation and Running:

Follow the setps provided in the [README](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/README.md) to install and run `AUTOMATIC1111 - stable diffusion webui`

Note 1: After successfull installation, run the webui with the `api` flag, as follows:- 

```
    bash webui.sh --api
```

Note 2: After successfully running the webui, note down the `URL` at which the webui is running. For e.g.

    Running on local URL:  http://127.0.0.1:7860

 #### Important: Do not close or exit the terminal, using which sd-webui is running

## Step 3 - Clone this repo (in another terminal)

- for HTTPS:
```
    git clone https://github.com/ayushr6/sd-webui-automation.git
```

- for SSH:
```
    git clone git@github.com:ayushr6/sd-webui-automation.git
```
## Step 4 - Install required Libraries

- cd `sd-webui-automation`

run:
```
    pip install -r requirements.txt
```

## Step 5 - Setup and Running Script

### There are two ways through which you can generate images:

#### 1. using `two csv` files:

- one, which contains the unique name of actors, items, animals, etc.
- second, which contains `prompts`, which contains special characters which can be `replaced by` the name of a character, item, animal, etc from the initial csv.

Note:- The second `csv` must also contain the following parameters, `replace_with`, `model_name`, `sampling_method`, `sampling_steps`, `cfg_scale`, and `batch_count`.


for e.g.

```
first - tiny cute #### toy, soft smooth lighting, soft pastel colors, 3d blender render
second - tiger or camel or any other animal name

prompt = tiny cute tiger toy, soft smooth lighting, soft pastel colors, 3d blender render
```

This how, we can use `two csvs` to generate images for a list of characters, animals, etc. and use different prompts for each keyword.

#### Run:

for webui:

```
python scraper.py generate_images_from_two_csv --input_csv "input/animals.csv" --prompt_csv "input/animals_prompts.csv" --headless False --output_dir "output/animals"
```

for api:

```
python scraper.py generate_images_from_two_csv --input_csv "input/animals.csv" --prompt_csv "input/animals_prompts.csv" --use api --output_dir "output/animals"
```

### Parameters

    Parameter                 | Definition
    ------------------------- | -----------------------------------------------------
    `--input_csv`             | `path` to `input_csv`
    `--prompt_csv`            | `path` to `prompt_csv`
    `--webui_url`             | `url` at which `automatic1111-webui` is running
    `--model`                 | sd model name (e.g. sd-v1-4)
    `--output_dir`            | path to output_dir
    `--sampling_method`       | sampling method name (e.g. Eular a, DDIM, etc.)
    `--sampling_steps`        | sampling steps (1 - 150)
    `--batch_count`           | number of images in one batch (1 - 100)
    `--cfg_scale`             | cfg scale (1 - 30)
    `--use`                   | accepted values (webui/api)
    `--headless`              | run webui in headless mode? (True/False)
    `--add_on`                | overwrite existing content or not (`True` / `False`)


#### 2. using a `single csv` file:

- This file contains prompts, respect to while we need to generate the images.

Note:- This `csv` must also contain the following parameters, `replace_with`, `model_name`, `sampling_method`, `sampling_steps`, `cfg_scale`, and `batch_count`.

for e.g.

```
prompt - tiny cute tiger toy, soft smooth lighting, soft pastel colors, 3d blender render
```

This how, we can use `two csvs` to generate images for a list of characters, animals, etc. and use different prompts for each keyword.

#### Run:

for webui:

```
python scraper.py generate_images_from_single_csv --prompt_csv "input/famous_structures.csv" --headless False --output_dir "output/famous_structures"
```

for api:

```
python scraper.py generate_images_from_single_csv --prompt_csv "input/famous_structures.csv" --use api --output_dir "output/famous_structures"
```


### Parameters

    Parameter                 | Definition
    ------------------------- | -----------------------------------------------------
    `--prompt_csv`            | `path` to `prompt_csv`
    `--webui_url`             | `url` at which `automatic1111-webui` is running
    `--model`                 | sd model name (e.g. sd-v1-4)
    `--output_dir`            | path to output_dir
    `--sampling_method`       | sampling method name (e.g. Eular a, DDIM, etc.)
    `--sampling_steps`        | sampling steps (1 - 150)
    `--batch_count`           | number of images in one batch (1 - 100)
    `--cfg_scale`             | cfg scale (1 - 30)
    `--use`                   | accepted values (webui/api)
    `--headless`              | run webui in headless mode? (True/False)
    `--add_on`                | overwrite existing content or not (`True` / `False`)


`CFG Scale` : a parameter that controls how much the generated image matches the text prompt and/or the input image. A higher CFG scale value results in an output image more in line with the input prompt or image, but at the expense of quality. Conversely, a lower CFG scale value produces a better-quality image that may differ from the original prompt or image.

`Sampling Method/Samplers` : Samplers are used to tell the AI how it should start generating visual patterns from the initial noise. NovelAI supports a wide variety of Sampling Methods: DPM++ 2M, Euler Ancestral, Euler, DPM2, DPM++ 2S Ancestral, DPM++ SDE, DPM Fast, and DDIM. (Note: Refer to webui to see list of all samplers)

`Sampling Steps` : Sampling steps is the number of iterations that Stable Diffusion runs to go from random noise to a recognizable image based on the text prompt.