import modal

image = modal.Image.debian_slim(python_version="3.12").uv_sync(
    uv_version="0.8.11", groups=["app"]
)

app = modal.App(
    name="rag_research_assistant",
    image=image,
    secrets=[modal.Secret.from_name("openai-secret", required_keys=["OPENAI_API_KEY"])],
)


def qanda(query: str):
    #    from langchain.chains import create_retrieval_chain
    #    from langchain.chains.combine_documents import create_stuff_documents_chain
    #    from langchain_core.prompts import ChatPromptTemplate, LLMChain
    from langchain_openai import ChatOpenAI

    #    from langchain.chains.llm import LLMChain
    from langchain_core.messages import HumanMessage, SystemMessage

    llm = ChatOpenAI(
        model_name="gpt-5-mini",
        use_responses_api=True,
        output_version="responses/v1",
    )

    messages = [
        SystemMessage(content="You are a helpful assistant! Your name is Bob."),
        HumanMessage(content="What is your name?"),
    ]

    #    system_prompt = (
    #        "You are an assistant for question-answering tasks. "
    #        "Use the following pieces of retrieved context to answer "
    #        "the question. Keep your answer concise."
    #        "\n\n"
    #        "{context}"
    #    )

    llm.invoke(messages)

    #    prompt = ChatPromptTemplate.from_messages(
    #        [
    #            ("system", system_prompt),
    #            ("human", "{input}"),
    #        ]
    #    )

    #    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # question_answer_chain = create_stuff_documents_chain(llm, prompt)
    # rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    print("running query against Q&A chain.\n")
    #    result = rag_chain.invoke({"input": query}, return_only_outputs=True)
    result = llm.invoke(messages)
    #    result = llm_chain.run({
    #        "text": query
    #    })
    #    answer = result["answer"]
    return result


@app.function()
@modal.fastapi_endpoint(method="GET", docs=True)
def web(query: str):
    answer = qanda(query)
    #    if show_sources:
    #        return {
    #            "answer": answer,
    #            "sources": sources,
    #        }
    #    else:
    return {
        "answer": answer,
    }


@app.function()
def cli(query: str):
    answer = qanda(query)
    print("ANSWER:")
    print(answer)
