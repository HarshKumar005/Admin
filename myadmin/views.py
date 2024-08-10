import datetime
from http import client
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from requests import request
from .forms import ClientForm,ServiceProviderForm,  ServicesForm,  UserLogin
from .models import Services, Client ,Company # Import the Client model
from .forms import ClientForm, ServicesForm, ServiceProviderForm
from django.shortcuts import get_object_or_404, render
 
######################### LOGIN PANEL #############################################################################################################################################################################################################################

def loginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserLogin(request=request, data=request.POST)
            
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']  # Corrected 'passwaord' to 'password'
                userOBJ = authenticate(username=uname, password=upass)
                
                if userOBJ is not None:
                    login(request, userOBJ)
                    return HttpResponseRedirect('/dashboard/')  # Use HttpResponseRedirect to redirect

        else:
            fm = UserLogin()
        return render(request, 'login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dashboard/')  # Use HttpResponseRedirect to redirect

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')  # Redirect to the login page

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return HttpResponseRedirect('/')  # Redirect to the login page
    
    
####################################  ADD INVOCIE  #########################################################################################################################################################################################    

def add_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            clientFm = ClientForm(request.POST)
            if clientFm.is_valid():
                comp = clientFm.cleaned_data['company_name']
                gst = clientFm.cleaned_data['gst_number']
                cntry = clientFm.cleaned_data['country']
                sts = clientFm.cleaned_data['state']
                add = clientFm.cleaned_data['address']
          
                obj = Client(company_name=comp, gst_number=gst, country=cntry, state=sts, address=add)
                obj.save()
                 # Generate the report data for the added client
              
                
                messages.success(
                    request, "Your 'Client' form has been saved successfully"
                )
            return redirect('add-invoice')

        else:
            clientFm = ClientForm()  
        return render(request, 'add_invoice.html', {'clientFm': clientFm ,})
    
    
###################################### REVIEW INVOICE ##########################################################################################################################################################################################################################################   


def review_invoice(request):
      # Retrieve all services from the database
    clients = Client.objects.all()  # Retrieve all clients for generating the report
    return render(request, 'review_invoice.html', {'clients': clients})



