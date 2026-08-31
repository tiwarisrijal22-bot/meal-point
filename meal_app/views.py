from django.shortcuts import render,redirect
from .models import Feedback,Contact,CustomerDetail,ManagerDetail,MealPlan,Payment,UpiDetail
from django.contrib import messages
# Create your views here.
from django.http import JsonResponse
import cohere 

AI_CONTEXT = """
very important
if question is not exist in this context then cant reply a genral answer
importent notes alwayes follow this 
please implement this strictly 
Use HTML tags in responses like h1, ul, 
   li tags for better formatting. Avoid code blocks and always use 
   proper HTML tags for all responses .
# MealPlan and Service Platform – AI Context

This project is a customer and manager portal for a meal planning and service platform.
Customers can register, log in, view meal plans, access weekly meal schedules, and submit
feedback. Managers can register with their contact details, city, and address information.
The platform also stores contact inquiries from customers and recent feedback ratings.

Main data models in this project:
- CustomerDetail: name, email, password, phone, profile_pic, date
- ManagerDetail: name, email, password, phone, city, address, profile_pic
- MealPlan: plan_name, meals_included, duration, cost
- Contact: name, email, phone, question, date
- FeedBack: name, email, rating, review, date

The AI assistant should help users with account login issues, meal plan information,
weekly schedule questions, feedback submission, manager details, and general platform guidance.

Use HTML tags in responses like h1, ul, li, p, and strong for better formatting.
Avoid code blocks and always use proper HTML tags in the response.
"""


def build_dynamic_ai_context():
    lines = ["Dynamic database context:"]

    # Registered customers
    customers = CustomerDetail.objects.all()
    if customers:
        lines.append("\n=== Registered Customers ===")
        for customer in customers:
            # joined = customer.date.isoformat() if getattr(customer, "date", None) else "unknown"
            lines.append(
                f"- {customer.name} | email={customer.email} | "
                f"phone={customer.phone}"
            )
    else:
        lines.append("\n=== Registered Customers ===")
        lines.append("- No customers registered yet.")

    # Registered managers
    managers = ManagerDetail.objects.all()
    if managers:
        lines.append("\n=== Registered Managers ===")
        for manager in managers:
            address_preview = (manager.address or "")[:60].replace("\n", " ")
            lines.append(
                f"- {manager.name} | email={manager.email} | "
                f"phone={manager.phone} | city={manager.city} | "
                f"address={address_preview}"
            )
    else:
        lines.append("\n=== Registered Managers ===")
        lines.append("- No managers registered yet.")

    # Current meal plans
    meal_plans = MealPlan.objects.all().order_by("cost")
    if meal_plans:
        lines.append("\n=== Available Meal Plans ===")
        for plan in meal_plans:
            meals_preview = (plan.meals_included or "")[:80].replace("\n", " ")
            lines.append(
                f"- {plan.plan_name} | duration={plan.duration} | "
                f"cost=₹{plan.cost} | meals={meals_preview}"
            )
    else:
        lines.append("\n=== Available Meal Plans ===")
        lines.append("- No meal plans available yet.")

    # Recent customer inquiries
    contacts = Contact.objects.all().order_by("-contact_date")[:5]
    if contacts:
        lines.append("\n=== Recent Customer Contacts and Inquiries ===")
        for contact in contacts:
            question_preview = (contact.question or "")[:80].replace("\n", " ")
            lines.append(
                f"- {contact.name} ({contact.email}) | phone={contact.phone} | "
                f"question={question_preview}..."
            )
    else:
        lines.append("\n=== Recent Customer Contacts ===")
        lines.append("- No contact inquiries yet.")
    # Recent customer feedback/ratings
    feedbacks = Feedback.objects.all().order_by("-date")[:5]
    if feedbacks:
        lines.append("\n=== Recent Customer Feedback and Ratings ===")
        for feedback in feedbacks:
            review_preview = (feedback.review or "")[:80].replace("\n", " ")
            lines.append(
                f"- {feedback.name} | email={feedback.email} | "
                f"rating={feedback.rating} | review={review_preview}..."
            )
    else:
        lines.append("\n=== Recent Customer Feedback ===")
        lines.append("- No feedback available yet.")

    return "\n".join(lines)


def ai_assistant(request):
    return render(request, "html/ai_assistant.html")


