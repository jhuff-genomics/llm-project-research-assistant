# llm-project-research-assistant
**A research assistant that can answer queries using a frontier large language model (LLM) while contextualizing with the text from a collection of PDFs**

## :bulb: Basic idea
A collection of PDF articles in an AWS S3 bucket is ingested into chunks and stored in a vector database on disk for efficient retrieval. Upon receiving a user query, the system retrieves the relevant chunks, composing a prompt for a frontier LLM to perform retrieval-augmented generation (RAG). The generated responses cite the source PDFs.

The app is developed and deployed using an affordable, pay-as-you-go serverless cloud container service with a generous free tier. The first container ingests the PDFs and populates the knowledge base table on disk along with vector embeddings. Another container queries using a hybrid approach to retrieve text from the knowledge base and sends the augmented prompt to the LLM. A third container runs a web server for a user interface.


## :arrow_forward: Check out the live app
Website: [https://jhuff-genomics--rag-research-assistant-web.modal.run](https://jhuff-genomics--rag-research-assistant-web.modal.run)

***or***

via `curl` CLI for query strings:
```
$ curl --get \
  --data-urlencode "query=When were cats domesticated?" \
  https://jhuff-genomics--rag-research-assistant-web.modal.run
```


## :computer: Local development 

Set up local dev environment (requires [`uv` to be installed](https://docs.astral.sh/uv/getting-started/installation/)), excluding the app dependencies:
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


To run temporarily in the cloud with hot reloading:
```
$ uv run modal serve rag_research_assistant.py
```


To query the temporary endpoint (replace below with the `modal` workspace name for the deployed url or set an environmental variable, e.g.,  using `MODAL_WORKSPACE={modal workspace name}`):
``` 
$ curl --get \
  --data-urlencode "query=When were cats domesticated?" \
  https://${MODAL_WORKSPACE}--rag-research-assistant-web-dev.modal.run
```

The temporary Gradio web app can be accessed at this URL in a browser: `https://${MODAL_WORKSPACE}--rag-research-assistant-web-dev.modal.run`


## :rocket: Cloud deployment

Here is how I deployed the [live app linked above](#arrow_forward-check-out-the-live-app). The cloud container image requirements split up the `uv` dependency groups as needed.

To deploy in a serverless cloud container with `modal`:
```
$ uv run modal deploy rag-research-assistant.py
```

To query the deployed web endpoint (replace below with the `modal` workspace name for the deployed url or set an environmental variable, e.g.,  using `MODAL_WORKSPACE={modal workspace name}`):
```
$ curl --get \
  --data-urlencode "query=When were cats domesticated?" \
  https://${MODAL_WORKSPACE}--rag-research-assistant-web.modal.run
```

The deployed Gradio web app can be accessed at this URL in a browser: `https://${MODAL_WORKSPACE}--rag-research-assistant-web.modal.run`
