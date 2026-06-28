"""
Email Service Module for Job Portal
Provides reusable email functionality with proper error handling and logging
"""

import logging
from typing import Dict, List, Optional, Tuple
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service class for handling email operations"""

    @staticmethod
    def send_acceptance_email(applicant, job_title: str = None) -> Tuple[bool, str]:
        """
        Send acceptance email to applicant

        Args:
            applicant: User object of the accepted applicant
            job_title: Optional job title for the email

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Prepare context for email template
            context = {
                'applicant_name': applicant.get_full_name() or applicant.username,
                'job_title': job_title or 'الوظيفة المطلوبة',
                'current_year': timezone.now().year,
            }

            # Render email templates
            html_content = render_to_string(
                'jobapp/emails/acceptance_email.html',
                context
            )
            text_content = render_to_string(
                'jobapp/emails/acceptance_email.txt',
                context
            )

            # Email details
            subject = 'تهانينا! تم قبولك في الوظيفة'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
            to_email = [applicant.email]

            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=to_email
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            # Log success
            logger.info(
                f"Acceptance email sent successfully to {applicant.email} "
                f"for applicant ID: {applicant.id}"
            )

            return True, 'تم إرسال إشعار القبول بنجاح'

        except Exception as e:
            error_msg = f'فشل في إرسال إشعار القبول: {str(e)}'
            logger.error(
                f"Failed to send acceptance email to {applicant.email}: {str(e)}",
                exc_info=True
            )
            return False, error_msg

    @staticmethod
    def send_communication_email(
        subject: str,
        message: str,
        recipient_email: str,
        sender_name: str,
        sender_email: str,
        title: str = ''
    ) -> Tuple[bool, str]:
        """
        Send communication email between users

        Args:
            subject: Email subject
            message: Email message content
            recipient_email: Recipient email address
            sender_name: Sender's full name
            sender_email: Sender's email address
            title: Optional email title

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Prepare context for email template
            context = {
                'title': title or subject,
                'message': message,
                'sender_name': sender_name,
                'sender_email': sender_email,
                'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'current_year': timezone.now().year,
            }

            # Render email templates
            html_content = render_to_string(
                'jobapp/emails/communication_email.html',
                context
            )
            text_content = render_to_string(
                'jobapp/emails/communication_email.txt',
                context
            )

            # Email details
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
            to_email = [recipient_email]

            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=to_email
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            # Log success
            logger.info(
                f"Communication email sent successfully from {sender_email} "
                f"to {recipient_email}"
            )

            return True, 'تم إرسال الرسالة بنجاح'

        except Exception as e:
            error_msg = f'فشل في إرسال الرسالة: {str(e)}'
            logger.error(
                f"Failed to send communication email from {sender_email} "
                f"to {recipient_email}: {str(e)}",
                exc_info=True
            )
            return False, error_msg

    @staticmethod
    def validate_email_address(email: str) -> Tuple[bool, str]:
        """
        Validate email address format

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        import re

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not email:
            return False, 'البريد الإلكتروني مطلوب'

        if not re.match(email_pattern, email):
            return False, 'صيغة البريد الإلكتروني غير صحيحة'

        return True, 'البريد الإلكتروني صحيح'


# Convenience functions for backward compatibility
def send_acceptance_email(applicant, job_title: str = None) -> Tuple[bool, str]:
    """Convenience function to send acceptance email"""
    return EmailService.send_acceptance_email(applicant, job_title)


def send_communication_email(
    subject: str,
    message: str,
    recipient_email: str,
    sender_name: str,
    sender_email: str,
    title: str = ''
) -> Tuple[bool, str]:
    """Convenience function to send communication email"""
    return EmailService.send_communication_email(
        subject, message, recipient_email, sender_name, sender_email, title
    )
