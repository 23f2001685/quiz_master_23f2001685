from datetime import datetime, timedelta
from flask_mail import Mail, Message
from sqlalchemy import func
import io
import csv

from application.models import User, Quiz, QuizAttempt, Subject, Chapter
from application.database import db

# Import celery instance
from celery_config import celery_app, flask_app

@celery_app.task
def send_daily_quiz_reminders():
    """Send daily quiz reminders to users about upcoming quizzes."""
    try:
        print("[INFO] Starting daily quiz reminders task")

        # Get quizzes scheduled for today and tomorrow
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        upcoming_quizzes = Quiz.query.filter(
            func.date(Quiz.date_of_quiz).between(today, tomorrow),
            Quiz.is_active == True
        ).all()

        if not upcoming_quizzes:
            print("[INFO] No upcoming quizzes found for reminders")
            return "No upcoming quizzes"

        # Get all active users
        users = User.query.filter_by(active=True).all()

        reminder_count = 0
        for user in users:
            try:
                # Send email reminder
                send_quiz_reminder_email.delay(user.id, [quiz.id for quiz in upcoming_quizzes])
                reminder_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to send reminder to user {user.id}: {str(e)}")

        print(f"[INFO] Sent {reminder_count} quiz reminders")
        return f"Sent {reminder_count} quiz reminders"

    except Exception as e:
        print(f"[ERROR] Error in send_daily_quiz_reminders: {str(e)}")
        return f"Error: {str(e)}"

@celery_app.task
def send_quiz_reminder_email(user_id, quiz_ids):
    """Send quiz reminder email to a specific user."""
    try:
        print(f"[INFO] Sending quiz reminder email to user {user_id}")

        user = User.query.get(user_id)
        if not user:
            return f"User {user_id} not found"

        quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()

        mail = Mail(flask_app)

        # Create email content
        quiz_list = ""
        for quiz in quizzes:
            quiz_list += f"""
            <li>
                <strong>{quiz.title}</strong><br>
                Subject: {quiz.chapter.subject.name}<br>
                Chapter: {quiz.chapter.name}<br>
                Date: {quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M')}<br>
                Duration: {quiz.time_duration} minutes
            </li><br>
            """

        html_body = f"""
        <html>
        <body>
            <h2>Quiz Reminder</h2>
            <p>Hello {user.full_name},</p>
            <p>This is a friendly reminder about the following upcoming quizzes:</p>
            <ul>
                {quiz_list}
            </ul>
            <p>Don't forget to prepare and participate!</p>
            <p>Best regards,<br>Quiz Master Team</p>
        </body>
        </html>
        """

        msg = Message(
            subject="Quiz Reminder - Upcoming Quizzes",
            recipients=[user.email],
            html=html_body
        )

        mail.send(msg)
        print(f"[INFO] Quiz reminder sent to {user.email}")
        return f"Reminder sent to {user.email}"

    except Exception as e:
        print(f"[ERROR] Error sending quiz reminder email: {str(e)}")
        return f"Error: {str(e)}"

@celery_app.task
def send_monthly_performance_reports():
    """Send monthly performance reports to all users."""
    try:
        print("[INFO] Starting monthly performance reports task")

        # Get all active users
        users = User.query.filter_by(active=True).all()

        report_count = 0
        for user in users:
            try:
                # Generate and send performance report
                send_performance_report_email.delay(user.id)
                report_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to send performance report to user {user.id}: {str(e)}")

        print(f"[INFO] Sent {report_count} performance reports")
        return f"Sent {report_count} performance reports"

    except Exception as e:
        print(f"[ERROR] Error in send_monthly_performance_reports: {str(e)}")
        return f"Error: {str(e)}"

