# Rapid Reading

Simple approach to extracting key data from research papers using ChatGPT

Presentation Slides - https://docs.google.com/presentation/d/1wEWF4xYZ_1bqAqaCeppcnlnq0wwJ0hTkTvQCsRPHPN0/edit?usp=sharing

## Set Up

### Installing Packages

Use [pip](https://pip.pypa.io/en/stable/) to install the following packages - python flask, openai and openpyxl.

```bash
pip install flask
pip install openai
pip install openpyxl
```

### Obtaining an API Key

To obtain an API key from OpenAI, follow the steps below:

1. Log in to your OpenAI account on the OpenAI website.
2. Navigate to the API section, usually located in the account settings or developer settings area.
3. If required, provide any necessary information or complete any necessary steps to enable API access for your account.
4. Locate the option to generate an API key, often labeled as "Generate API Key" or something similar.
5. Click on the "Generate API Key" button to generate a new API key.
6. Once the key is generated, securely copy it to your clipboard or save it in a secure location.

### Changing the Code

Replace your api key in the medthread.py file as shown below -

```python
openai.api_key = '[YOUR_API_KEY]'
```

Replace your excel file path name as well in the medthread.py file as shown below -

```python
file_path = "[YOUR_EXCEL_FILE_PATH]"
```

## Running the Application

From the directory where medthread.py file is saved, open the terminal and run the following command -

```bash
python summarizer.py
```
