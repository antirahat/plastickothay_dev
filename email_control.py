from django.core.mail import send_mail, EmailMessage
from plastickothay.models import Post

def test_email() :
    send_mail(
        'Subject here',
        'Here is the message.',
        'contact.plastickothay@gmail.com',
        ['phylosopherhossain2022@gmail.com'],
        fail_silently=False,
    )

def test_html_email():
    html_content = """
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2c3e50;">Hello from Django!</h2>
                <p style="font-size: 16px; color: #555555;">
                    This is a test HTML email sent from your Django project.
                </p>
                <p style="font-size: 14px; color: #888888;">
                    <em>Sent on: {{ current_date }}</em>
                </p>
                <hr />
                <p style="font-size: 12px; color: #aaaaaa;">© 2025 Your Company Name</p>
            </div>
        </body>
    </html>
    """

    email = EmailMessage(
        subject='📬 Django HTML Email Test',
        body=html_content,
        from_email='contact.plastickothay@gmail.com',
        to=['phylosopherhossain2022@gmail.com'],
    )
    email.content_subtype = 'html'  # Specify that the body is HTML

    # Optional: attach a file
    # email.attach_file('/path/to/file.pdf')

    email.send()

def post_mail(post: Post) :
    subject = "🌟 Thank You for Making a Difference with Plastickothay"
    body = f"Hi {post.name},\n\nThank you for reporting plastic on Plastickothay! Your contribution helps us track and combat plastic pollution more effectively. Every report brings us one step closer to cleaner communities. Stay tuned for updates on how your input is making an impact.\n\nTogether, we can create a plastic-free future.\n\nWarm regards,\nThe Plastickothay Team"
    
    try :
        send_mail(
            subject,
            body,
            'contact.plastickothay@gmail.com',
            [post.email],
            fail_silently=False,
        )
        return True
    except :
        return False