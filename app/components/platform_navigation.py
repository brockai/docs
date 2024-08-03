import requests
import streamlit as st
import streamlit_antd_components as sac

from components.platform_auth import cookie_manager, stay_signed_in, signin_button
from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_cookie_name, domain

def bread_crumbs():
    return sac.segmented(
        items=[
            sac.SegmentedItem(label='Prototypes', icon='rocket', disabled=True),
            sac.SegmentedItem(label='Regcheck', icon='shield-check'),
            sac.SegmentedItem(label='Chat', icon='chat-left-text')
        ], index=st.session_state["bread_crumb_index"], return_index=True, align='left', size='sm', radius='sm', use_container_width=True
    )

def prototype_navigation(): 
        
    bread_crumb_idx = bread_crumbs()
    st.session_state["bread_crumb_index"] = bread_crumb_idx
   
    stay_signed_in(st.session_state.get("access_token"))

    return bread_crumb_idx

def navigation(title, icon, tag, show_signin_button): 

    access_token = st.session_state.get("access_token")

    if access_token == {}:
        access_token = None
    
    if access_token == None:
        if not show_signin_button: 
            get_title(title, icon, tag)
        else:
            get_title(title, icon, tag)
    else:
        title = get_title(title, icon, tag)


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

def get_platform_title(title, icon, tag):
    title = sac.menu(
        items=[
            sac.MenuItem(title, icon=icon, tag=tag)
            ],
            index=None, 
            key=title,
            open_all=True, indent=20,
            format_func='title'
    )
    return title
