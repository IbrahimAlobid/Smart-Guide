# This Project For traning About LLM


## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n llm-env python=3.8
```
3) Activate the environment:
```bash
$ conda activate llm-env
```
4) to Add this environment to jupyter first install ipykernel 

```bash
$ conda install ipykernel 
```
4) to Add this environment to jupyter first install ipykernel 

```bash
$ python -m ipykernel install --user --name=llm-env
```

### Setup the environment variables

```bash
$ cp .env.example .env
```


Set your environment variables in the `.env` file. Like `TOGETHER_API_KEY` value.