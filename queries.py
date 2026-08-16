import weaviate
import google.generativeai as genai
import asyncio
import edge_tts

async def get_voice(text):
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural",rate="+10%")
    await communicate.save("output.mp3")
    print("Audio saved as output.mp3")


client = weaviate.connect_to_local()
questions = client.collections.get("School")
genai.configure(api_key="AIzaSyC3pCAiP_jYxMrYO8C6alZzCYTrP11EE8A")

history=dict() # to store the history


while True:
    print("------------------------------------------")
    query=input("Ask Question: ")
    print("------------------------------------------")


    if query=="bye":
        print("Come back soon!!")
        break
    

    model1 = genai.GenerativeModel("gemini-1.5-flash")
    response = model1.generate_content(f"Given a chat history that is {history} and the latest user question that is {query} which might reference context in the chat history. Formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as it is.")



    query=response.text

    response = questions.generate.near_text(
        query=query,
        limit=5,
        grouped_task=f"Answer the question {query} in simple Indian English as a teacher."

    )

    from_rag=response.generated

    model2 = genai.GenerativeModel("gemini-1.5-flash")
    response = model2.generate_content(f"you are a teacher, teaching a student and giving a mature and simplified answer in easy english. It should be in 100 words. the query asked by that student is{query} in english, here is an output coming from a RAG model that is {from_rag} it can be right or wrong, you should give answer accordingly. Don't reveal that you are using any reference and don't use any kind of  character like '*' and only use paragraph.")


    mytext=response.text


    print(mytext)


    history[query]=mytext

    asyncio.run(get_voice(mytext))




client.close()
print("successfully connected!!!")