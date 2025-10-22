
import streamlit as st
import pandas as pd
import random

# Laadime sõnad Exceli failist, alates 2. reast
words = pd.read_excel("Sonad.xlsx", sheet_name="Leht1", skiprows=2, usecols=["Unnamed: 5", "Unnamed: 6"], engine="openpyxl")
words.columns = ['Spanish', 'Estonian']
words = words.dropna().reset_index(drop=True)

# Funktsioon uue sõna lisamiseks
def add_new_word(spanish, estonian):
    new_row = pd.DataFrame([[spanish, estonian]], columns=['Spanish', 'Estonian'])
    global words
    words = pd.concat([words, new_row], ignore_index=True)
    # Salvestame uue sõna Exceli faili
    df_new = pd.DataFrame(words)
    df_new.to_excel("Sonad.xlsx", sheet_name="Leht1", index=False, engine="openpyxl")

# Funktsioon vastuse kontrollimiseks
def check_answer():
    user_answer = st.session_state.user_answer.strip().lower()
    correct_answer = st.session_state.correct_answer.strip().lower()
    if user_answer == correct_answer:
        st.session_state.feedback = f"✅ Õige vastus!"
    else:
        st.session_state.feedback = f"❌ Vale vastus. Õige on: {st.session_state.correct_answer}"
    # Genereeri uus küsimus
    new_index = random.choice(words.index)
    ask_in_spanish = random.choice([True, False])
    st.session_state.current_word = new_index
    st.session_state.ask_in_spanish = ask_in_spanish
    st.session_state.user_answer = ""

# Streamlit UI
st.title("Hispaania keele sõnade õppimise äpp")

# Küsimuse genereerimine
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(words.index)
    st.session_state.ask_in_spanish = random.choice([True, False])
    st.session_state.feedback = ""
    st.session_state.user_answer = ""

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

st.session_state.correct_answer = correct_answer

st.text_input("Sinu vastus", key="user_answer", on_change=check_answer)

if st.session_state.feedback:
    st.write(st.session_state.feedback)

# Uue sõna lisamine
st.write("---")
st.subheader("Lisa uus sõna")
new_spanish = st.text_input("Hispaania keeles", key="new_spanish")
new_estonian = st.text_input("Eesti keeles", key="new_estonian")

if st.button("Lisa sõna"):
    if new_spanish and new_estonian:
        add_new_word(new_spanish, new_estonian)
        st.success("Sõna lisatud!")
    else:
        st.error("Palun täida mõlemad väljad.")
