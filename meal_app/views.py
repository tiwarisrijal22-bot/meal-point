import cohere
import os
from django.shortcuts import render, redirect
from .models import (
    Feedback,
    Contact,
    CustomerDetail,
    ManagerDetail,
    MealPlan,
    Payment,
    UpiDetail,
)
from django.contrib import messages
from django.http import JsonResponse


# =========================================================
# COHERE AI
# =========================================================

# co = cohere.Client(os.getenv("3Qr9unxPeKqDRBWersAi1Mets3qXnZp9Q2bdOVf4"))

AI_CONTEXT = """
IMPORTANT INSTRUCTIONS:

You are the AI Assistant for the Meal Point website.

ONLY answer questions related to Meal Point and the information
available in this context.

If the user's question is not related to Meal Point, its customers,
managers, meal plans, weekly meal schedule, feedback, contact
inquiries, login, registration, payment, booking, profile, FAQ,
or general use of this website, politely say that you can only
help with Meal Point.

Do not invent information that is not available in the context.

Always follow these instructions strictly.

Use HTML tags such as <h1>, <h2>, <p>, <ul>, <li>, and <strong>
for better formatting.

Do NOT use Markdown.
Do NOT use code blocks.

# Meal Point – AI Context

This project is a customer and manager portal for a meal planning
and food service platform.

Customers can:
- Register
- Login
- View meal plans
- View weekly meal schedules
- Purchase meal plans
- Make payments
- View booking/payment status
- Submit feedback
- Edit their profile
- Contact Meal Point
- Use the AI Assistant

Managers can:
- Login
- View manager details
- Manage meal plans
- View customer bookings
- View customer feedback
- Handle customer inquiries

Main data models:

CustomerDetail:
name, email, password, phone, profile_pic, date

ManagerDetail:
name, email, password, phone, city, address, profile_pic

MealPlan:
plan_name, meals_included, duration, cost

Contact:
name, email, phone, question, contact_date

Feedback:
name, email, rating, review, date

Payment:
customer, plan, amount, transaction_id

UpiDetail:
upiid

The AI assistant should help users with:
- Customer registration
- Customer login
- Manager login
- Meal plan information
- Meal prices and duration
- Weekly meal schedule
- Payment and booking guidance
- Feedback submission
- Contact inquiries
- Customer profile
- Manager details
- General Meal Point website guidance

Use the live database context provided below when answering
questions about available customers, managers, meal plans,
inquiries and feedback.
"""


