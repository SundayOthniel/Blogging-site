from .models import BloggerSignup, BloggerContent
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class BloggerSignupView(CreateView):
    template_name = "blogger_signup.html"
    model = BloggerSignup

    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        phone = request.POST.get('tel')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpass = request.POST.get('cpass')

        blogger_exist = self.model.blogger.user(uname)
        email_exist = self.model.blogger.email(email)
        phone_exist = self.model.blogger.phone(phone)
        if password == cpass:
            if blogger_exist:
                messages.error(request, f"This username {uname} already exist")
                return redirect('blogger_signup')
            elif email_exist:
                messages.error(request, f"This email {email} already exist")
                return redirect('blogger_signup')
            elif phone_exist:
                messages.error(request, f"This mobile number {phone} already exist")
                return redirect('blogger_signup')
            elif fname is None or lname is None or uname is None or email is None or address is None or dob is None or phone is phone is None or gender is None or password is None or cpass is None:
                messages.error(request, f"Fill the form")
                return redirect('blogger_signup')
            else:      
                blogger = self.model.objects.create(first_name=fname.capitalize(), 
                                                    middle_name=mname.capitalize(), 
                                                    last_name=lname.capitalize(), 
                                                    username=uname.capitalize(), 
                                                    dob=dob, 
                                                    email=email.capitalize(), 
                                                    phone=phone, 
                                                    gender=gender, 
                                                    address=address.capitalize(), 
                                                    password=password)
                blogger.is_superuser = True
                blogger.is_staff = True
                blogger.set_password(password)
                blogger.save()
                return redirect("blogger_signin")
        else:
            messages.error(request, 'Password Mismatch')

class BloggerLogin(LoginView):
    template_name = "blogger_login.html"
    def post(self, request):
        next_page = redirect("blogger_dashboard")

        uname = request.POST.get('uname').capitalize()
        password = request.POST.get('password')
        
        blogger = authenticate(username=uname, password=password)

        if blogger is not None:
            login(request, blogger)
            messages.success(request, "You have sucessfully login")
            return next_page
        else:
            messages.error(request, "Incorrect Username or Password")
            return redirect("blogger_signin")
        

class PasswordReset(View):
    """
    A class that handles the password reset functionality for a user.

    Methods:
        get(self, request): Renders the password reset form.
        post(self, request): Handles the form submission when a user requests a password reset.
    """

    def get(self, request):
        """
        Renders the password reset form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered password reset form.
        """
        return render(request, 'password_reset_form.html')

    def post(self, request):
        """
        Handles the form submission when a user requests a password reset.

        Args:
            request (HttpRequest): The HTTP request object containing the form data.

        Returns:
            HttpResponseRedirect: If the email exists, the user is redirected to the "link_sent" page.
            None: If the email does not exist, an error message is displayed and the user is redirected back to the password reset form.
        """
        email = request.POST.get('email').capitalize()
        blogger_exist = BloggerSignup.blogger.email(email)
        blogger = BloggerSignup.blogger.filter(email=email).first()

        if blogger_exist:
            token = default_token_generator.make_token(blogger)

            subject = 'Password Reset Request'
            context = {
                'username' : blogger.username,
                'email': email,
                'domain': '127.0.0.1:8000',
                'site_name': 'OthnielKid',
                'uid' : urlsafe_base64_encode(force_bytes(blogger.pk)),
                'token' : token,
                'protocol' : 'http'
            }

            email_content = render_to_string('message.html', context)
            msg = EmailMultiAlternatives(subject, email_content, 'djangopractice22@gmail.com', [email])
            msg.attach_alternative(email_content, "text/html")
            msg.send()
            return redirect('link_sent')        
        else:
            messages.error(request, f"This email {email} does not exist. Use your registered email")
            return redirect("password_reset")
        # except Exception as e:
        #             error_message = f'An error occurred: {str(e)}'  # Provide a more informative message
        #             if request.META.get('HTTP_ACCEPT', '').startswith('text/html'):  # Check if the client accepts HTML
        #                 context = {'error_message': error_message}
        #                 return render(request, 'error.html', context)
        #             else:
                        # return HttpResponse(f'Error: {error_message}')
        
class LinkSent(TemplateView):
    def get(self, request):
        return render(request, 'linksent.html')
    
class BloggerDashboard(TemplateView):
    template_name = 'blogger_dashboard.html'

class BloggerProfile(TemplateView):
    template_name = 'blogger_profile.html'


class BloggerEditProfile(View):
    
    def get(self, request):
        return render(request, 'blogger_edit_profile.html')
    def post(self, request):
        if request.method == 'POST':
            if request.user.is_authenticated:
                user = request.user    
                user.username = request.POST.get('uname')
                user.first_name = user.first_name
                user.middle_name = request.POST.get('mname')
                user.last_name = user.last_name
                user.email = request.POST.get('email')
                user.dob = request.POST.get('dob')
                user.gender = request.POST.get('gender')
                user.address = request.POST.get('address')
                messages.success(request, "Your data is successfully updated")
                user.save()
            else:
                messages.error(request, "username already taken")
            return redirect('blogger_profile')

class CreateContent(View):
    def get(self, request):
        return render(request, 'create_content.html')

    def post(self, request):
        content = request.POST.get('content')
        BloggerContent.objects.create(content=content)
        return render(request, 'create_content.html')
    