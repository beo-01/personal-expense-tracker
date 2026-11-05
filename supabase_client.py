import streamlit as st
from supabase import create_client, Client


def get_supabase_client() -> Client:

    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]

    supabase = create_client(
        supabase_url,
        supabase_key
    )

    return supabase


def update_password(supabase, new_password):

    response = supabase.auth.update_user({
        "password": new_password
    })

    return response
