

### Overview
This project implements a Song Recommendation Engine using ollama and K-Nearest Neighbors with the Spotify Music Dataset.

### Installation
To get started, clone this repository and install the required packages using pip:

```bash
pip install -r requirements.txt
```

Install and run ollama's llama3.2-vision:

```bash
ollama run llama3.2-vision
```

Set up the customized llama3.2-vision:

```bash
ollama create music -f ./ollama/Modelfile
```

### Usage
To run the application, execute the following command:

```bash
cd streamlit
streamlit run tmp.py
```