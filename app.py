
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# App title and logo
st.image("KID-22300_KGS-Logo_Full Color.png", width=300)
st.title("KGS Marketing Efforts Estimator")

# Dropdown options
departments = ['Sales', 'Customer Service', 'HR', 'Finance', 'IT', 'Operations', 'Legal']
countries = ['BE', 'NL', 'UK', 'IE', 'FR', 'IT', 'ES', 'PT', 'DE', 'DK', 'SE', 'FI', 'NO', 'PL', 'TR', 'ZA', 'ME', 'OUT-OF-EMEA']
services = ['Poster Design', 'Brochure Design', 'Catalogue Design', 'Leaflet Design', 'Presentation Design', 'Whitepaper Creation', 'Infographic Design', 'Office Wall Design', 'Website Banner Design', 'Social Media Graphics', 'Translation (<5 pages)', 'Translation (5–10 pages)', 'Translation (10–20 pages)', 'Translation (20–50 pages)', 'Translation (>50 pages)', 'Website Event Registration Webpage', 'Event Registration Handling', 'Webpage Link for Campaign', 'Video Production (<1 minute)', 'Video Production (>1 minute)', 'Cost of One Lead Generated', 'Specific PR Need', 'Market Research Report', 'Brand Guidelines Creation', 'VR Experience (1-day)', 'Event Support (on-site branding)', 'Event Support (digital assets)', 'Webinar Setup & Promotion', 'Trade Show Booth Design', 'Business Card Design' , 'Product camera photo + editing' , 'Event Backdrop (One)' , 'Emailing Campaign' ]

# Pricing model
pricing = {'Poster Design': 150, 'Brochure Design': 400, 'Catalogue Design': 800, 'Leaflet Design': 100, 'Presentation Design': 300, 'Whitepaper Creation': 500, 'Infographic Design': 250, 'Office Wall Design': 1200, 'Website Banner Design': 250, 'Social Media Graphics': 200, 'Translation (<5 pages)': 100, 'Translation (5–10 pages)': 180, 'Translation (10–20 pages)': 350, 'Translation (20–50 pages)': 800, 'Translation (>50 pages)': 1500, 'Website Event Registration Webpage': 600, 'Event Registration Handling': 400, 'Webpage Link for Campaign': 300, 'Video Production (<1 minute)': 800, 'Video Production (>1 minute)': 1500, 'Cost of One Lead Generated': 50, 'Specific PR Need': 1000, 'Market Research Report': 2000, 'Brand Guidelines Creation': 1500, 'VR Experience (1-day)': 2000, 'Event Support (on-site branding)': 1200, 'Event Support (digital assets)': 800, 'Webinar Setup & Promotion': 1000, 'Trade Show Booth Design': 2500,'Business Card Design': 160, 'Product camera photo + editing': 55 , 'Event Backdrop (One)': 280 , 'Emailing Campaign': 480 }

# Initialize session state
if 'services_list' not in st.session_state:
    st.session_state.services_list = []

# Form to add a service
with st.form("add_service_form"):
    department = st.selectbox("Select Department", departments)
    country = st.selectbox("Select Country", countries)
    service = st.selectbox("Select Service", services)
    quantity = st.number_input("Quantity", min_value=1, value=1)
    add_btn = st.form_submit_button("Add Another Service")
    if add_btn:
        st.session_state.services_list.append({"Department": department, "Country": country, "Service": service, "Quantity": quantity})

# Display added services
if st.session_state.services_list:
    st.write("### Added Services")
    st.table(pd.DataFrame(st.session_state.services_list))

# Estimate button
if st.button("Estimate"):
    df = pd.DataFrame(st.session_state.services_list)
    df['Unit Price (€)'] = df['Service'].map(pricing)
    df['Total (€)'] = df['Quantity'] * df['Unit Price (€)']
    total_savings = df['Total (€)'].sum()

    st.subheader(f"Total Estimated Savings: €{total_savings:,.2f}")

    # Professional closing message
    st.markdown("""
    **This amount represents the money saved by leveraging internal marketing resources instead of external agencies.**  
    Remember: *Saved money is earned money.*
    """)

    # Bar chart
    fig = px.bar(df, x='Service', y='Total (€)', color='Service', title='Breakdown of Services')
    st.plotly_chart(fig)

    # Excel download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Estimate')
    st.download_button(label="Download Excel", data=output.getvalue(), file_name="estimate.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