def edit_client(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get the client instance to edit
            client = Client.objects.get(pk=id)
            fm = ServiceProviderForm(request.POST, instance=client)  # Use the instance parameter to edit an existing object
            if fm.is_valid():
                fm.save()
                messages.success(request, "Successfully updated. Go back to client details.")
                return HttpResponseRedirect(f'/client-details/{id}/')  # Redirect to client details page after editing
        else:
            # Get the client instance to edit
            client = Client.objects.get(pk=id)
            fm = ClientForm(instance=client)
    
        return render(request, 'edit_client.html', {'form': fm, 'client_id': id})
    else:
        return HttpResponseRedirect('/')




def show_client(request, client_id):
    # Get the client object or return a 404 page if it doesn't exist
    client = get_object_or_404(Client, pk=client_id)

    # Assuming there's a ForeignKey from Services and Company to Client,
    # you can retrieve related services and company for this client
    services = Services.objects.filter(client=client)
    companies = Company.objects.filter(client=client)

    # Pass the data to the template
    return render(request, 'show_client.html', {'client': client, 'companies': companies, 'services': services})


def delete_client(request, client_id):
    if request.method == 'POST':
        client = Client.objects.get(pk=client_id)
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect('review-invoice')  # Replace 'client-list' with your actual client list URL
    else:
        client = Client.objects.get(pk=client_id)
        return render(request, 'delete_client.html', {'client': client})


   
######################################## ADD SERVCIES ##########################################################################################################################################  
def add_services(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            addservicesfm = ServicesForm(request.POST)
            if addservicesfm.is_valid():
                client = addservicesfm.cleaned_data['client']
                description = addservicesfm.cleaned_data['description']
                quantity = addservicesfm.cleaned_data['quantity']
                amount = addservicesfm.cleaned_data['amount']

                # Create a new Service object and save it to the database
                obj = Services(
                    client=client,
                    description=description,
                    quantity=quantity,
                    amount=amount
                )
                # Process the form data and save to the database
                obj.save()
                
                messages.success(
                    request, "Your 'Service Invoice' form has been saved successfully"
                )
                addservicesfm = ServicesForm()
        else:
            addservicesfm = ServicesForm()
        return render(request,'add_services.html', {'form': addservicesfm})
   


##########################################ADD SERVICES PROVIDER ############################################################################################################################################

def service_provider(request):
    companies = Company.objects.all()

    if request.user.is_authenticated:
        if request.method == 'POST':
            Servicefm = ServiceProviderForm(request.POST)
            if Servicefm.is_valid():
                  # Access cleaned data from each field
                client = Servicefm.cleaned_data['client']
                company_name = Servicefm.cleaned_data['company_name']
                handle_by = Servicefm.cleaned_data['handle_by']
                email = Servicefm.cleaned_data['email']
                phone = Servicefm.cleaned_data['phone']
                account_number = Servicefm.cleaned_data['account_number']
                ifsc_code = Servicefm.cleaned_data['ifsc_code']
                bank_name = Servicefm.cleaned_data['bank_name']
                gst_number = Servicefm.cleaned_data['gst_number']
                
               
                obj=Company(client=client,company_name=company_name,handle_by=handle_by,email=email,phone=phone,account_number=account_number,ifsc_code=ifsc_code,bank_name=bank_name,gst_number=gst_number)
                
                # Process the form data and save to the database
                obj.save()
                messages.success(
                    request, "Your 'Service Provider' form has been saved successfully"
                )

                return render(request, 'service_provider.html', {'form': Servicefm, 'companies': companies})

        else:
            Servicefm = ServiceProviderForm()


        return render(request, 'service_provider.html', {'form': Servicefm, 'companies': companies})
 

def delete_company(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            company = get_object_or_404(Company, pk=id)
            # You can add permission checks here if needed
            company.delete()
            return redirect('/service-provider/')  # Redirect after successful deletion
    return HttpResponse('Unauthorized', status=401)  # Return an error response if not authenticated

    
def edit_company(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            company = Company.objects.get(pk=id)
            fm = ServiceProviderForm(request.POST, instance=company)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Successfully updated Go Back")
        else:
            company = Company.objects.get(pk=id)
            fm = ServiceProviderForm(instance=company)
    
        return render(request, 'edit_company.html', {'form': fm})
    else:
        return HttpResponseRedirect('/')



############################################  REPORT  ####################################################################################################################################################################################################################################

def report(request):
    # Retrieve all services from the database
    clients = Client.objects.all()  # Retrieve all clients for generating the report
    return render(request, 'report.html', {'clients': clients})
def gst_report(request, client_id):

    if request.user.is_authenticated:
        try: 
        # Retrieve the client details based on the client_id
         client = Client.objects.get(pk=client_id)

        # Retrieve services related to this client
         services = Services.objects.filter(client=client)

        # Retrieve the associated Company (Service Provider) for this client
         company = Company.objects.get(client=client)

        # Calculate the total amount and GST
         total_amount = sum(service.amount for service in services)
         gst_amount = (total_amount * 18) / 100  # Assuming 18% GST
         total_amount_with_gst = total_amount + gst_amount

         return render(request, 'gstreport.html', {
            'client': client,
            'services': services,
            'company': company,  # Pass the company details to the template
            'total_amount': total_amount,
            'gst_amount': gst_amount,
            'total_amount_with_gst': total_amount_with_gst,
        })
        except Client.DoesNotExist:
        # Handle the case where the client doesn't exist
         return render(request, 'client_not_found.html')
   





############################################################################################################################################
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.urls import reverse

def generate_pdf(request):
    # Define the template name (your gstreport.html template)
    template_path = 'gstreport.html'

    # Define the context data that you want to pass to the template
    context = {
        # Add your context data here
    }

    # Load the template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="gst_report.pdf"'

    # Create a PDF document from the HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html))

    return response









