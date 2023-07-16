
# automatic1111-automation

## Step 1 - Clone:

- for HTTPS:
```
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
```

- for SSH:
```
    git clone git@github.com:AUTOMATIC1111/stable-diffusion-webui.git
```

## Step 2 - Install the dependencies:

```
# Debian-based:
    sudo apt install wget git python3 python3-venv

# Red Hat-based:
    sudo dnf install wget git python3

# Arch-based:
    sudo pacman -S wget git python3
```


## Step 3 - Installation and Running:

Follow the setps provided in the [README](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/README.md) to install and run `AUTOMATIC1111 - stable diffusion webui`

Note: After successfully running the webui, note down the `URL` at which the webui is running. For e.g.

    Running on local URL:  http://127.0.0.1:7860


## Step 4 - Clone this repo

- for HTTPS:
```
    git clone https://github.com/deepklarity/exploration.git
```

- for SSH:
```
    git clone git@github.com:deepklarity/exploration.git
```
## Step 5 - Install required Libraries

- cd `exploration/automatic1111`

run:
```
    pip install -r requirements.txt
```

## Step 6 - Setup and Running Script

##### 1. create `two csv` files:

- one, which contains the unique name of characters, items, animals, etc.
- second, which contains `prompts`, which contains characters which can be `replaced by` the name of a character, item, animal, etc.

Note:- The second `csv` may also contain options parameters, such as, `sampling_method`, `sampling_steps`, `batch_count` and `cfg_scale`.

At last, run:
```
    python script.py main --input_csv "input/animals.csv" --prompt_csv "input/animals_prompts.csv" --output_dir "output/animals" --sampling_steps 15 --batch_count 4 --cfg_scale 20 --use "webui"
```

```
    python script.py main --input_csv "input/animals.csv" --prompt_csv "input/animals_prompts.csv" --output_dir "output/animals" --sampling_steps 25 --batch_count 8 --cfg_scale 15 --use "api"
```