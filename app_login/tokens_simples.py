# ativação sem adiconar tabela extras 

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
import datetime

def send_activation_email(user, request):
    # Geração do token de ativação
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode())  # Codificando o ID do usuário

    # Obtendo o domínio atual
    current_site = get_current_site(request)
    domain = current_site.domain

    # Gerando o conteúdo HTML do e-mail
    html_message = render_to_string(
        'activation_email.html',  # Template do e-mail
        {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': token,
            'current_year': datetime.datetime.now().year,  # Incluindo o ano atual no footer
        }
    )

    # Gerando o conteúdo de texto simples
    '''
plain_message = f"""
    Olá {user.first_name},

    Obrigado por se registrar em nosso site! Para ativar sua conta, por favor, clique no link abaixo:

    http://{domain}/activate/{uid}/{token}

    Se você se registrou em nosso site, pode ignorar este e-mail.
"""
'''


    # Enviando o e-mail com partes em HTML e texto simples
    email = EmailMultiAlternatives(
        subject='Ative sua conta',  # Assunto do e-mail
        #body=plain_message,  # Conteúdo em texto simples
        from_email='penha.bahia321@gmail.com',  # Remetente
        to=[user.email],  # Destinatário
    )
    
    # Anexando a versão HTML do e-mail
    email.attach_alternative(html_message, "text/html")

    # Envia o e-mail
    email.send()




from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def activate_conta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Sua conta foi ativada com sucesso!')
            return redirect('login')  # Redireciona para a página de login
        else:
            messages.error(request, 'O link de ativação é inválido ou expirado.')
            return redirect('register')  # Redireciona para o formulário de registro
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Link de ativação inválido.')
        return redirect('register')
