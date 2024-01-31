import streamlit as st
import streamlit_antd_components as sac 
import extra_streamlit_components as stx

from authlib.integrations.requests_client import OAuth2Session
from components.auth import get_tokens
from components.platform_signup import beta_email_request
from components.compliancy import compliancy
from components.contact import contact
from components.chat import chat
from components.auth import signin_button

from services.opensearch import check_opensearch_health, create_index, is_index, all_docs

from helpers.antd_utils import show_space
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, auth0_authorization_url, token_url, scope, response_type, domain, userinfo_url
from helpers.markdown import sidebar_links_footer, sidebar_app_header, opensearch_platform_button

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

def set_oauth():
    oauth = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        redirect_uri=auth0_redirect_uri,
        scope=scope,
        response_type=response_type,
    )
    return oauth

oauth = set_oauth()
authorization_url, state = oauth.create_authorization_url(auth0_authorization_url) 

st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 

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

def get_manager():
    return stx.CookieManager()

def stay_signed_in():
    on = st.toggle('Stay Signed In?')
    
    if on:
        st.write('Set on')
        st.write(on)
    # else:
    #     cookie_manager.delete('brockai')

def get_title(title, icon, tag):
    title = sac.menu(
        items=[
            sac.MenuItem(title, icon=icon, tag=tag)
            ],
            key=title,
            open_all=True, indent=20,
            format_func='title'
    )
    return title

def navigation(title, icon, tag, show_sigin_button): 

    access_token = st.session_state.get("access_token")

    if access_token == {}:
        access_token = None

    if not show_sigin_button and access_token == None:
        get_title(title, icon, tag)
    else:
        col1, col2 = st.columns([9, 3])
        with col1:
            get_title(title, icon, tag)
        with col2:
            if show_sigin_button and access_token == None:
                signin_button()
            
            if access_token != None:
                if st.button('Platform Sign out', use_container_width=True):
                    cookie_manager.delete('brockai')
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{domain}\'" />', unsafe_allow_html=True) 

                # stay_signed_in()

authMetadata = get_tokens(authorization_code)
cookie_manager = get_manager()

if authMetadata != None:
    if 'access_token' in authMetadata:
        cookie_manager.set('brockai', authMetadata['access_token'])

        if not is_index():
            create_index()

health, version = check_opensearch_health()

with st.sidebar.container():

    upload = sac.Tag('Upload Files', color='blue', bordered=False)
    modified = sac.Tag('Modified', color='blue', bordered=False)
    protoType = sac.Tag('Prototype', color='green', bordered=False)
    deprecated = sac.Tag('Deprecated', color='orange', bordered=False)
    production = sac.Tag('Production', color='red', bordered=False)
    beta = sac.Tag('Beta', color='purple', bordered=False)
    alpha = sac.Tag('Alpha', color='purple', bordered=False)

    menu = sac.menu(
        items=[
            sac.MenuItem('platform', icon='rocket', tag=alpha),
            sac.MenuItem('regcheck', icon='shield-check', tag=protoType),
            sac.MenuItem('chat', icon='chat-left-text',tag=protoType),
            sac.MenuItem('contact', icon='envelope',)
        ],
        key='menu',
        open_all=True, indent=10,
        format_func='title',
    )
    
    st.markdown(opensearch_platform_button, unsafe_allow_html=True)
    show_space(1)
    sac.divider('OpenSearch Status', color='gray')
    sac.chip(
        items=[
            sac.ChipItem(label=health),
            sac.ChipItem(label=version),
        ], variant='outline', size='xs', radius="md")
    
    sac.divider('Docs & Jupyter Notebooks', color='gray')
    with open('styles.css') as f:
        st.sidebar.markdown(
            f'<style>{f.read()}</style>'
            +sidebar_app_header
            +sidebar_links_footer
            , unsafe_allow_html=True
        ) 

with st.container():        
    if menu == 'regcheck':
        navigation('regcheck', 'shield-check', protoType, False)
        compliancy()
    elif menu == 'chat':
        navigation('chat', 'chat-left-text', protoType, True)
        chat()
    elif menu == 'contact':
        navigation('contact', 'envelope', None, True)
        contact()
    else:
        navigation('platform', 'rocket', alpha, True)
        beta_email_request()

    
