# from sympy import Eq, solve, symbols, sympify


# word: str = "(5 + x) - (5 + y) - 7"
# symbols_list:list = []

# for i in word:
#     if i not in ["0","1","2","3","4","5","6","7","8","9","+","-","/","*", "(", ")","=", " "]:
#         symbols_list.append(symbols(i))

# equation = Eq(sympify(word), int(word[-1]))

# answer = solve(equation, symbols_list)

# print(f"The answer is : {answer}")
# import speech_recognition as sr

# m = sr.Recognizer()
# with sr.Microphone() as source:
#     print("listening....")
#     audio = m.listen(source)
#     text = m.recognize_google(audio)
#     print(text)

# import pandas as pd

# pand = pd.read_html(
#     "https://gtts.readthedocs.io/en/latest/module.html#gtts.lang.tts_langs"
# )

# print(pand)
# print(pand[0]["Top-level domain (tld)"])