def ai_chat(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."}, status=405)

    question = (request.POST.get("message") or "").strip()
    if not question:
        return JsonResponse({"reply": "Please enter a question."}, status=400)

    prompt = AI_CONTEXT + "\n\n" + build_dynamic_ai_context()

    try:
        response = co.chat(
            model="command-a-03-2025",
            message=question,
            preamble=prompt,
            temperature=0.2,
        )
        return JsonResponse({"reply": response.text})
    except Exception as exc:
        return JsonResponse(
            {"reply": "The AI service is temporarily unavailable. Please try again later."},
            status=503,
        )

def home(request):
    return render(request,'html/index.html')
def about_us(request):
    return render(request,'html/about_us.html')
def contact_us(request):
    if request.method == "GET":
        return render(request, "html/contact_us.html")
    if request.method == "POST":
        nm = request.POST["name"]
        em = request.POST["email"]
        ph = request.POST["phone"]
        qe = request.POST["question"]
        con= Contact(
            name=nm,
            email=em,
            phone=ph,
            question=qe
        )
        con.save()
        messages.success(request,"Thanks for contact")
        return redirect("contactpage")
def customer_feedback(request):
    if request.method=="GET":
            return render(request,'customer/customer_feedback.html')
       
    if request.method=="POST":
        nm=request.POST["name"]#fetching the value from html control with name 
        #request.POST is built in dictionary
        em=request.POST["email"]
        rt=request.POST["rating"]
        rw=request.POST["review"]
        f=Feedback(name=nm,email=em,rating=rt,review=rw)
        f.save()#it will save data into table
        messages.success(request,"Thanks for give your feedback")
        return redirect("feedbackpage")
def customer_registration(request):
    if request.method=="GET":
        return render(request,'customer/customer_registration.html')
    if request.method=="POST":
                nm=request.POST["name"]
                em=request.POST["email"]
                ps=request.POST["password"]
                ph=request.POST["phone"]
                pic = request.FILES.get("profile_pic")
    if not pic.name.lower().endswith((" .jpg", " .jpeg"," .png "," .gif"," .webp")):
        # check email existance before registration
                email_list=CustomerDetail.objects.filter(email=em)
                if len(email_list)>0:
                    messages.error(request,"this email allready exists, please take another one😓" )
                    return redirect("registrationpage")
                else:
                    cus=CustomerDetail(name=nm,email=em,password=ps,phone=ph,profile_pic=pic)##
                    cus.save()#it will save data into table
                    messages.success(request,"welcome ")
                    return redirect("loginpage")
def customer_login(request):
    if request.method=="GET":
     return render(request,'customer/customer_login.html')
    if request.method=="POST":
        em=request.POST["email"]
        ps=request.POST["password"]
        customer_list=CustomerDetail.objects.filter(email=em,password=ps)
        size=len(customer_list)
        if size>0:
            request.session["session_key"]=em
            request.session["role"]="customer"
            return redirect("homepage")
        else:
            messages.error(request,"Invalid credentials")
            return redirect("loginpage")
def customer_home(request):
   ## to indentify user we get data from session
    email_id=request.session["session_key"]
   ##getting the object from CustomerDetails model on the basis of Email
    customer_object=CustomerDetail.objects.get(email=email_id)
   ##creating dict to send object on the template
    context={"customer_key":customer_object }
    return render(request,'customer/customer_home.html',context)
def manager_login(request):
     if request.method=="GET":
        return render(request,'manager/manager_login.html')
     if request.method=="POST":
             em=request.POST["email"]
             ps=request.POST["password"]
             manager_list=ManagerDetail.objects.filter(email=em,password=ps)
             size=len(manager_list)
             if size>0:
                 request.session["session_key"]=em
                 request.session["role"]="manager"
                 return redirect("managerhomepage")
             else:
                 messages.error(request,"Invalid manager")
                 return redirect("managerloginpage")
def manager_detail(request):
    return render(request,'manager/manager_detail.html')
def manager_home(request):
    email_id=request.session["session_key"]
    manager_object=ManagerDetail.objects.get(email=email_id)
    context={"manager_key":manager_object }
    return render(request,'manager/manager_home.html', context)
##customerlogout
def customer_logout(request):
    del request.session ["session_key"]
    del request.session["role"]
    messages.success(request,"😀Thank you for visiting Meal Point. See you again!😀 ")
    return redirect("loginpage")
def manager_logout(request):
    del request.session ["session_key"]
    del request.session["role"]
    messages.success(request,"Logout successful. Have a great day!")
    return redirect("managerloginpage")

# def post_blog(request):
#     if request.method=="GET":
#         return render(request,"user/blog.html")
#     if request.method=="POST":
#         email_id=request.session["session_key"]
#         user_object=CustomerDetail.objects.get(email=email_id)
#         tl=request.POST["title"]
#         cl=request.POST["content"]
#         bl_image=request.FILES.get("img")
#         blog_object=Blog(user=user_object,title=tl,content=cl,blog_image=bl_image)
#         blog_object.save()
#         messages.success(request,"BLOG POSTED SUCCESSFULLY")
#         return redirect("customer_blog_page")

def all_review(request):
    #f_list feedback.objects.all()it will fetch all the data from table
    #f_list=feedback.object.order.by("-date")
    # f_list=Feedback.objects.filter(rating="⭐⭐⭐⭐⭐")
    f_list=Feedback.objects.all()
    context={
        "f_key":f_list
    }
    return render(request,"html/all_review.html",context)
def weekly_meal_schedule(request):
    f_list = MealPlan.objects.all()

    context = {
        "f_key": f_list
    }
    return render(request, "html/weekly_meal_schedule.html", context)
def food(request):
    return render(request, "html/food.html")
def purchase_plan(request, id):
    upi_object=UpiDetail.objects.first()
    print(upi_object.upiid)
    
    if request.method=="GET":
         plan_obj = MealPlan.objects.get(id=id)
         upi_link = f"upi://pay?pa={upi_object.upiid}&am={plan_obj.cost}&cu=INR"
    context = {
        "plan_key": plan_obj,
        "upi":upi_link
    }
    return render(request, "html/purchase_plan.html", context)

def make_payement(request):
    # to indentify user we get data from session
    # if request.method=="GET":
    if request.method=="POST":
        email_id=request.session["session_key"]
        customer_object=CustomerDetail.objects.get(email=email_id)
        p_id=request.POST["plan_id"]
        plan_ob=MealPlan.objects.get(id=p_id)
        am=request.POST["amount"]
        t_id=request.POST["transaction_id"]
        pos=Payment(customer=customer_object,plan=plan_ob,amount=am,transaction_id=t_id)
        pos.save()
        messages.success(request,"payment successful🤗")
        return redirect("purchase_plan", id=p_id)
# def mybooking_status(request):
#         email_id=request.session["session_key"]
#         customer_object=CustomerDetail.objects.get(email=email_id)
#         paylist=Payment.objects.filter(customer=customer_object)
#         context={
#             "P_key":paylist
#             }
#         return render(request,"customer/mybooking_status.html",context)
def mybooking_status(request):
    email_id=request.session["session_key"] 
    customer_object=CustomerDetail.objects.get(email=email_id)
    paylist=Payment.objects.filter(customer=customer_object)
    context={
       "p_key":paylist
    }


    return render(request,'customer/mybooking_status.html',context)

def all_bookings(request):
    paylist = Payment.objects.all()

    context = {
        "p_key": paylist
    }

    return render(request, "manager/all_booking.html", context)
# def edit_profile(request):
#         email_id=request.session["session_key"] 
#         customer_object=CustomerDetail.objects.get(email=email_id)
#         if request.method=="GET":
#             context = {
#                     "customer_key": customer_object
#                  }
#          return render(request,'customer/edit_profile.html',context)
#     if request.method=="POST":
#         nm=request.POST["name"]
#         ph=request.POST["phone"]
#         if "profile_pic" in request.FILES:
#         customer_object.profile_pic=request.FILES.get("profile_pic")
#         customer_object.save()#updating profile pic
#         ### updating name and phone ###
#         customer_object.name=nm
#         customer_object.phone=ph
#         customer_object.save()##updating name and phone with new/old value
#         messages.success(request,"profile update successfully👍👍")
#         return redirect(homepage)
def edit_profile(request):
    email_id = request.session["session_key"]

    customer_object = CustomerDetail.objects.get(email=email_id)

    if request.method == "GET":
        context = {
            "customer_key": customer_object
        }
        return render(request, "customer/edit_profile.html", context)

    if request.method == "POST":
        nm = request.POST["name"]
        ph = request.POST["phone"]

        # Updating profile picture
        if "profile_pic" in request.FILES:
            customer_object.profile_pic = request.FILES.get("profile_pic")

        # Updating name and phone
        customer_object.name = nm
        customer_object.phone = ph

        customer_object.save()

        messages.success(request, "Profile updated successfully 👍👍")

        return redirect("homepage")
def faq(request):
    return render(request,'html/faq.html')