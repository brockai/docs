import streamlit as st
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 

from components.platform_auth import auth_init, cookie_manager, set_tenant_role, signin_button, signout_button
from components.platform_signup import platform_signup
from components.chat import chat
from components.platform_admin import platform_admin
from components.bomai import bomai

from services.shared_service import check_opensearch_health, is_index
from services.tenant_service import get_tenant_doc

from helpers.config import auth0_cookie_name, platform_admin_tenant
from helpers.markdown import opensearch_platform_button
from streamlit_extras.tags import tagger_component

params = st.query_params.to_dict()

authorization_code = None
authorization_state = None

if len(params) > 0: 
    authorization_code = params["code"]
    authorization_state = params["state"]

    # initlalize Auth0 client
    tenant_id = auth_init(authorization_code)
    st.session_state['tenant_id'] = tenant_id

    admin_disabled = False

    if is_index(st.session_state['tenant_id'], st.session_state['tenant_id']):
        
        if 'tenant_doc' not in st.session_state:
            tenant_doc = get_tenant_doc(platform_admin_tenant) 

            if len(tenant_doc['hits']['hits']) == 0:
                st.session_state['tenant_doc'] = tenant_doc['hits']['hits'][0]['_source']['mappings']['properties']
                set_tenant_role()

st.markdown(f'''
    <style>
    .stApp .main .block-container{{
        padding:30px 50px
    }}
    .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2){{
        padding-top:50px
    }}
    iframe{{
        display:block;
    }}
    .stRadio div[role='radiogroup']>label{{
        margin-right:5px
    }}
    </style>
    ''', unsafe_allow_html=True)

cookie = cookie_manager.get(auth0_cookie_name)
if cookie:
    cookie_values = cookie.split('|')
    st.session_state['tenant_id'] = cookie_values[0] 

health, version = check_opensearch_health()

col1, col2 = st.columns([9, 3], gap="medium")

with col1:
    with open('styles.css') as f:
        st.markdown(
            f'<style>{f.read()}</style>'
            +"""<img src="app/static/brockailogo.png" height="65" alt="Platform">"""
            , unsafe_allow_html=True
        ) 
with col2:
    if 'tenant_id' not in st.session_state:
        signin_button()
    else:
        signout_button()

pageCol = st.columns([12])

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📱 Apps", "🚀 BOM Check AI", "💬 Chat", "👥 Contact", "☁️ Platform"])

with tab1:
    col1, col2 = st.columns([8, 4], gap="large")

    with col1:

        cola, colb = st.columns([6, 6], gap="large")

        with cola:
            st.markdown('''
                <div style="display: inline-flex; align-items: center;">
                <img src="app/static/brockai.png" height="55" alt="Platform" style="margin-right: 10px;">
                <span style="color: red; font-size: 24px;">Mobile Fuel Delivery</span>
                </div>
                <p>Full featured mobile bulk fuel delivery with geotab integration</p>
                ''', unsafe_allow_html=True)
            st.link_button("Mobile Fuel Delivery - Learn More", "https://github.com/brockai#apps")

            st.markdown('''
                <span style="font-size: 24px; color: white;">🏆 Sponsor</span>
                <div><a href="https://bmel.ca/" target="_blank">
                    <img src="app/static/bmellogo.jpg" alt="Birch Mountain Enterprisesr" height="75">
                </a></div>
                ''', unsafe_allow_html=True)
            
        with colb:  
            st.markdown('''
                <div style="display: inline-flex; align-items: center;">
                <img src="app/static/brockai.png" height="55" alt="Platform" style="margin-right: 10px;">
                <span style="color: red; font-size: 24px;">BOM Check AI</span>
                </div>
                <p>AI and machine learning to assist in checking Bill of Materials (BOM) for regulatory compliance</p>
                ''', unsafe_allow_html=True)
            st.link_button("BOM Check AI - Learn More", "https://github.com/brockai/bomai")
        
            st.markdown('''
                <span style="font-size: 24px; color: white;">🏆 Sponsor</span>
                <div><a href="https://rumzer.com" target="_blank">
                    <img src="app/static/rumzerlogo.png" alt="Rumzer" height="55">
                </a></div>
                ''', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<h5>Our Stack</h5>', unsafe_allow_html=True)
        st.markdown('''
            - **Frontend:** React/NextJS/TailwindCSS/Streamlit
            - **Server:** NodeJS
            - **Database:** OpenSearch
            - **Integration:** Geotab
            - **Security & Authentication:** Auth0
            ''', unsafe_allow_html=True)

        st.link_button("Future-proof your app with AI from OpenSearch - Learn More", "https://opensearch.org/platform/search/vector-database.html")

        st.link_button("Visit our Wiki - Learn More", "https://github.com/brockai/brockai/wiki")

with tab2:
    bomai()

with tab3:
    chat()

with tab4:
    st.subheader('Contact')
    platform_signup()

with tab5:
    col1, col2 = st.columns([10, 2], gap="medium")
    with col1:
        tagger_component('OpenSearch', [health, version])
    with col2:
        st.markdown(opensearch_platform_button, unsafe_allow_html=True)

    if 'tenant_id' in st.session_state:
        platform_admin()
    
    if 'tenant_id' not in st.session_state:
        st.text('Please Sign In')




 