@celery_app.task
def send_performance_report_email(user_id):
    """Generate and send performance report email to a specific user."""
    try:
        print(f"[INFO] Generating performance report for user {user_id}")

        user = User.query.get(user_id)
        if not user:
            return f"User {user_id} not found"

        # Get user's quiz attempts from last month
        last_month = datetime.now() - timedelta(days=30)
        attempts = QuizAttempt.query.filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.timestamp >= last_month
        ).join(Quiz).join(Chapter).join(Subject).all()

        if not attempts:
            # Send "no activity" email
            html_body = f"""
            <html>
            <body>
                <h2>Monthly Performance Report</h2>
                <p>Hello {user.full_name},</p>
                <p>We haven't seen you taking any quizzes in the last month.</p>
                <p>Why not give it a try? Check out our latest quizzes!</p>
                <p>Best regards,<br>Quiz Master Team</p>
            </body>
            </html>
            """
        else:
            # Calculate statistics
            total_attempts = len(attempts)
            total_score = sum(attempt.total_score for attempt in attempts)
            max_possible_score = sum(attempt.max_score for attempt in attempts)
            average_percentage = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0

            # Subject-wise performance
            subject_stats = {}
            for attempt in attempts:
                subject = attempt.quiz.chapter.subject.name
                if subject not in subject_stats:
                    subject_stats[subject] = {
                        'attempts': 0,
                        'total_score': 0,
                        'max_score': 0
                    }
                subject_stats[subject]['attempts'] += 1
                subject_stats[subject]['total_score'] += attempt.total_score
                subject_stats[subject]['max_score'] += attempt.max_score

            subject_performance = ""
            for subject, stats in subject_stats.items():
                percentage = (stats['total_score'] / stats['max_score'] * 100) if stats['max_score'] > 0 else 0
                subject_performance += f"""
                <tr>
                    <td>{subject}</td>
                    <td>{stats['attempts']}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
                """

            html_body = f"""
            <html>
            <body>
                <h2>Monthly Performance Report</h2>
                <p>Hello {user.full_name},</p>
                <p>Here's your performance summary for the last month:</p>

                <h3>Overall Statistics</h3>
                <ul>
                    <li>Total Quizzes Attempted: {total_attempts}</li>
                    <li>Average Score: {average_percentage:.1f}%</li>
                    <li>Total Points: {total_score}/{max_possible_score}</li>
                </ul>

                <h3>Subject-wise Performance</h3>
                <table border="1" style="border-collapse: collapse; width: 100%;">
                    <tr>
                        <th>Subject</th>
                        <th>Attempts</th>
                        <th>Average Score</th>
                    </tr>
                    {subject_performance}
                </table>

                <p>Keep up the great work!</p>
                <p>Best regards,<br>Quiz Master Team</p>
            </body>
            </html>
            """

        mail = Mail(flask_app)
        msg = Message(
            subject="Monthly Performance Report",
            recipients=[user.email],
            html=html_body
        )

        mail.send(msg)
        print(f"[INFO] Performance report sent to {user.email}")
        return f"Performance report sent to {user.email}"

    except Exception as e:
        print(f"[ERROR] Error sending performance report: {str(e)}")
        return f"Error: {str(e)}"

@celery_app.task
def export_user_attempts_csv(user_id):
    """
    Fetches all quiz attempts for a user, generates a CSV,
    and emails it to them.
    """
    with flask_app.app_context():
        try:
            user = User.query.get(user_id)
            if not user:
                print(f"[ERROR] User with ID {user_id} not found for CSV export.")
                return

            attempts = db.session.query(QuizAttempt).filter_by(user_id=user_id).join(Quiz).order_by(QuizAttempt.timestamp.desc()).all()

            if not attempts:
                # Optionally, send an email notifying the user they have no attempts.
                print(f"[INFO] No quiz attempts found for user {user.email} to export.")
                return

            # Create CSV in-memory
            output = io.StringIO()
            writer = csv.writer(output)

            # Write header
            header = [
                'Quiz Title', 'Subject', 'Chapter', 'Date Attempted',
                'Score', 'Max Score', 'Percentage', 'Quiz Remarks'
            ]
            writer.writerow(header)

            # Write data rows
            for attempt in attempts:
                row = [
                    attempt.quiz.title,
                    attempt.quiz.chapter.subject.name,
                    attempt.quiz.chapter.name,
                    attempt.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    attempt.total_score,
                    attempt.max_score,
                    f"{attempt.percentage:.2f}%",
                    attempt.quiz.remarks
                ]
                writer.writerow(row)

            csv_data = output.getvalue()
            output.close()

            # Send email with CSV attachment
            mail = Mail(flask_app)
            msg = Message(
                subject="Your Quiz Attempts Export",
                recipients=[user.email],
                body="Please find your quiz attempts history attached.",
                html="<p>Hello,</p><p>Please find your quiz attempts history attached in the CSV file.</p>"
            )
            msg.attach(
                "quiz_attempts.csv",
                "text/csv",
                csv_data
            )
            mail.send(msg)
            print(f"[INFO] Successfully sent quiz attempts CSV to {user.email}")

        except Exception as e:
            print(f"[ERROR] Failed to export CSV for user {user_id}: {str(e)}")
        return f"Exported quiz attempts for user {user.email} to CSV"
