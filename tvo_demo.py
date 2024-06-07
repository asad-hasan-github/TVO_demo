import streamlit as st
import pandas as pd
import plotly.express as px

# Import csv
df = pd.read_csv('tvo_test_data_final.csv')

# Title
st.markdown("<h1 style='text-align: center; color: white;'>TVO Media Education Group <br> Quick Demo</h1>", unsafe_allow_html=True)

# Text
st.markdown("Thought I'd put this together just to show my genuine interest in the position!")
st.markdown("I looked into any data I could find publicly as just some sample data to use and ended up manually building a dataset off the course information given by tvo ILC:")
st.markdown("https://www.ilc.org/collections/all-courses?uff_6qd9x4_metafield%3Acourse.language=English")
st.markdown("Wanted to add more to this dataset somehow so ended up merging the course codes to the public provincial historic course enrolment data (2011-2022) for the overall demand over time:")
st.markdown("https://data.ontario.ca/dataset/course-enrolment-in-secondary-schools")

# Divider
st.markdown("""<hr style="height:10px;border:none;color:#FFFFFF;background-color:#FFFFFF;" /> """, unsafe_allow_html=True)

# General Distributions Title
st.markdown("<h1 style='text-align: center; color: white;'>General Distributions</h1>", unsafe_allow_html=True)

# Multiselect for grade
Grade_options = df['Grade'].unique().tolist()
selected_grades = st.multiselect('Select grade(s):', Grade_options)

# Filter the DataFrame based on the selected grades
if not selected_grades:  # If no grades selected, show all rows
    filtered_df = df
else:
    filtered_df = df[df['Grade'].isin(selected_grades)]

## CHART 1 (BAR CHART) ##
# Group the DataFrame by 'Subject' and 'Type' and count the number of courses in each category
grouped_df = filtered_df.groupby(['Subject', 'Type']).size().reset_index(name='Count')

# Sort the DataFrame by count in descending order
sorted_df = grouped_df.sort_values(by='Count', ascending=False)

st.subheader('Course Distribution by Subject and Type')

# Plot bar chart using sorted DataFrame
fig = px.bar(sorted_df, x='Subject', y='Count', color='Type')

# Customize the order of x-axis labels
fig.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig)


## CHART 3 (PIE CHART) ##
st.subheader('Course Distribution by Subject')
fund_counts = filtered_df['Subject'].value_counts()
fig = px.pie(names=fund_counts.index, values=fund_counts.values)
st.plotly_chart(fig)

## CHART 4 (BOX PLOT) ##
st.subheader('Box Plot of Number of Lessons per Course by Subject')
fig = px.box(filtered_df, x='Subject', y='Lessons')
st.plotly_chart(fig)

## CHART 4 (SUNBURST CHART) ##
st.subheader('Comprehensive Sunburst Chart')
st.markdown("**(Click inner circles to interact)**")

fig = px.sunburst(
    filtered_df,
    path=['Type', 'Subject', 'Course Code'],
    values='Lessons'
)

st.plotly_chart(fig)

# Divider
st.markdown("""<hr style="height:10px;border:none;color:#FFFFFF;background-color:#FFFFFF;" /> """, unsafe_allow_html=True)

# Course Specific Information Title
st.markdown("<h1 style='text-align: center; color: white;'>Course Specific Information</h1>", unsafe_allow_html=True)

st.subheader(f'Enrollment per Academic Year (Across Ontario Schools)')

# Sidebar to select course code
course_code = st.selectbox('Select Course Code', filtered_df['Course Code'])

# Filter data based on selected course code
filtered_data = filtered_df[filtered_df['Course Code'] == course_code]

# Exclude the next 5 columns after the first column
filtered_data = filtered_data.iloc[:, [0] + list(range(7, len(filtered_df.columns)))]

# Plot chart if data is available for the selected course code
if not filtered_data.empty:
    # Melt DataFrame to long-form
    melted_df = pd.melt(filtered_data, id_vars=['Course Code'], var_name='Academic Year', value_name='Enrollment')

    # Plot line plot
    fig = px.line(melted_df, x='Academic Year', y='Enrollment')
    st.plotly_chart(fig)
else:
    st.write('No data available for the selected course code.')

# Divider
st.markdown("""<hr style="height:10px;border:none;color:#FFFFFF;background-color:#FFFFFF;" /> """, unsafe_allow_html=True)

# Created Source Table Title
st.markdown("<h1 style='text-align: center; color: white;'>Merged Source Table Used</h1>", unsafe_allow_html=True)
df





