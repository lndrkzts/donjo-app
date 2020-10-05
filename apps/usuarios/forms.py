from apps.usuarios.models import User, TipoUsuario

from django import forms


class FormularioRegistro(forms.Form):
    usuario = forms.CharField(required=True, min_length=4, max_length=20)
    nombre = forms.CharField(required=True, min_length=2, max_length=20)
    apellido = forms.CharField(required=True, min_length=2, max_length=20)
    email = forms.EmailField(required=True)
    contrasena = forms.CharField(required=True, min_length=8, widget=forms.PasswordInput(), 
                                 label="Contraseña")
    contrasena2 = forms.CharField(required=True, min_length=8, widget=forms.PasswordInput(),
                                  label="Repetir contraseña")

    usuario.widget.attrs.update({'id': 'usuario', 'class': 'form-control'})
    nombre.widget.attrs.update({'id': 'nombre', 'class': 'form-control'})
    apellido.widget.attrs.update({'id': 'apellido', 'class': 'form-control'})
    email.widget.attrs.update({'id': 'email', 'class': 'form-control'})
    contrasena.widget.attrs.update({'id': 'contrasena', 'class': 'form-control'})
    contrasena2.widget.attrs.update({'id': 'contrasena2', 'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('contrasena2') != cleaned_data.get('contrasena'):
            self.add_error('contrasena2', 'Las contraseñas no coinciden')

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')

        if User.objects.filter(username=usuario):
            raise forms.ValidationError("El nombre de usuario ya se encuentra en uso")
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email):
            raise forms.ValidationError("El email ya se encuentra en uso")
        return email

    def save(self):
        return User.objects.create_user(username=self.cleaned_data.get('usuario'),
                                   first_name = self.cleaned_data.get('nombre'),
                                   last_name = self.cleaned_data.get('apellido'),
                                   email = self.cleaned_data.get('email'),
                                   tipo_usuario = TipoUsuario.CLIENTE.value,
                                   password = self.cleaned_data.get('contrasena'))
