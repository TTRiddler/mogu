from profiles.forms import RegisterForm, LoginForm


def getting_forms(request):
    reg_form = RegisterForm() 
    login_form = LoginForm()

    context = {
        'reg_form': reg_form,
        'login_form': login_form,
    }
    return context