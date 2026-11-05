
def sign_up(supabase, email, password):

    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    return response


def sign_in(supabase, email, password):

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    return response


def sign_out(supabase):

    response = supabase.auth.sign_out()

    return response


def reset_password(supabase, email, redirect_url):

    response = supabase.auth.reset_password_for_email(
        email,
        {
            "redirect_to": redirect_url
        }
    )

    return response



def reset_password(supabase, email, redirect_url):

    response = supabase.auth.reset_password_for_email(
        email,
        {
            "redirect_to": redirect_url
        }
    )

    return response

