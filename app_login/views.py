from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone 


from django.shortcuts import get_object_or_404
# Create your views here.
from .tokens import activate,send_activation_email
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Cria o usuário, mas com 'is_active' como False

            # Envia o e-mail de ativação
            send_activation_email(user, request)

            # Exibe a mensagem de sucesso
            messages.success(request, 'Conta criada com sucesso! Um e-mail foi enviado para você ativar sua conta.')

            # Retorna a resposta de sucesso
            return HttpResponse('Sucesso, um e-mail foi enviado para você ativar sua conta.')
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os dados e tente novamente.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



def home(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Tenta encontrar o usuário
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Se o usuário não for encontrado, exibe uma mensagem de erro
            messages.error(request, "Nome de usuário não encontrado.")
            return render(request, 'login.html')  # Redireciona de volta para a página de login
    
        # Verifica se o usuário está ativo
        if not user.is_active:

            user.date_joined = timezone.now()
            user.save()
            send_activation_email(user, request)
            return HttpResponse('sua conta esta desativada. um email foi enviado pra voce ativar ')

            #messages.error(request, "Sua conta foi desativada.")
            #return redirect('login_view')  # Redireciona de volta para o login

        # Tenta autenticar o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Se o usuário for autenticado com sucesso
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial após o login
        else:
            # Se a autenticação falhar
            messages.error(request, "Nome de usuário ou senha inválidos.")
            return render('login_view')  # Redireciona de volta para o login

    return render(request, 'login.html')
    




def logout_view(request):
    logout(request)  # Essa função encerra a sessão do usuário
    return redirect('home')  # Redireciona para a página inicial ou qualquer página que você deseje






