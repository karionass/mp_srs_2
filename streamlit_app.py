import os
import streamlit as st
from crewai import Agent, Process, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI # Импортируем Gemini

if 'GOOGLE_API_KEY' in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Ключ GOOGLE_API_KEY не найден!")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    verbose=True,
    temperature=0.5,
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)

st.set_page_config(page_title="Локализация видеоконтента", layout="wide")

st.title("Локализация и адаптация учебного видеоконтента")

with st.expander("Настройка Агентов и Задач"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Агент 1: Переводчик")
        a1_role = st.text_input("Role", "Специалист по академическому переводу")
        a1_goal = st.text_input("Goal", "Переводить учебные материалы с сохранением академической точности")
        a1_backstory = st.text_area("Backstory", "Эксперт в области образовательной лингвистики.")
        t1_desc = st.text_area("Описание задачи 1", "Переводить транскрипцию с английского на академический русский.")

    with col2:
        st.subheader("Агент 2: Редактор")
        a2_role = st.text_input("Role", "Эксперт по глоссарию")
        a2_goal = st.text_input("Goal", "Проверять терминологию по глоссарию")
        a2_backstory = st.text_area("Backstory", "Строгий эксперт по университетской терминологии.")
        t2_desc = st.text_area("Описание задачи 2", "Проверять перевод и применять термины из глоссария.")

        translator = Agent(
            role=a1_role,
            goal=a1_goal,
            backstory=a1_backstory,
            llm=llm,
            verbose=True
        )

        editor = Agent(
            role=a2_role,
            goal=a2_goal,
            backstory=a2_backstory,
            llm=llm,
            verbose=True
        )

st.divider()
st.subheader("Ввод данных для обработки")
transcript_input = st.text_area("Вставьте транскрипцию (English):", height=150)
glossary_input = st.text_area("Вставьте глоссарий (Термин - Перевод):", height=100)


if st.button("Сохранить и запустить"):
    if not transcript_input or not glossary_input:
        st.error("Пожалуйста, заполните все поля перед запуском.")
    else:
        translator = Agent(
            role=a1_role, goal=a1_goal, backstory=a1_backstory, verbose=True
        )
        editor = Agent(
            role=a2_role, goal=a2_goal, backstory=a2_backstory, verbose=True
        )

        task1 = Task(
            description=f"{t1_desc}\n\nТекст: {transcript_input}",
            agent=translator,
            expected_output="Перевод транскрипции на академический русский язык."
        )
        task2 = Task(
            description=f"{t2_desc}\n\nГлоссарий: {glossary_input}",
            agent=editor,
            expected_output="Финальный русский текст с правильной терминологией."
        )

        crew = Crew(
            agents=[translator, editor],
            tasks=[task1, task2],
            process=Process.sequential
        )

        with st.spinner("Агенты работают..."):
            result = crew.kickoff()
        
        st.divider()
        st.subheader("Результат:")
        st.markdown(result)
