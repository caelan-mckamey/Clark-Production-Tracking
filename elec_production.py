import pandas as pd

# Prompt the user to upload their CSV file
csv_file_path = input("Please enter the path to your CSV file: ")

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Keep only the specified columns
keep_columns = ['Subject', 'Status', 'Space']
keep_values = df[keep_columns]

# Prompt the user to select subjects
print("Options for subjects: transformers, ATS, panel boards, conduit, switches, ducts")
selected_subject = input("Please enter the subject you want to filter by: ")

# Create a filtering rule to categorize subjects
def categorize_subject(subject):
    if 'TR' in subject:
        return 'Transformer'
    elif 'ATS' in subject:
        return 'ATS'
    elif 'conduit' in subject:
        return 'Conduit'
    elif 'A/' in subject:
        return 'Switch'
    else:
        return 'Panel'

# Apply the filtering rule to create a new 'category' column
keep_values['Category'] = keep_values['Subject'].apply(categorize_subject)

# Filter the DataFrame based on the selected subject
filtered_df = keep_values[keep_values['Subject'].str.contains(selected_subject)]

# Display the filtered DataFrame
print(filtered_df)

# Define the logic to determine the status of each column
def determine_status(row):
    if row['Status'] == 'Not Started':
        return 'Input Date'
    elif row['Status'] == 'Tubs Installed':
        if 'Tubs' in row['Subject']:
            return 'Complete'
        else:
            return 'Input Date'
    elif row['Status'] == 'Conduit Ran':
        return 'Complete' if 'Conduit' in row['Subject'] else 'Input Date'
    elif row['Status'] == 'Wire Pulled':
        return 'Complete' if 'Conduit' in row['Subject'] else 'Input Date'
    elif row['Status'] == 'Panel In':
        if 'Panel' in row['Subject']:
            return 'Complete'
        else:
            return 'Input Date'
    elif row['Status'] == 'Terminated and labelled':
        if 'Panel' in row['Subject']:
            return 'Complete'
        else:
            return 'Input Date'
    elif row['Status'] == 'Tested/Finished':
        return 'Complete'
    else:
        return 'Input Date'

# Create the 'Dashboard' DataFrame
dashboard_columns = ['Equipment Tag', 'Space', 'Deliver', 'Conduit', 'Pull', 'Set (tubs)', 'Set Equipment', 'Terminate (internals)', 'Test', 'Energize']

# Read 'keep_values' DataFrame from CSV file
keep_values = pd.read_csv('keep_values.csv')

# Apply the logic to determine the status of each column
keep_values['Deliver'] = keep_values.apply(lambda row: determine_status(row) if 'Deliver' in dashboard_columns else '', axis=1)
keep_values['Conduit'] = keep_values.apply(lambda row: determine_status(row) if 'Conduit' in dashboard_columns else '', axis=1)
keep_values['Pull'] = keep_values.apply(lambda row: determine_status(row) if 'Pull' in dashboard_columns else '', axis=1)
keep_values['Set (tubs)'] = keep_values.apply(lambda row: determine_status(row) if 'Set (tubs)' in dashboard_columns else '', axis=1)
keep_values['Set Equipment'] = keep_values.apply(lambda row: determine_status(row) if 'Set Equipment' in dashboard_columns else '', axis=1)
keep_values['Terminate (internals)'] = keep_values.apply(lambda row: determine_status(row) if 'Terminate (internals)' in dashboard_columns else '', axis=1)
keep_values['Test'] = keep_values.apply(lambda row: determine_status(row) if 'Test' in dashboard_columns else '', axis=1)
keep_values['Energize'] = keep_values.apply(lambda row: determine_status(row) if 'Energize' in dashboard_columns else '', axis=1)

# Rename the columns to match the 'Dashboard' DataFrame
keep_values.rename(columns={'Subject': 'Equipment Tag', 'Space': 'Space'}, inplace=True)

# Create the 'Dashboard' DataFrame
dashboard = keep_values[dashboard_columns]

# Write the 'Dashboard' DataFrame to an Excel file
dashboard.to_excel('Dashboard.xlsx', index=False)


#The first pie chart represents the percentages of subjects with specific statuses: 'Not Started', 'Tubs Installed', 'Deliver', 'Set (tubs)', 'Set Equipment', 'Terminate (internals)', 'Test', 'Energize'.
#The second pie chart represents the percentages of 'Conduit' and 'Pull' statuses compared to the quantity of subjects labeled 'conduit'.

import pandas as pd
import matplotlib.pyplot as plt

# Read 'keep_values' DataFrame from CSV file
keep_values = pd.read_csv('keep_values.csv')

# Calculate the percentages of subjects with specific statuses
statuses = ['Not Started', 'Tubs Installed', 'Deliver', 'Set (tubs)', 'Set Equipment', 'Terminate (internals)', 'Test', 'Energize']
status_counts = keep_values['Status'].value_counts()
status_counts = status_counts.reindex(statuses, fill_value=0)
total_subjects = len(keep_values)
status_percentages = (status_counts / total_subjects) * 100

# Create the first pie chart
plt.figure(figsize=(10, 6))
plt.pie(status_percentages, labels=status_percentages.index, autopct='%1.1f%%', startangle=140)
plt.title('Percentages of Subjects with Specific Statuses')
plt.axis('equal')
plt.show()

# Calculate the percentage of 'Conduit' and 'Pull' statuses compared to the quantity of subjects labeled 'conduit'
conduit_subjects = keep_values[keep_values['Subject'].str.contains('conduit', case=False)]
conduit_status_counts = conduit_subjects['Status'].value_counts()
conduit_total = len(conduit_subjects)
conduit_status_percentages = (conduit_status_counts / conduit_total) * 100

# Create the second pie chart
plt.figure(figsize=(10, 6))
plt.pie(conduit_status_percentages, labels=conduit_status_percentages.index, autopct='%1.1f%%', startangle=140)
plt.title('Percentages of Conduit and Pull Statuses Compared to Subjects Labeled "Conduit"')
plt.axis('equal')
plt.show()
