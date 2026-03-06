import os
import streamlit as st
from crewai import LLM, Agent, Process, Task, Crew

st.set_page_config(page_title="Локализация видеоконтента", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Ключ GOOGLE_API_KEY не найден в Secrets!")
    st.stop()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.5
)

st.title("Локализация и адаптация учебного видеоконтента")

with st.expander("Настройка Агентов и Задач"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Агент 1: Переводчик")
        a1_role = st.text_input("Role 1", "Специалист по академическому переводу")
        a1_goal = st.text_input("Goal 1", "Переводить материалы с сохранением точности")
        a1_backstory = st.text_area("Backstory 1", "Эксперт в области лингвистики.")
        t1_desc = st.text_area("Task Description 1", "Перевести текст лекции на русский.")

    with col2:
        st.subheader("Агент 2: Редактор")
        a2_role = st.text_input("Role 2", "Эксперт по глоссарию")
        a2_goal = st.text_input("Goal 2", "Проверять терминологию")
        a2_backstory = st.text_area("Backstory 2", "Специалист по терминологии и глоссариям.")
        t2_desc = st.text_area("Task Description 2", "Сверить перевод с глоссарием.")

st.divider()
st.subheader("Ввод данных для обработки")

transcript_input = st.text_area("Вставьте транскрипцию (English):", height=150)
glossary_input = st.text_area("Вставьте глоссарий (Термин - Перевод):", height=100)

if st.button("Сохранить и запустить"):
    if not transcript_input or not glossary_input:
        st.error("Пожалуйста, заполните все поля.")
    else:
        translator_agent = Agent(
            role=a1_role,
            goal=a1_goal,
            backstory=a1_backstory,
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        editor_agent = Agent(
            role=a2_role,
            goal=a2_goal,
            backstory=a2_backstory,
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        task1 = Task(
            description=f"{t1_desc}\n\nТекст: {transcript_input}",
            agent=translator_agent,
            expected_output="Точный перевод текста."
        )

        task2 = Task(
            description=f"{t2_desc}\n\nГлоссарий: {glossary_input}",
            agent=editor_agent,
            context=[task1],
            expected_output="Финальный текст с проверенными терминами."
        )

        crew = Crew(
            agents=[translator_agent, editor_agent],
            tasks=[task1, task2],
            process=Process.sequential
        )

        with st.spinner("Агенты работают..."):
            result = crew.kickoff()

        st.divider()
        st.subheader("Результат:")
        st.markdown(result.raw if hasattr(result, "raw") else result)