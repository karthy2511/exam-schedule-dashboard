import streamlit as st
import pandas as pd

# Set the file path to the Excel file
file_path = 'EXAM SYLLABUS_COMP_24-25.xlsx'

# Load the Excel file
try:
    data = pd.read_excel(file_path, sheet_name='Sheet1')
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# Extract unique dates
unique_dates = data['DATE'].unique()

# Function to filter data based on selected date
def get_exam_details(selected_date):
    filtered_data = data[data['DATE'] == selected_date]
    exam_type = filtered_data['TYPE OF EXAM'].unique()[0]
    
    # Prepare class-wise data with programs
    class_program_data = {}
    for class_ in ['VI', 'VII', 'VIII', 'IX', 'X']:
        class_filtered_data = filtered_data[filtered_data['CLASS'] == class_]
        if not class_filtered_data.empty:
            programs = class_filtered_data['PROGRAM'].unique()
            program_data = {}
            for program in programs:
                program_filtered_data = class_filtered_data[class_filtered_data['PROGRAM'] == program]
                program_data[program] = program_filtered_data[['SUBJECT', 'SYLLABUS']].reset_index(drop=True)
            class_program_data[class_] = program_data
    
    return exam_type, class_program_data

# Streamlit UI
st.title('Exam Schedule Dashboard')

# Date selection
selected_date = st.selectbox('Select a date', unique_dates)

if selected_date:
    exam_type, class_program_data = get_exam_details(selected_date)
    
    st.subheader(f"Type of Exam: {exam_type}")
    
    for class_ in ['VI', 'VII', 'VIII', 'IX', 'X']:
        if class_ in class_program_data:
            st.markdown(f"### Class: {class_}")
            for program, data in class_program_data[class_].items():
                st.markdown(f"#### Program: {program}")
                for idx, row in data.iterrows():
                    st.write(f"**Subject:** {row['SUBJECT']}")
                    st.write(f"Syllabus: {row['SYLLABUS']}")
                    st.write("---")

