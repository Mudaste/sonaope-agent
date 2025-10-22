
import streamlit as st
import pandas as pd
import random

# Laadime sõnad Exceli failist
df = pd.read_excel("Sonad.xlsx", sheet_name="Leht1", engine="openpyxl")

# Eemaldame tühjad read ja valime ainult vajalikud veerud
words = df.iloc[3:, [5, 6]].dropna()
words.columns = ['Spanish', 'Estonian']
words = words.reset_index(drop=True)

# Funktsioon uue sõna lisamiseks
def add_new_word(spanish, estonian):
    new_row = pd.DataFrame([[spanish, estonian]], columns=['Spanish', 'Estonian'])
    global words
    words = pd.concat([words, new_row], ignore_index=True)
    # Salvestame uue sõna Exceli faili
    df_new = pd.DataFrame(words)
    df_new.to_excel("Sonad.xlsx", sheet_name="Leht1", index=False, engine="openpyxl")

# Streamlit UI
st.title("Hispaania keele sõnade õppimise äpp")

# Küsimuse genereerimine
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(words.index)
    st.session_state.ask_in_spanish = random.choice([True, False])

current = st.session_state.current_word
ask_in_spanish = st.session_state.ask_in_spanish

if ask_in_spanish:
    question = words.loc[current, 'Spanish']
    correct_answer = words.loc[current, 'Estonian']
    st.write(f"Mis tähendab: **{question}** eesti keeles?")
else:
    question = words.loc[current, 'Estonian']
    correct_answer = words.loc[current, 'Spanish']
    st.write(f"Kuidas on eesti keeles: **{question}** hispaania keeles?")

user_answer = st.text_input("Sinu vastus")

if st.button("Kontrolli vastust"):
    if user_answer.strip().lower() == correct_answer.strip().lower():
        st.success("Õige vastus!")
    else:
        st.error(f"Vale vastus. Õige on: {correct_answer}")
    # Uus küsimus
    st.session_state.current_word = random.choice(words.index)
    st.session_state.ask_in_spanish = random.choice([True, False])

# Uue sõna lisamine
st.write("---")
st.subheader("Lisa uus sõna")
new_spanish = st.text_input("Hispaania keeles")
new_estonian = st.text_input("Eesti keeles")

if st.button("Lisa sõna"):
    if new_spanish and new_estonian:
        add_new_word(new_spanish, new_estonian)
        st.success("Sõna lisatud!")
    else:
        st.error("Palun täida mõlemad väljad.")
