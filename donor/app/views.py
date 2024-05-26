
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserForm,DonorSignupForm,VolunteerSignupForm,LoginForm,MyPasswordChangeForm,DonateNowForm,DonationAreaForm
from django.contrib.auth.models import User 
from .models import Donor,Volunteer,Donation,DonationArea,Gallery
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from datetime import date
from django.utils.timezone import now

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
def index(request):
    return render(request, "index.html")

def gallery(request):
    gallery_items = Gallery.objects.all()
    return render(request, "gallery.html", {'gallery_items': gallery_items})


class login_admin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-admin.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        
        username = request.POST['username']
        password = request.POST['password']
        try:
            user=authenticate(username=username,password=password)
            if user:
                
                if user.is_staff:
                    login(request,user)
                    messages.success(request,'Login Successfully')
                    return redirect('/index-admin')
                else:
                    messages.warning(request, 'Invalid Admin User!')
            else:
                messages.warning(request, 'Invalid Username and Password!')
        except:
            messages.warning(request,'Login Failed!')
        return render(request,"login-admin.html",locals())

    
class login_donor(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-donor.html", {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        
        username = request.POST['username']
        password = request.POST['password']
        try:
            user=authenticate(username=username,password=password)
            if user:
                donor_user = Donor.objects.filter(user_id=user.id)
                if donor_user:
                    login(request,user)
                    messages.success(request,'Login Successfully')
                    return redirect('/index-donor')
                else:
                    messages.warning(request, 'Invalid Donor User!')
            else:
                messages.warning(request, 'Invalid Username and Password!')
        except:
            messages.warning(request,'Login Failed!')
        return render(request,"login-donor.html",locals())

    
  

class login_volunteer(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-volunteer.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user=authenticate(username=username,password=password)
            if user:
                vol_user = Volunteer.objects.filter(user_id=user.id)
                if vol_user:
                    login(request,user)
                    messages.success(request,'Login Successfully')
                    return redirect('/index-volunteer')
                else:
                    messages.warning(request, 'Invalid Volunteer User!')
            else:
                messages.warning(request, 'Invalid Username and Password!')
        except:
            messages.warning(request,'Login Failed!')
        return render(request,"login-volunteer.html",locals())

    





class signup_donor(View):
    def get(self, request):
        form1 = UserForm()
        form2 = DonorSignupForm()
        return render(request, "signup_donor.html", locals())

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = DonorSignupForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form1.is_valid() and form2.is_valid():
            fn = form1.cleaned_data["first_name"]
            ln = form1.cleaned_data["last_name"]
            em = form1.cleaned_data["email"]
            us = form1.cleaned_data["username"]
            pwd = form1.cleaned_data["password1"]  # Directly access cleaned_data for password
            contact = form2.cleaned_data["contact"]
            userpic = form2.cleaned_data["userpic"]
            address = form2.cleaned_data["address"]

            try:
                user = User.objects.create_user(first_name=fn, last_name=ln, username=us, email=em, password=pwd)
                Donor.objects.create(user=user, contact=contact, userpic=userpic, address=address)
                messages.success(request, 'Congratulations!! Donor Profile Created Successfully')
               
            except Exception as e:
                messages.warning(request, f'Profile not Created!! Error: {str(e)}')

        return render(request, "signup_donor.html", {'form1': form1, 'form2': form2})
             
    

class signup_volunteer(View):
    def get(self, request):
        form1 = UserForm()
        form2 = VolunteerSignupForm()
        return render(request, "signup_volunteer.html", locals())
    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form1.is_valid() and form2.is_valid():
            fn = form1.cleaned_data["first_name"]
            ln = form1.cleaned_data["last_name"]
            em = form1.cleaned_data["email"]
            us = form1.cleaned_data["username"]
            pwd = form1.cleaned_data["password1"]  # Directly access cleaned_data for password
            contact = form2.cleaned_data["contact"]
            userpic = form2.cleaned_data["userpic"]
            idpic = form2.cleaned_data["idpic"]
            address = form2.cleaned_data["address"]
            aboutme = form2.cleaned_data["aboutme"]

            try:
                user = User.objects.create_user(first_name=fn, last_name=ln, username=us, email=em, password=pwd)
                Volunteer.objects.create(user=user, contact=contact, userpic=userpic,idpic=idpic,aboutme=aboutme, address=address,
                status='pending')
                messages.success(request, 'Congratulations!! Volunteer Profile Created Successfully')
               
            except Exception as e:
                messages.warning(request, f'Profile not Created!! Error: {str(e)}')

        return render(request, "signup_volunteer.html", {'form1': form1, 'form2': form2})
             


def index_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    totaldonations=Donation.objects.all().count()
    totaldonors=Donor.objects.all().count()
    totalvolunteers=Volunteer.objects.all().count()
    totalpendingdonations=Donation.objects.filter(status="pending").count()
    totalaccepteddonations=Donation.objects.filter(status="accept").count()
    totaldelivereddonations=Donation.objects.filter(status="Donation Delivered Successfully").count()
    totaldonationareas=DonationArea.objects.all().count()
    return render(request, "index-admin.html",locals())


# admin dashboard
def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="pending")
    return render(request, "pending-donation.html",locals())


def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="accept")
    return render(request, "accepted-donation.html",locals())


def rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="reject")
    return render(request, "rejected-donation.html",locals())


def volunteerallocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="Volunteer Allocated")
    return render(request, "volunteerallocated-donation.html",locals())


def donationrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="Donation Received")
    return render(request, "donationrec-admin.html",locals())


def donationnotrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="Donation Not Received")
    return render(request, "donationnotrec-admin.html",locals())


def donationdelivered_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.filter(status="Donation Delivered Successfully")
    return render(request, "donationdelivered-admin.html",locals())


def all_donations(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donation= Donation.objects.all()
    return render(request, "all-donations.html",locals())

def delete_donation(request,pid):
    donation= Donation.objects.get(id=pid)
    donation.delete()
    return redirect('all_donations')



def manage_donor(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donor= Donor.objects.all()
    return render(request, "manage-donor.html",locals())


def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.filter(status='pending')
    return render(request, "new-volunteer.html",locals())


def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.filter(status='accept')
    return render(request, "accepted-volunteer.html",locals())


def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.filter(status='reject')
    return render(request, "rejected-volunteer.html",locals())


def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    volunteer=Volunteer.objects.all()
    return render(request, "all-volunteer.html",locals())

def delete_volunteer(request,pid):
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('all_volunteer')

class add_area(View):
    def get(self, request):
        form = DonationAreaForm()
        return render(request, "add-area.html", {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-admin')

        form = DonationAreaForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Save the form directly
                messages.success(request, 'Area added successfully')
                return redirect('/add-area')  # Redirect to the same page or another page
            except Exception as e:
                messages.warning(request, f'Area not added: {str(e)}')
        else:
            messages.warning(request, 'Invalid form submission')

        return render(request, "add-area.html", {'form': form})


class edit_area(View):
    def get(self, request,pid):
        form = DonationAreaForm()
        area=DonationArea.objects.get(id=pid)
        return render(request, "edit-area.html", {'form': form})

    def post(self, request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')

        form = DonationAreaForm(request.POST)
        area=DonationArea.objects.get(id=pid)
        areaname=request.POST['areaname']
        description=request.POST['description']
        area.areaname=areaname
        area.description=description
        if form.is_valid():
            try:
                area.save()  # Save the form directly
                messages.success(request, 'Area Updated successfully')
                return redirect('manage_area')  # Redirect to the same page or another page
            except Exception as e:
                messages.warning(request, f'Area not Updated: {str(e)}')
        else:
            messages.warning(request, 'Invalid form submission')
        return render(request, "edit-area.html", {'form': form})

   


def manage_area(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    
    areas = DonationArea.objects.all()
    context = {
        'areas': areas,
    }
    return render(request, "manage-area.html", context)

def delete_area(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area=DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')


class changepwd_admin(View):
    def get(self, request):
        form = MyPasswordChangeForm(request.user)
        return render(request, "changepwd-admin.html",locals())
    def post(self,request):
        form = MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confirmpass=request.POST['new_password2']
        try:
            if newpass==confirmpass:
                user= User.objects.get(id=request.user.id)
                if user.check_password(old):
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Change Password Successfully')
                else:
                    messages.warning(request,'Old Password not matched')
            else:
                messages.warning(request,'Old Password and New Password are different')
        except:
             messages.warning(request,'Failed to Change Password')
        return render(request,"changepwd-admin.html",locals())

def logoutView(request):
    logout(request)
    return redirect("index")


# admin view details
class accepted_donationdetail(View):
    def get(self, request, pid):
        donation = Donation.objects.get(id=pid)
        donation_areas = DonationArea.objects.all()
        volunteers = Volunteer.objects.filter(status='accept')
        return render(request, "accepted-donationdetail.html", {
            'donation': donation,
            'donation_areas': donation_areas,
            'volunteers': volunteers
        })

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        donationareaid = request.POST['donationareaid']
        volunteerid = request.POST['volunteerid']
        adminremark = request.POST['adminremark']
        da = DonationArea.objects.get(id=donationareaid)
        v = Volunteer.objects.get(id=volunteerid)

        try:
            donation.donationarea = da
            donation.volunteer = v
            donation.adminremark = adminremark
            donation.status = "Volunteer Allocated"
            donation.volremark = "Not Updated Yet"
            donation.updationdate = date.today()
            donation.save()
            messages.success(request, "Volunteer Allocated Successfully")
        except:
            messages.warning(request, "Failed to Allocate Volunteer")

        donation_areas = DonationArea.objects.all()
        volunteers = Volunteer.objects.filter(status='accept')
        return render(request, "accepted-donationdetail.html", {
            'donation': donation,
            'donation_areas': donation_areas,
            'volunteers': volunteers
        })



    

class view_volunteerdetail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        volunteer = Volunteer.objects.get(id=pid)
        return render(request, "view-volunteerdetail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        volunteer = Volunteer.objects.get(id=pid)
        status=request.POST['status']
        adminremark=request.POST['adminremark']
        try:
            volunteer.adminremark=adminremark
            volunteer.status=status
            volunteer.updationdate=date.today()
            volunteer.save()
            messages.success(request,'Volunteer Updated Successfully')
        except:
            messages.warning(request,'Failed to Update Volunteer')
        return render(request, "view-volunteerdetail.html",locals())


def view_donordetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donor=Donor.objects.get(id=pid)
    return render(request, "view-donordetail.html",locals())


class view_donationdetail(View):
    def get(self,request,pid):
        donation = Donation.objects.get(id=pid)
        return render(request, "view-donationdetail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        status=request.POST['status']
        adminremark=request.POST['adminremark']
        try:
            donation.adminremark=adminremark
            donation.status=status
            donation.updationdate=date.today()
            donation.save()
            messages.success(request,'Status & Remark Successfully')
        except:
            messages.warning(request,'Failed to Update Status & Remark')
        return render(request, "view-donationdetail.html",locals())


def delete_donor(request,pid):
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('manage_donor')


# donor dashboard
def index_donor(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')

    user = request.user
    try:
        donor = Donor.objects.get(user=user)
        donationcount = Donation.objects.filter(donor=donor).count()
        acceptedcount = Donation.objects.filter(donor=donor, status="accept").count()
        rejectedcount = Donation.objects.filter(donor=donor, status="reject").count()
        pendingcount = Donation.objects.filter(donor=donor, status="pending").count()
        deliveredcount = Donation.objects.filter(donor=donor, status="Donation Delivered Successfully").count()
    except Donor.DoesNotExist:
        # Handle case where Donor object doesn't exist for the logged-in user
        return redirect('/login-donor')  # or render an error page

    context = {
        'donationcount': donationcount,
        'acceptedcount': acceptedcount,
        'rejectedcount': rejectedcount,
        'pendingcount': pendingcount,
        'deliveredcount': deliveredcount,
    }

    return render(request, "index-donor.html", context)


class donate_now(View):
    def get(self, request):
        form = DonateNowForm()
        return render(request, "donate-now.html", {'form': form})

    def post(self, request):
        form = DonateNowForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            try:
                donor = Donor.objects.get(user=user)
            except Donor.DoesNotExist:
                messages.error(request, 'Donor not found.')
                return render(request, "donate-now.html", {'form': form})
            
            donationame = form.cleaned_data['donationame']
            donationpic = request.FILES.get('donationpic')
            collectionloc = form.cleaned_data['collectionloc']
            description = form.cleaned_data['description']
            
            try:
                Donation.objects.create(
                    donor=donor,
                    donationame=donationame,
                    donationpic=donationpic,
                    collectionloc=collectionloc,
                    description=description,
                    status='pending',
                    donationdate=date.today()
                )
                messages.success(request, 'Congratulations!! Donation saved successfully.')
                 # Redirect to a success page or any other view
            except Exception as e:
                messages.warning(request, f'Failed to donate: {str(e)}')
        else:
            messages.warning(request, 'Invalid form submission.')
        
        return render(request, "donate-now.html", {'form': form})
                   
    



def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user = request.user
    donor = Donor.objects.get(user=user)
    donation=Donation.objects.filter(donor=donor)
    return render(request, "donation-history.html",locals())


class profile_donor(View):
    def get(self, request):
        form1 = UserForm()
        form2 = DonorSignupForm()
        user = request.user
        donor = Donor.objects.get(user=user)
        return render(request, "profile-donor.html", locals())
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        
        form1 = UserForm(request.POST)
        form2 = DonorSignupForm(request.POST)
        user = request.user
        donor = Donor.objects.get(user=user)
        fn = request.POST["firstname"]  # Access cleaned data
        ln = request.POST["lastname"]
        contact = request.POST["contact"]
        address = request.POST["address"]

            
        donor.user.first_name = fn
        donor.user.last_name = ln
        donor.contact = contact
        donor.address = address
            
        try:
            userpic = request.FILES['userpic']
            donor.userpic = userpic
            donor.save()
            donor.user.save()
            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            messages.warning(request, 'Profile update failed: {}'.format(str(e)))  # Convert exception to string
        
        
        return render(request, "profile-donor.html", locals())   

        
           
class changepwd_donor(View):
    def get(self, request):
        form = MyPasswordChangeForm(request.user)
        return render(request, "changepwd-donor.html",locals())
    def post(self,request):
        form = MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confirmpass=request.POST['new_password2']
        try:
            if newpass==confirmpass:
                user= User.objects.get(id=request.user.id)
                if user.check_password(old):
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Password Changed Successfully')
                else:
                    messages.warning(request,'Old Password not matched')
            else:
                messages.warning(request,'Old Password and New Password are different')
        except:
             messages.warning(request,'Failed to Change Password')
        return render(request,"changepwd-donor.html",locals())







# volunteer dashboard
def index_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    collectionReq=Donation.objects.filter(volunteer=volunteer,status="Volunteer Allocated").count()
    receivedDonation=Donation.objects.filter(volunteer=volunteer,status="Donation Received").count()
    totalNotRecDonation=Donation.objects.filter(volunteer=volunteer,status="Donation Not Received").count()
    
    deliveredDonation=Donation.objects.filter(volunteer=volunteer,status="Donation Delivered Successfully").count()
    
    return render(request, "index-volunteer.html",locals())


def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Volunteer Allocated")
    return render(request, "collection-req.html",locals())


def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Donation Received")
    return render(request, "donationrec-volunteer.html",locals())


def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Donation Not Received")
    return render(request, "donationnotrec-volunteer.html",locals())


def donationdelivered_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation=Donation.objects.filter(volunteer=volunteer,status="Donation Delivered Successfully")
    return render(request, "donationdelivered-volunteer.html",locals())


class profile_volunteer(View):
    def get(self, request):
        form1=UserForm()
        form2=VolunteerSignupForm()
        user = request.user
        volunteer = Volunteer.objects.get(user=user)
        return render(request, "profile-volunteer.html",locals())
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')
        
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST)
        user = request.user
        volunteer = Volunteer.objects.get(user=user)
        fn = request.POST["firstname"] 
        ln = request.POST["lastname"]
        contact = request.POST["contact"]
        address = request.POST["address"]
        aboutme= request.POST["aboutme"]
        volunteer.user.first_name = fn
        volunteer.user.last_name = ln
        volunteer.contact = contact
        volunteer.address = address
        volunteer.aboutme = aboutme
            
        try:
            userpic = request.FILES['userpic']
            volunteer.userpic = userpic
            idpic=request.FILES['idpic']
            volunteer.idpic = idpic
            volunteer.save()
            volunteer.user.save()
            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            messages.warning(request, 'Profile update failed: {}'.format(str(e)))  # Convert exception to string
        
        
        return render(request, "profile-volunteer.html", locals())   



class changepwd_volunteer(View):
    def get(self, request):
        form = MyPasswordChangeForm(request.user)
        return render(request, "changepwd-volunteer.html",locals())
    def post(self,request):
        form = MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')
        old=request.POST['old_password']
        newpass=request.POST['new_password1']
        confirmpass=request.POST['new_password2']
        try:
            if newpass==confirmpass:
                user= User.objects.get(id=request.user.id)
                if user.check_password(old):
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Change Password Successfully')
                else:
                    messages.warning(request,'Old Password not matched')
            else:
                messages.warning(request,'Old Password and New Password are different')
        except:
             messages.warning(request,'Failed to Change Password')
        return render(request,"changepwd-volunteer.html",locals())




# view details
def donationdetail_donor(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    donation = Donation.objects.get(id=pid)
    return render(request, "donationdetail-donor.html", locals())

class donationcollection_detail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        return render(request, "donationcollection-detail.html",locals())
    def post(self,request,pid):
        donation = Donation.objects.get(id=pid)
        status=request.POST['status']
        volremark=request.POST['volremark']
        try:
            donation.status=status
            donation.volremark=volremark
            donation.updationdate=date.today()
            donation.save()
            messages.success(request,"Volunteer Status and Remark Updated Successfully")
        except:
            messages.warning(request,"Failed to Update Volunteer Status and Remark")
        return render(request, "donationcollection-detail.html",locals())
    


class donationrec_detail(View):
    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        return render(request, "donationrec-detail.html", {'donation': donation})

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        try:
            donation = Donation.objects.get(id=pid)
            status = request.POST.get('status')
            delivery_pic = request.FILES.get('deliverypic')  # Corrected variable name
            if status:  # Check if status is provided
                donation.status = status
            donation.updationdate = now()  # Use Django's timezone-aware now()
            donation.save()

            if delivery_pic:  # Check if delivery_pic is provided
                Gallery.objects.create(donation=donation, deliverypic=delivery_pic)  # Corrected field name
            messages.success(request, "Donation Delivered Successfully")
        except Donation.DoesNotExist:
            messages.warning(request, "Donation not found")
        except Exception as e:
            messages.warning(request, f"Donation Delivery Failed: {str(e)}")
            print("Error:", str(e))


        return render(request, "donationrec-detail.html", {'donation': donation})

class donationnotrec_detail(View):
    def get(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        return render(request, "donationnotrec_detail.html", {'donation': donation})

    def post(self, request, pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        try:
            donation = Donation.objects.get(id=pid)
            status = request.POST.get('status')
            delivery_pic = request.FILES.get('deliverypic')  # Corrected variable name
            if status:  # Check if status is provided
                donation.status = status
            donation.updationdate = now()  # Use Django's timezone-aware now()
            donation.save()

            if delivery_pic:  # Check if delivery_pic is provided
                Gallery.objects.create(donation=donation, deliverypic=delivery_pic)  # Corrected field name
            messages.success(request, "Donation Delivered Successfully")
        except Donation.DoesNotExist:
            messages.warning(request, "Donation not found")
        except Exception as e:
            messages.warning(request, f"Donation Delivery Failed: {str(e)}")
            print("Error:", str(e))


        return render(request, "donationnotrec_detail.html", {'donation': donation})

def send_custom_email(request):
    user = request.user  # Assuming the user is authenticated
    subject = 'Welcome to Our Website!'
    html_message = render_to_string('password_reset_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'yadavshweta9460@gmail.com'  # Update with your email address
    to_email = user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    return HttpResponse('Email sent successfully!')
