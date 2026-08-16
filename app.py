
import google.generativeai as genai

def taking_input():
    text=input()
    return text

genai.configure(api_key="AIzaSyC3pCAiP_jYxMrYO8C6alZzCYTrP11EE8A")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(taking_input())
mytext=response.text
print(mytext)
def from_app():
    return mytext








#AIzaSyDpgibC7-ymOft7He5fpJEA7jwcxwD8ku0
# import google.generativeai as genai
# from gtts import gTTS

# genai.configure(api_key="AIzaSyC3pCAiP_jYxMrYO8C6alZzCYTrP11EE8A")
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("evaporation kya hota h in hinglish and it should be long enough to speak it upto 5 min")
# print(response.text)
# mytext=response.text
# myobj=gTTS(text=mytext, lang='en-IN', slow=False)
# myobj.save("welcome.mp3")