def build_dynamic_ai_context():

    lines = ["Dynamic database context:"]

    # =====================================================
    # REGISTERED CUSTOMERS
    # =====================================================

    customers = CustomerDetail.objects.all()

    if customers:
        lines.append("\n=== Registered Customers ===")

        for customer in customers:
            lines.append(
                f"- {customer.name} | "
                f"email={customer.email} | "
                f"phone={customer.phone}"
            )
    else:
        lines.append("\n=== Registered Customers ===")
        lines.append("- No customers registered yet.")

    # =====================================================
    # REGISTERED MANAGERS
    # =====================================================

    managers = ManagerDetail.objects.all()

    if managers:
        lines.append("\n=== Registered Managers ===")

        for manager in managers:

            address_preview = (
                getattr(manager, "address", "") or ""
            )[:60].replace("\n", " ")

            lines.append(
                f"- {manager.name} | "
                f"email={manager.email} | "
                f"phone={manager.phone} | "
                f"city={manager.city} | "
                f"address={address_preview}"
            )

    else:
        lines.append("\n=== Registered Managers ===")
        lines.append("- No managers registered yet.")

    # =====================================================
    # MEAL PLANS
    # =====================================================

    meal_plans = MealPlan.objects.all().order_by("cost")

    if meal_plans:

        lines.append("\n=== Available Meal Plans ===")

        for plan in meal_plans:

            meals_preview = (
                getattr(plan, "meals_included", "") or ""
            )[:80].replace("\n", " ")

            lines.append(
                f"- {plan.plan_name} | "
                f"duration={plan.duration} | "
                f"cost=₹{plan.cost} | "
                f"meals={meals_preview}"
            )

    else:

        lines.append("\n=== Available Meal Plans ===")
        lines.append("- No meal plans available yet.")

    # =====================================================
    # RECENT CONTACT INQUIRIES
    # =====================================================

    contacts = Contact.objects.all().order_by("-contact_date")[:5]

    if contacts:

        lines.append(
            "\n=== Recent Customer Contacts and Inquiries ==="
        )

        for contact in contacts:

            question_preview = (
                getattr(contact, "question", "") or ""
            )[:80].replace("\n", " ")

            lines.append(
                f"- {contact.name} | "
                f"email={contact.email} | "
                f"phone={contact.phone} | "
                f"question={question_preview}"
            )

    else:

        lines.append("\n=== Recent Customer Contacts ===")
        lines.append("- No contact inquiries yet.")

    # =====================================================
    # RECENT FEEDBACK
    # =====================================================

    feedbacks = Feedback.objects.all().order_by("-date")[:5]

    if feedbacks:

        lines.append(
            "\n=== Recent Customer Feedback and Ratings ==="
        )

        for feedback in feedbacks:

            review_preview = (
                getattr(feedback, "review", "") or ""
            )[:80].replace("\n", " ")

            lines.append(
                f"- {feedback.name} | "
                f"email={feedback.email} | "
                f"rating={feedback.rating} | "
                f"review={review_preview}"
            )

    else:

        lines.append("\n=== Recent Customer Feedback ===")
        lines.append("- No feedback available yet.")

    return "\n".join(lines)


# =========================================================
# AI ASSISTANT PAGE
# =========================================================

def ai_assistant(request):
    return render(request, "html/ai_assistant.html")


# =========================================================
# AI CHAT API
# =========================================================

def ai_chat(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "reply": "<p>Invalid request method.</p>"
            },
            status=405
        )

    question = (
        request.POST.get("message") or ""
    ).strip()

    if not question:

        return JsonResponse(
            {
                "reply": "<p>Please enter a question.</p>"
            },
            status=400
        )

    # Check API key
   
    api_key = os.getenv("CO_API_KEY")
    if not api_key:

        return JsonResponse(
            {
                "reply": (
                    "<p>AI service is not configured. "
                    "Please contact the administrator.</p>"
                )
            },
            status=503
        )

    try:

        # Create Cohere client using environment variable
        client = cohere.Client(api_key)

        dynamic_context = build_dynamic_ai_context()

        prompt = (
            AI_CONTEXT
            + "\n\n"
            + dynamic_context
        )

        response = client.chat(
            model="command-a-03-2025",
            message=question,
            preamble=prompt,
            temperature=0.2,
        )

        return JsonResponse(
            {
                "reply": response.text
            }
        )

    except Exception:

        return JsonResponse(
            {
                "reply": (
                    "<p>The AI service is temporarily unavailable. "
                    "Please try again later.</p>"
                )
            },
            status=503
        )


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, "html/index.html")


# =========================================================
# ABOUT US
# =========================================================

def about_us(request):
    return render(request, "html/about_us.html")


# =========================================================
# CONTACT US
# =========================================================

def contact_us(request):

    if request.method == "GET":

        return render(
            request,
            "html/contact_us.html"
        )

    if request.method == "POST":

        nm = request.POST["name"]
        em = request.POST["email"]
        ph = request.POST["phone"]
        qe = request.POST["question"]

        con = Contact(
            name=nm,
            email=em,
            phone=ph,
            question=qe
        )

        con.save()

        messages.success(
            request,
            "Thanks for contact"
        )

        return redirect("contactpage")


# =========================================================
# CUSTOMER FEEDBACK
# =========================================================

