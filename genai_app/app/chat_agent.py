from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
import os

def chat_with_memory(user_id, message):
    vector_path = f"../vector_store/{user_id}_store"
    if not os.path.exists(vector_path):
        return {"response": "No data found for this user."}

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local(vector_path, embeddings)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )

    result = qa.run(message)
    return {"response": result}
