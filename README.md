# llm-project-research-assistant
**A research assistant that can answer questions about the text in a collection of PDFs using a frontier large language model (LLM)**

## :bulb: Basic idea
A collection of PDF articles hosted in a public AWS S3 are ingested into chunks and stored in a vector database for efficient retrieval. Upon receiving a user query, the system retrieves the relevant chunks, composing a prompt for the LLM to perform retrieval-augmented generation (RAG). The generated responses cite the source PDFs.

The app is developed and deployed in an inexpensive, pay-as-you-go serverless cloud container service. One container runs the vector knowledge base in memory, persisted to disk for each S3 bucket ingested, and calls the LLM. Another container runs the web server for the user interface.


## :arrow_forward: Check out the live app
Website: [https://jhuff-genomics--rag-research-assistant-web.modal.run](https://jhuff-genomics--rag-research-assistant-web.modal.run)

***or***

via `curl` CLI for query strings:
```
$ curl --get \
  --data-urlencode "query=What did the president say about Justice Breyer" \
  https://jhuff-genomics--rag-research-assistant-web.modal.run
```


## :computer: Local development 

Set up dev environment (requires [`uv`to be installed](https://docs.astral.sh/uv/guides/install-python/)), excluding all of the app dependencies:
```
$ uv sync --no-group app
```
Install pre-commits if intend to commit with `git`: 
```
$ pre-commit install
```


## :cloud: To run and deploy serverless in the cloud, first set up [Modal Labs (modal.com)](https://modal.com)

Create a free Modal account (or link an existing one) by running:
```
$ uv run modal setup
```


## :construction: Cloud testing and web endpoint

**Prerequisite**: Make sure a valid secret `openai-secret` is set up in your [Modal Secrets](https://modal.com/secrets/), which should contain `OPENAI_API_KEY` (that you get for the [OpenAI API](https://platform.openai.com/api-keys)). Use of [Modal Secrets](https://modal.com/secrets/) ensures the key is kept secure.


To run an example once in the cloud via `modal`:
```
$  uv run modal run rag_research_assistant.py \
   --query "When were cats domesticated?" \
   --show-sources
```


To run a temporarily in a cloud with hot reloading:
```
$ uv run modal serve rag_research_assistant.py
```


To query the temporary endpoint:
```
$ MODAL_WORKSPACE={modal workspace name}
# replace with the workspace name for the url below
    
$ curl --get \
  --data-urlencode "query=When were cats domesticated?" \
  https://${MODAL_WORKSPACE}--rag-research-assistant-web-dev.modal.run
```

The temporary Gradio web app can be accessed at this URL in a browser: `https://${MODAL_WORKSPACE}--rag-research-assistant-web-dev.modal.run`


## :rocket: Cloud deployment

Here is how I deployed the live app linked at the top.

To deploy in a serverless cloud container with `modal`:
```
$ uv run modal deploy potus_speech_qanda.py
```

To query the deployed web endpoint (replace below with the `modal` workspace name for the deployed url or set an environmental variable for `MODAL_WORKSPACE`):
```
$ curl --get \
  --data-urlencode "query=What did the president say about Justice Breyer" \
  https://${MODAL_WORKSPACE}--example-potus-speech-qanda-web.modal.run
```

The deployed Gradio web app can be accessed at this URL in a browser: `https://${MODAL_WORKSPACE}--rag-research-assistant-web.modal.run`