def customer_feedback(request):

    if request.method == "GET":

        return render(
            request,
            "customer/customer_feedback.html"
        )

    if request.method == "POST":

        nm = request.POST["name"]
        em = request.POST["email"]
        rt = request.POST["rating"]
        rw = request.POST["review"]

        f = Feedback(
            name=nm,
            email=em,
            rating=rt,
            review=rw
        )

        f.save()

        messages.success(
            request,
            "Thanks for giving your feedback"
        )

        return redirect("feedbackpage")


# =========================================================
# CUSTOMER REGISTRATION
# =========================================================

def customer_registration(request):

    if request.method == "GET":

        return render(
            request,
            "customer/customer_registration.html"
        )

    if request.method == "POST":

        nm = request.POST["name"]
        em = request.POST["email"]
        ps = request.POST["password"]
        ph = request.POST["phone"]

        pic = request.FILES.get("profile_pic")

        # Check email already exists

        email_exists = CustomerDetail.objects.filter(
            email=em
        ).exists()

        if email_exists:

            messages.error(
                request,
                "This email already exists, please take another one 😓"
            )

            return redirect("registrationpage")

        # Profile picture is optional

        if pic:

            allowed_extensions = (
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp"
            )

            if not pic.name.lower().endswith(
                allowed_extensions
            ):

                messages.error(
                    request,
                    "Only JPG, JPEG, PNG, GIF and WEBP images are allowed."
                )

                return redirect("registrationpage")

        # Create customer

        cus = CustomerDetail(
            name=nm,
            email=em,
            password=ps,
            phone=ph,
            profile_pic=pic
        )

        cus.save()

        messages.success(
            request,
            "Welcome to Meal Point"
        )

        return redirect("loginpage")


# =========================================================
# CUSTOMER LOGIN
# =========================================================

def customer_login(request):

    if request.method == "GET":

        return render(
            request,
            "customer/customer_login.html"
        )

    if request.method == "POST":

        em = request.POST["email"]
        ps = request.POST["password"]

        customer_list = CustomerDetail.objects.filter(
            email=em,
            password=ps
        )

        if customer_list.exists():

            request.session["session_key"] = em
            request.session["role"] = "customer"

            return redirect("homepage")

        else:

            messages.error(
                request,
                "Invalid credentials"
            )

            return redirect("loginpage")


# =========================================================
# CUSTOMER HOME
# =========================================================

def customer_home(request):

    email_id = request.session["session_key"]

    customer_object = CustomerDetail.objects.get(
        email=email_id
    )

    context = {
        "customer_key": customer_object
    }

    return render(
        request,
        "customer/customer_home.html",
        context
    )


# =========================================================
# MANAGER LOGIN
# =========================================================

def manager_login(request):

    if request.method == "GET":

        return render(
            request,
            "manager/manager_login.html"
        )

    if request.method == "POST":

        em = request.POST["email"]
        ps = request.POST["password"]

        manager_list = ManagerDetail.objects.filter(
            email=em,
            password=ps
        )

        if manager_list.exists():

            request.session["session_key"] = em
            request.session["role"] = "manager"

            return redirect("managerhomepage")

        else:

            messages.error(
                request,
                "Invalid manager"
            )

            return redirect("managerloginpage")


# =========================================================
# MANAGER DETAIL
# =========================================================

def manager_detail(request):

    return render(
        request,
        "manager/manager_detail.html"
    )


# =========================================================
# MANAGER HOME
# =========================================================

def manager_home(request):

    email_id = request.session["session_key"]

    manager_object = ManagerDetail.objects.get(
        email=email_id
    )

    context = {
        "manager_key": manager_object
    }

    return render(
        request,
        "manager/manager_home.html",
        context
    )


# =========================================================
# CUSTOMER LOGOUT
# =========================================================

def customer_logout(request):

    request.session.pop("session_key", None)
    request.session.pop("role", None)

    messages.success(
        request,
        "😀 Thank you for visiting Meal Point. See you again! 😀"
    )

    return redirect("loginpage")


