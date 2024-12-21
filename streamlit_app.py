import streamlit as st
import requests
from datetime import datetime
import re
import time

# Page Configuration
st.set_page_config(
    page_title="EventFlow",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
BASE_URL = 'http://127.0.0.1:5000'

# Enhanced Modern CSS
st.markdown("""
    <style>
        /* Modern Color Scheme */
        :root {
            --primary-color: #6366F1;
            --secondary-color: #4F46E5;
            --accent-color: #EC4899;
            --background-color: #F9FAFB;
            --card-background: #FFFFFF;
            --text-color: #111827;
            --border-color: #E5E7EB;
        }
        
        /* Global Styles */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color);
            font-family: 'Inter', system-ui, sans-serif;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        
        /* Card Styling */
        .modern-card {
            background-color: var(--card-background);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s;
            color: var(--text-color);
        }
        
        .modern-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Button Styling */
        .stButton>button {
            border-radius: 0.5rem;
            padding: 0.625rem 1.25rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            font-weight: 500;
            letter-spacing: 0.025em;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.15);
        }
        
        /* Sidebar Styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-color);
        }
        
        /* Updated Form Input Styling */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea {
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            padding: 0.75rem 1rem;
            font-size: 0.975rem;
            transition: border-color 0.2s, box-shadow 0.2s;
            background-color: white !important;
            color: var(--text-color) !important;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        /* Password Input Styling */
        [type="password"] {
            background-color: white !important;
            color: var(--text-color) !important;
        }
        
        .stPassword > div > div > div[data-lastpass-icon-root] {
            color: var(--text-color);
        }
        
        /* Placeholder Styling */
        .stTextInput>div>div>input::placeholder,
        .stTextArea>div>div>textarea::placeholder {
            color: #6B7280;
            opacity: 0.8;
        }
        
        /* Message Styling */
        .success-message {
            background-color: #ECFDF5;
            color: #065F46;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #059669;
            margin: 1rem 0;
            animation: slideIn 0.3s ease-out;
        }
        
        .error-message {
            background-color: #FEF2F2;
            color: #991B1B;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #DC2626;
            margin: 1rem 0;
            animation: slideIn 0.3s ease-out;
        }
        
        /* Event Card Styling */
        .event-card {
            background: white;
            border-radius: 1rem;
            padding: 1.75rem;
            margin: 1.25rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s;
            color: var(--text-color);
        }
        
        .event-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .event-title {
            color: var(--primary-color);
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }
        
        /* Badge Styling */
        .badge {
            background-color: #EEF2FF;
            color: var(--primary-color);
            padding: 0.375rem 0.875rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
        }
        
        /* Metric Card Styling */
        .metric-card {
            background: white;
            border-radius: 0.75rem;
            padding: 1.25rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-color);
            transition: transform 0.2s;
            color: var(--text-color);
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
        }
        
        .metric-value {
            font-size: 1.75rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            color: #6B7280;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        /* Navigation Styling */
        .nav-link {
            padding: 0.875rem 1.25rem;
            border-radius: 0.5rem;
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 0.5rem 0;
            transition: background-color 0.2s;
            font-weight: 1500;
        }
        
        .nav-link:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Animation */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: var(--card-background);
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            padding: 0.75rem 1rem;
            transition: background-color 0.2s;
            color: var(--text-color);
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #F9FAFB;
        }
        
        /* Date Input Styling */
        .stDateInput>div>div>input {
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            padding: 0.625rem 1rem;
            background-color: white !important;
            color: var(--text-color) !important;
        }
        
        /* Select Box Styling */
        .stSelectbox>div>div>div {
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            background-color: white !important;
            color: var(--text-color) !important;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background-color: transparent;
            border-bottom: 2px solid var(--border-color);
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 1.5rem;
            color: var(--text-color);
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            color: var(--primary-color);
            border-bottom: 2px solid var(--primary-color);
        }
        
        /* Additional Input Container Styling */
        .stTextInput>div, .stTextArea>div, .stDateInput>div {
            background-color: transparent !important;
        }
        
        /* Ensure all form controls have white backgrounds */
        .stTextInput>div>div, .stTextArea>div>div, .stDateInput>div>div,
        .stSelectbox>div, .stMultiSelect>div {
            background-color: white !important;
        }
        
        /* Ensure all text elements use the text color variable */
        .stMarkdown, 
        .stText, 
        .stTextInput label,
        .stSelectbox label,
        .stMultiSelect label,
        .stDateInput label,
        .stMarkdown p,
        .stMarkdown span {
            color: var(--text-color) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Utility Functions
def show_notification(message, type="info"):
    """Display styled notifications"""
    if type == "success":
        st.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)
    elif type == "error":
        st.markdown(f'<div class="error-message">{message}</div>', unsafe_allow_html=True)
    else:
        st.info(message)

def validate_email(email):
    """Validate email format"""
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

def handle_api_error(response):
    """Handle API errors consistently"""
    error_message = response.json().get("message", "An error occurred") if response.content else "An unexpected error occurred"
    show_notification(error_message, "error")
    if response.status_code == 404:
        st.session_state.page = "Dashboard"
        st.rerun()
		
def landing_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🎉 EventFlow")
        st.markdown("### Streamline your event planning journey")
        st.markdown("---")
        
        col_reg, col_login = st.columns(2)
        with col_reg:
            if st.button("🚀 Register"): st.session_state.page = "Register"
        with col_login:
            if st.button("🔑 Login"): st.session_state.page = "Login"

def register_user():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🎯 Create Account")
        with st.form("register_form", clear_on_submit=True):
            username = st.text_input("👤 Username")
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            
            if st.form_submit_button("Register"):
                if not all([username, email, password, confirm_password]):
                    show_notification("Please fill in all fields", "error")
                    return
                
                if not validate_email(email):
                    show_notification("Please enter a valid email address", "error")
                    return
                
                if password != confirm_password:
                    show_notification("Passwords do not match", "error")
                    return
                
                try:
                    response = requests.post(
                        f"{BASE_URL}/register",
                        json={"username": username, "email": email, "password": password}
                    )
                    if response.status_code == 201:
                        show_notification("Registration successful! Please log in.", "success")
                        st.session_state.page = "Login"
                    else:
                        handle_api_error(response)
                except requests.exceptions.RequestException:
                    show_notification("Could not connect to the server.", "error")

        if st.button("← Back"): st.session_state.page = "Landing"

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔑 Login")
        with st.form("login_form", clear_on_submit=True):
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")
            
            # Move the submit button inside the form block
            if st.form_submit_button("Login"):
                if not all([email, password]):
                    show_notification("Please fill in all fields", "error")
                    return

                try:
                    response = requests.post(
                        f"{BASE_URL}/login",
                        json={"email": email, "password": password}
                    )
                    if response.status_code == 200:
                        # Store necessary information in session state
                        st.session_state.user_id = response.json()["user_id"]
                        st.session_state.email = email  
                        st.session_state.page = "Dashboard"
                        st.rerun()
                    else:
                        handle_api_error(response)
                        
                except requests.exceptions.RequestException:
                    show_notification("Could not connect to the server.", "error")

    # Move the "Back" button below the form
    if st.button("← Back"): st.session_state.page = "Landing"

def create_or_edit_event(event_data=None): 
    is_edit = event_data is not None
    st.title("✏ Edit Event" if is_edit else "🎨 Create New Event")

    # Initialize default times
    default_start = datetime.now().replace(hour=8, minute=0)
    default_end = datetime.now().replace(hour=17, minute=0)

    # Parse existing event times if editing
    if is_edit:
        try:
            start_datetime = datetime.fromisoformat(event_data.get('start_time'))
            end_datetime = datetime.fromisoformat(event_data.get('end_time'))
        except (ValueError, TypeError):
            start_datetime = default_start
            end_datetime = default_end
    else:
        start_datetime = default_start
        end_datetime = default_end

    with st.form("event_form"):
        title = st.text_input("📌 Event Title", value=event_data.get('title', '') if is_edit else '', key="event_title")
        description = st.text_area("📝 Description", value=event_data.get('description', '') if is_edit else '', key="event_description")
        location = st.text_input("📍 Location", value=event_data.get('location', '') if is_edit else '', key="event_location")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("📅 Start Date", value=start_datetime.date(), key="start_date")
            start_time = st.time_input("⏰ Start Time", value=start_datetime.time(), key="start_time")
        with col2:
            end_date = st.date_input("📅 End Date", value=end_datetime.date(), key="end_date")
            end_time = st.time_input("⏰ End Time", value=end_datetime.time(), key="end_time")

        attendees = st.text_area("👥 Attendees (one email per line)", value='\n'.join(event_data.get('attendees', [])) if is_edit else '', key="attendees")

        # Vendor information
        col3, col4 = st.columns(2)
        with col3:
            vendor_names = st.text_area("🏪 Vendor Names", value='\n'.join([v['name'] for v in event_data.get('vendors', [])]) if is_edit else '', key="vendor_names")
        with col4:
            vendor_services = st.text_area("🛠 Services Provided", 
                                           value='\n'.join([v.get('service', 'Unknown') for v in event_data.get('vendors', [])]) 
                                           if is_edit else '', key="vendor_services")
        
        # Sponsor information
        col5, col6, col7 = st.columns(3)
        with col5:
            sponsor_names = st.text_area("💎 Sponsor Names", value='\n'.join([s['name'] for s in event_data.get('sponsors', [])]) if is_edit else '', key="sponsor_names")
        with col6:
            sponsor_levels = st.text_area("🏅 Sponsorship Levels", value='\n'.join([s['level'] for s in event_data.get('sponsors', [])]) if is_edit else '', key="sponsor_levels")
        with col7:
            sponsor_contributions = st.text_area("💰 Contributions ($)", value='\n'.join([str(s['contribution']) for s in event_data.get('sponsors', [])]) if is_edit else '', key="sponsor_contributions")

        # Modified Event Items section with two columns
        st.subheader("📋 Event Items")
        item_col1, item_col2 = st.columns(2)
        with item_col1:
            st.markdown("##### Item Names")
            item_names = st.text_area(
                "Item Name(s) (one per line)", 
                value='\n'.join([i['item_name'] for i in event_data.get('items', [])]) if is_edit else '', 
                key="item_names",
                height=150  # Set a fixed height for better alignment
            )
        with item_col2:
            st.markdown("##### Quantities")
            item_quantities = st.text_area(
                "Quantity (one per line)", 
                value='\n'.join([str(i['quantity']) for i in event_data.get('items', [])]) if is_edit else '', 
                key="item_quantities",
                height=150  # Match the height with item names
            )

        submitted = st.form_submit_button("💾 Save Event")

        if submitted:
            if not all([title, location, start_date, end_date, attendees]):
                show_notification("Please fill in all required fields", "error")
                return

            try:
                # Combine date and time
                start_datetime = datetime.combine(start_date, start_time)
                end_datetime = datetime.combine(end_date, end_time)

                if start_datetime >= end_datetime:
                    show_notification("End time must be after start time", "error")
                    return

                # Process sponsors ensuring valid numeric contributions
                sponsors = []
                sponsor_names_list = [n.strip() for n in sponsor_names.split('\n') if n.strip()]
                sponsor_levels_list = [l.strip() for l in sponsor_levels.split('\n') if l.strip()]
                sponsor_contributions_list = [c.strip() for c in sponsor_contributions.split('\n') if c.strip()]

                for n, l, c in zip(sponsor_names_list, sponsor_levels_list, sponsor_contributions_list):
                    try:
                        contribution = float(c.replace('$', '').replace(',', ''))
                        sponsors.append({"name": n, "level": l, "contribution": contribution})
                    except ValueError:
                        show_notification(f"Invalid contribution amount for sponsor {n}", "error")
                        return

                # Process event items ensuring valid numeric quantities
                event_items = []
                item_names_list = [n.strip() for n in item_names.split('\n') if n.strip()]
                item_quantities_list = [q.strip() for q in item_quantities.split('\n') if q.strip()]

                for name, quantity in zip(item_names_list, item_quantities_list):
                    try:
                        quantity_int = int(quantity)
                        event_items.append({"item_name": name, "quantity": quantity_int})
                    except ValueError:
                        show_notification(f"Invalid quantity for item: {name}", "error")
                        return

                # Construct event payload
                event_payload = {
                    "title": title,
                    "description": description,
                    "location": location,
                    "start_time": start_datetime.isoformat(),
                    "end_time": end_datetime.isoformat(),
                    "user_id": st.session_state.user_id,
                    "attendees": [email.strip() for email in attendees.split('\n') if email.strip()],
                    "vendors": [
                        {"name": n.strip(), "service": s.strip()}
                        for n, s in zip(vendor_names.split('\n'), vendor_services.split('\n'))
                        if n.strip() and s.strip()
                    ],
                    "sponsors": sponsors,
                    "items": event_items
                }

                # Send the request to the server
                if is_edit:
                    response = requests.put(f"{BASE_URL}/events/{event_data['id']}", json=event_payload)
                else:
                    response = requests.post(f"{BASE_URL}/events", json=event_payload)

                if response.status_code in [200, 201]:
                    show_notification(
                        f"Event {'updated' if is_edit else 'created'} successfully!",
                        "success"
                    )
                    st.session_state.show_create_event = False
                    st.session_state.editing_event = None
                    st.session_state.page = "Dashboard"  # Redirect to dashboard after creation
                    st.rerun()
                else:
                    handle_api_error(response)

            except requests.exceptions.RequestException:
                show_notification("Could not connect to the server.", "error")
            except ValueError as e:
                show_notification(f"Invalid data format: {str(e)}", "error")

    if st.button("← Back to Dashboard"):
        st.session_state.show_create_event = False
        st.session_state.editing_event = None
        st.rerun()
                
def show_event_details(event, is_attending_only=False, parent_key=None):
    """Display event details with collapsible sections"""
    # Initialize delete confirmation state for this event if not exists
    delete_key = f"delete_confirm_{event['id']}"
    if delete_key not in st.session_state:
        st.session_state[delete_key] = False
    
    st.markdown(f"### 📅 {event['title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"📍 *Location:* {event['location']}")
        st.write(f"⌛ *Time:* {event['start_time']} - {event['end_time']}")
    with col2:
        st.write(f"📝 *Description:* {event['description']}")
    
    # Display participants in an expander
    if event.get('attendees'):
        with st.expander("👥 Attendees"):
            st.write(", ".join(event['attendees']))
    
    # Display vendors in an expander
    if event.get('vendors'):
        with st.expander("🏪 Vendors"):
            for v in event['vendors']:
                service = v.get('service', 'Unknown')
                st.write(f"• {v['name']} - {service}")
    
    # Display sponsors in an expander
    if event.get('sponsors'):
        with st.expander("💎 Sponsors"):
            for s in event['sponsors']:
                st.write(f"• {s['name']} ({s['level']}) - ${float(s['contribution']):,.2f}")
    
    # Display event items in an expander
    if event.get('items'):
        with st.expander("📋 Event Items"):
            for item in event['items']:
                st.write(f"• {item['item_name']} - Quantity: {item['quantity']}")    
    
    # Only show action buttons if the user is the event creator
    if not is_attending_only:
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏ Edit", key=f"edit_event_{event['id']}_{parent_key}"):
                st.session_state.editing_event = event
                st.session_state.show_create_event = True
                st.rerun()
        
        with col2:
            # Delete button and confirmation
            if not st.session_state[delete_key]:
                if st.button("🗑 Delete", key=f"delete_event_{event['id']}_{parent_key}"):
                    st.session_state[delete_key] = True
                    st.rerun()
            else:
                st.error("Are you sure you want to delete this event?")
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("✔ Yes", key=f"confirm_delete_event_{event['id']}_{parent_key}"):
                        try:
                            response = requests.delete(f"{BASE_URL}/events/{event['id']}")
                            if response.status_code == 200:
                                st.session_state[delete_key] = False
                                st.success("Event deleted successfully!")
                                st.rerun()
                            else:
                                handle_api_error(response)
                        except requests.exceptions.RequestException:
                            st.session_state[delete_key] = False
                            show_notification("Could not connect to the server.", "error")
                with col4:
                    if st.button("❌ No", key=f"cancel_delete_event_{event['id']}_{parent_key}"):
                        st.session_state[delete_key] = False
                        st.rerun()
            
            if not is_attending_only:
                st.markdown(" ")
               # show_event_analytics(event['id'], parent_key=f"event_{event['id']}")

# def show_event_analytics(event_id, parent_key=None):
#     try:
#         # Fetch analytics data
#         response = requests.get(f"{BASE_URL}/events/{event_id}/analytics")
#         if response.status_code == 200:
#             data = response.json()
#             summary = data['summary']
#             analytics = data['analytics']

#             st.subheader("📊 Event Analytics")
            
#             # Create three columns for key metrics
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 total_attendees = analytics['total_attendees']
#                 if isinstance(total_attendees, str):
#                     try:
#                         total_attendees = int(total_attendees)
#                     except ValueError:
#                         total_attendees = 0
#                         st.error("Error converting Total Attendees to an integer.")
#                 st.metric("Total Attendees", total_attendees)
#                 st.metric("Total Sponsors", analytics['total_sponsors'])
            
#             with col2:
#                 total_sponsorship = analytics['total_sponsorship']
#                 if isinstance(total_sponsorship, str):
#                     try:
#                         total_sponsorship = float(total_sponsorship)
#                     except ValueError:
#                         total_sponsorship = 0.0
#                         st.error("Error converting Total Sponsorship to a numeric value.")
#                 st.metric("Total Sponsorship", f"${total_sponsorship:,.2f}")
#                 total_costs = analytics['total_costs']
#                 if isinstance(total_costs, str):
#                     try:
#                         total_costs = float(total_costs)
#                     except ValueError:
#                         total_costs = 0.0
#                         st.error("Error converting Total Costs to a numeric value.")
#                 st.metric("Total Costs", f"${total_costs:,.2f}")
            
#             with col3:
#                 projected_profit = analytics['projected_profit']
#                 if isinstance(projected_profit, str):
#                     try:
#                         projected_profit = float(projected_profit)
#                     except ValueError:
#                         projected_profit = 0.0
#                         st.error("Error converting Projected Profit to a numeric value.")
#                 st.metric("Projected Profit", f"${projected_profit:,.2f}")
#                 profit_color = "green" if projected_profit > 0 else "red"
#                 st.markdown(f"<p style='color:{profit_color}'>{'Profitable' if projected_profit > 0 else 'Loss'}</p>", 
#                             unsafe_allow_html=True)

#             # Show popularity metrics
#             st.subheader("📈 Event Popularity")
#             if 'popularity_rank' in summary:
#                 st.write(f"Popularity Rank: #{summary['popularity_rank']}")

#     except requests.exceptions.RequestException:
#         st.error("Could not fetch analytics data. Please try again later.")

def dashboard():
    # Redirect to login if user_id is not in session state
    if 'user_id' not in st.session_state:
        st.session_state.page = "Login"
        st.rerun()

    # Dashboard Title
    st.title("🎉 Event Dashboard")

    # Sidebar Navigation
    with st.sidebar:
        st.title("Navigation")
        if st.button("📅 Create New Event"):
            st.session_state.editing_event = None
            st.session_state.show_create_event = True
        if st.button("🏠 Dashboard Home"):
            st.session_state.show_create_event = False
            st.session_state.editing_event = None
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    if st.session_state.get('show_create_event', False):
        create_or_edit_event(st.session_state.get('editing_event'))
    else:
        try:
            # Fetch events created by the user
            response = requests.get(f"{BASE_URL}/events/user/{st.session_state.user_id}")
            if response.status_code == 200:
                created_events = response.json().get("events", [])

                # Fetch events the user is attending
                attendee_response = requests.get(f"{BASE_URL}/events/attendee/{st.session_state.email}")
                if attendee_response.status_code == 200:
                    attending_events = attendee_response.json().get("events", [])

                    # Combine events, prioritizing created events
                    all_events = created_events + [e for e in attending_events if e not in created_events]

                    if all_events:
                        st.write("### Your Events:")
                        for event in all_events:
                            # Check if 'user_id' exists in the event
                            if 'user_id' in event:
                                show_event_details(event, 
                                                   is_attending_only=event['user_id']!= st.session_state.user_id, 
                                                   parent_key=f"dashboard_event_{event['id']}")
                            else:
                                st.warning(f"Event {event['id']} is missing 'user_id' information.")
                            st.divider()
                    else:
                        st.info("No events found. Create your first event!")
                else:
                    handle_api_error(attendee_response)
            else:
                handle_api_error(response)
        except requests.exceptions.RequestException:
            show_notification("Could not connect to the server.", "error")

# Main routing
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Landing"

    pages = {
        "Landing": landing_page,
        "Register": register_user,
        "Login": login,
        "Dashboard": dashboard
    }

    pages[st.session_state.page]()

if __name__ == "__main__":
    main()