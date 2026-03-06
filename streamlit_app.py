import streamlit as st
from crewai import Agent, Task, Crew, Process

st.set_page_config(page_title="Локализация видеоконтента", layout="wide")

st.title("Локализация и адаптация учебного видеоконтента")

with st.expander("Настройка Агентов и Задач"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Агент 1: Переводчик")
        a1_role = st.text_input("Role", "Senior Translator")
        a1_goal = st.text_input("Goal", "Translate English lecture to Russian")
        a1_backstory = st.text_area("Backstory", "Expert in educational linguistics.")
        t1_desc = st.text_area("Описание задачи 1", "Translate the transcript into academic Russian.")

    with col2:
        st.subheader("Агент 2: Редактор")
        a2_role = st.text_input("Role", "Glossary Editor")
        a2_goal = st.text_input("Goal", "Check terminology against the glossary")
        a2_backstory = st.text_area("Backstory", "Strict university terminology expert.")
        t2_desc = st.text_area("Описание задачи 2", "Review translation and apply glossary terms.")



st.divider()
st.subheader("Ввод данных для обработки")
transcript_input = st.text_area("Вставьте транскрипцию (English):", height=150)
glossary_input = st.text_area("Вставьте глоссарий (Термин - Перевод):", height=100)


if st.button("Сохранить и запустить"):
    if not transcript_input or not glossary_input:
        st.error("Пожалуйста, заполните все поля ввода!")
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
            expected_output="A clean Russian translation."
        )
        task2 = Task(
            description=f"{t2_desc}\n\nГлоссарий: {glossary_input}",
            agent=editor,
            expected_output="Final Russian text with correct terminology."
        )

        crew = Crew(
            agents=[translator, editor],
            tasks=[task1, task2],
            process=Process.sequential
        )

        with st.spinner("Агенты работают над вашим текстом..."):
            result = crew.kickoff()
        
        st.divider()
        st.subheader("Результат:")
        st.markdown(result)