# =========================================================
# MANAGER LOGOUT
# =========================================================

def manager_logout(request):

    request.session.pop("session_key", None)
    request.session.pop("role", None)

    messages.success(
        request,
        "Logout successful. Have a great day!"
    )

    return redirect("managerloginpage")


# =========================================================
# ALL REVIEWS
# =========================================================

def all_review(request):

    f_list = Feedback.objects.all()

    context = {
        "f_key": f_list
    }

    return render(
        request,
        "html/all_review.html",
        context
    )


# =========================================================
# WEEKLY MEAL SCHEDULE
# =========================================================

def weekly_meal_schedule(request):

    f_list = MealPlan.objects.all()

    context = {
        "f_key": f_list
    }

    return render(
        request,
        "html/weekly_meal_schedule.html",
        context
    )


# =========================================================
# FOOD
# =========================================================

def food(request):

    return render(
        request,
        "html/food.html"
    )


# =========================================================
# PURCHASE PLAN
# =========================================================

def purchase_plan(request, id):

    plan_obj = MealPlan.objects.get(
        id=id
    )

    upi_object = UpiDetail.objects.first()

    if not upi_object:

        messages.error(
            request,
            "UPI details are not configured."
        )

        return redirect("homepage")

    upi_link = (
        f"upi://pay?"
        f"pa={upi_object.upiid}"
        f"&am={plan_obj.cost}"
        f"&cu=INR"
    )

    context = {
        "plan_key": plan_obj,
        "upi": upi_link
    }

    return render(
        request,
        "html/purchase_plan.html",
        context
    )


# =========================================================
# MAKE PAYMENT
# =========================================================

def make_payement(request):

    if request.method == "POST":

        email_id = request.session["session_key"]

        customer_object = CustomerDetail.objects.get(
            email=email_id
        )

        p_id = request.POST["plan_id"]

        plan_ob = MealPlan.objects.get(
            id=p_id
        )

        am = request.POST["amount"]
        t_id = request.POST["transaction_id"]

        pos = Payment(
            customer=customer_object,
            plan=plan_ob,
            amount=am,
            transaction_id=t_id
        )

        pos.save()

        messages.success(
            request,
            "Payment successful 🤗"
        )

        return redirect(
            "purchase_plan",
            id=p_id
        )


# =========================================================
# MY BOOKING STATUS
# =========================================================

def mybooking_status(request):

    email_id = request.session["session_key"]

    customer_object = CustomerDetail.objects.get(
        email=email_id
    )

    paylist = Payment.objects.filter(
        customer=customer_object
    )

    context = {
        "p_key": paylist
    }

    return render(
        request,
        "customer/mybooking_status.html",
        context
    )


# =========================================================
# ALL BOOKINGS
# =========================================================

def all_bookings(request):

    paylist = Payment.objects.all()

    context = {
        "p_key": paylist
    }

    return render(
        request,
        "manager/all_booking.html",
        context
    )


# =========================================================
# EDIT PROFILE
# =========================================================

def edit_profile(request):

    email_id = request.session["session_key"]

    customer_object = CustomerDetail.objects.get(
        email=email_id
    )

    if request.method == "GET":

        context = {
            "customer_key": customer_object
        }

        return render(
            request,
            "customer/edit_profile.html",
            context
        )

    if request.method == "POST":

        nm = request.POST["name"]
        ph = request.POST["phone"]

        # Update profile picture if uploaded

        if "profile_pic" in request.FILES:

            customer_object.profile_pic = (
                request.FILES.get("profile_pic")
            )

        # Update name and phone

        customer_object.name = nm
        customer_object.phone = ph

        customer_object.save()

        messages.success(
            request,
            "Profile updated successfully 👍👍"
        )

        return redirect("homepage")


# =========================================================
# FAQ
# =========================================================

def faq(request):

    return render(
        request,
        "html/faq.html"
    )
