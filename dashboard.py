import streamlit as st
import pandas as pd

# Load the Excel file
file_path = r"C:\Users\NSPIRA\Downloads\EXAM SYLLABUS_COMP_24-25.xlsx"
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Extract unique dates
unique_dates = data['DATE'].unique()

# Function to filter data based on selected date
def get_exam_details(selected_date):
    filtered_data = data[data['DATE'] == selected_date]
    exam_type = filtered_data['TYPE OF EXAM'].unique()[0]
    
    # Prepare class-wise data
    class_data = {}
    for class_ in ['VI', 'VII', 'VIII', 'IX', 'X']:
        class_filtered_data = filtered_data[filtered_data['CLASS'] == class_]
        if not class_filtered_data.empty:
            class_data[class_] = class_filtered_data[['SUBJECT', 'SYLLABUS']].reset_index(drop=True)
    
    return exam_type, class_data

# Streamlit UI
st.title('Exam Schedule Dashboard')

# Date selection
selected_date = st.selectbox('Select a date', unique_dates)

if selected_date:
    exam_type, class_data = get_exam_details(selected_date)
    
    st.subheader(f"Type of Exam: {exam_type}")
    
    for class_ in ['VI', 'VII', 'VIII', 'IX', 'X']:
        if class_ in class_data:
            st.markdown(f"### Class: {class_}")
            for idx, row in class_data[class_].iterrows():
                st.write(f"**Subject:** {row['SUBJECT']}")
                st.write(f"Syllabus: {row['SYLLABUS']}")
                st.write("---")
