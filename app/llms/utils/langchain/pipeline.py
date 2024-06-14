from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

from app.core.config import settings
from app.core.storage import download_file_from_minio
from app.llms.models import ChatBot
from app.llms.services.chatbot_service import ChatBotService
from app.llms.services.knowledge_base_service import KnowledgeBaseService
from app.llms.utils.dependencies import get_chroma_client
from app.llms.utils.langchain.chunkers import Chunker, \
    ManualInputChunkingStrategy, RecursiveChunkingStrategy
from app.llms.utils.langchain.helpers import create_llm_model, extract_metadata, format_docs, \
    get_chat_prompt
from app.llms.utils.langchain.loaders import get_crawler_loader_data, get_document_loader_data
from app.llms.vectordb.chroma_client import ChromaClient


def load_knowledge_base_data_file(file_path: str, metadatas: list[dict]):
    temp_file_path = download_file_from_minio(settings.S3_KNOWLEDGE_BASE_BUCKET, file_path)
    data = get_document_loader_data(file_path=file_path, file=temp_file_path)
    recursive_strategy = RecursiveChunkingStrategy()
    chunker = Chunker(recursive_strategy)
    docs = chunker.chunk(data, metadatas=metadatas)
    return docs


def load_knowledge_base_crawler_data(urls: list[str], metadatas: list[dict]):
    data = get_crawler_loader_data(urls=urls)
    recursive_strategy = RecursiveChunkingStrategy()
    chunker = Chunker(recursive_strategy)
    docs = chunker.chunk(data, metadatas=metadatas)
    return docs


def load_knowledge_base_manual_input_data(manual_input: str, metadatas: list[dict]):
    manual_input_strategy = ManualInputChunkingStrategy()
    chunker = Chunker(manual_input_strategy)
    docs = chunker.chunk([manual_input], metadatas=metadatas)
    return docs


def rag_chain_with_source(retriever, prompt_callable, rag_chain_from_docs):
    setup_and_retrieval = RunnableParallel({
        "context": retriever,
        "query": RunnablePassthrough(),
        "user_prompt": RunnableLambda(prompt_callable)
    }).assign(answer=rag_chain_from_docs)
    return setup_and_retrieval


def setup_rag_chain_from_docs(output_parser, temperature):
    llm = create_llm_model(temperature)
    prompt = get_chat_prompt()
    chain = RunnablePassthrough.assign(
        context=(lambda x: format_docs(x["context"]))) | prompt | llm | output_parser
    return chain


def get_question_and_answer(question: str, chatbot_id: int, chatbot_service: ChatBotService,
                            knowledge_base_service: KnowledgeBaseService):
    from langchain_core.output_parsers import StrOutputParser
    chatbot = chatbot_service.validator.validate_exists_with_id(pk=chatbot_id, model=ChatBot)
    chroma = get_chroma_client()
    vector_db = ChromaClient(client=chroma, collection_name=str(chatbot.uuid))
    retriever = vector_db.search_embeddings()
    setup_and_retrieval = setup_rag_chain_from_docs(StrOutputParser(), chatbot.temperature)
    chain = rag_chain_with_source(retriever, lambda _: chatbot.prompt, setup_and_retrieval)
    answer_with_source = chain.invoke(question)
    context = answer_with_source.get("context")
    answer = answer_with_source.get("answer")

    extracted_metadata = extract_metadata(context)
    metadata_value = [extracted_metadata[0]] if extracted_metadata else []
    print(f"Extracted metadata values are: {extracted_metadata}")
    knowledge_bases = knowledge_base_service.get_by_metadata_values(chatbot_id, metadata_value)
    print(f"Knowledge bases objects are: {knowledge_bases}")
    print(f"Question: {question}, Chatbot ID: {chatbot_id}, Answer: {answer}, Context: {context}")
    return answer, knowledge_bases
