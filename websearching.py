# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-ffaec16e92bd4bc8a721a0fbc8271b52")  # Replace with your actual key


response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Use an OpenAI model
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)





# import asyncio
# import edge_tts

# async def get_voice(text):
#     communicate = edge_tts.Communicate(text, "en-AU-NatashaNeural", rate="+10%")
#     await communicate.save("output.mp3")
#     print("Audio saved as output.mp3")

# # Run the async function properly
# text='''Okay, beta, let's talk about acids.  It's a simple concept, but it's important to understand it properly.  Think of it like this:  everything around us is made up of tiny, tiny particles called atoms, right? These atoms sometimes join hands to form bigger groups called molecules.  Acids are a special type of molecule.

# What makes an acid special?  Well, acids have a particular characteristic: they give away a proton. Now, don't get scared by the word "proton".  Think of it as a tiny positively charged particle, like a little bit of positive electricity.  When an acid molecule is put in water, it readily releases this tiny positive charge, this proton.  That's the key thing about acids. They are proton donors. They are happy to give away this positive particle.

# Now, you might be thinking, "So what?"  Well, this giving away of the proton is what makes acids have their special properties.  For example, acids often taste sour. Think of the sour taste of lemon juice – that's because lemon juice contains citric acid.  Or think of the vinegar you use in your food – that's acetic acid.  The sour taste is a result of these acids releasing their protons.

# Another characteristic of acids is that they can react with certain metals.  If you put some zinc metal into some acid, like hydrochloric acid, you'll see bubbles forming.  This is because the acid is reacting with the metal, releasing hydrogen gas.  This is a chemical reaction, a change at the atomic level.  The acid is not just mixing with the metal; it's actually interacting with it at a fundamental level.

# Acids also change the color of certain substances called indicators.  You might have seen litmus paper in your science class.  This paper changes color when it comes into contact with an acid.  It usually turns red.  This is a very simple way to tell if something is acidic.  Different indicators change color in different ways, but they all react to the presence of the proton released by acids.

# Now, the strength of an acid depends on how easily it gives away its proton. Some acids are strong acids, meaning they readily release their protons in water. Examples include hydrochloric acid (found in your stomach to help digest food) and sulfuric acid (used in car batteries).  These are powerful acids, and you need to handle them carefully.

# Other acids are weak acids, meaning they don't release their protons as readily.  Acetic acid (in vinegar) and citric acid (in lemons) are examples of weak acids. These are much safer to handle.  The difference lies in how much of the acid actually releases its proton in water. Strong acids do it almost completely, while weak acids only do it partially.

# Think of it like this: imagine you have a group of very generous people (strong acid) and a group of less generous people (weak acid). The generous people readily give away their things (protons), while the less generous people are more hesitant.  The strength of an acid simply reflects this willingness to give away protons.

# So, to summarize, acids are molecules that readily donate protons when dissolved in water. This proton donation leads to the characteristic sour taste, reactions with metals, and color changes in indicators.  The strength of an acid depends on how readily it gives away its protons. Remember, always handle acids with care, especially strong ones, as they can be corrosive and dangerous.  Always follow the safety instructions provided by your teacher or the lab manual.  Understanding acids is a crucial step in understanding chemistry, and it opens up a world of possibilities for scientific exploration.'''
# asyncio.run(get_voice(text))





# response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': 'Current complaints of the citizens for government of india'}])
# print(response['message']['content'])


'''
f"you are a teacher, teaching a student and giving a mature answer in 1000 words to his or her query that is{query} and here is a response given by DuckDuckGo search tool on the behalf of that query that is {duck_answer}, you should behave like you know the answer and don't reveal that you are using any reference."'''