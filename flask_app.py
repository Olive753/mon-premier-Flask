from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'xxxxx'
app.config['MAIL_PASSWORD'] = 'xxxxx'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

        @app.route('/contact', methods=['POST'])
        def process_contact_form():
            name = request.form['name']
                email = request.form['email']
                    message = request.form['message']

                        send_email('Nouveau message de contact', 'your email', ['your email'], f'Nom: {name}\nAdresse e-mail: {email}\nMessage: {message}', f'<p><strong>Nom:</strong> {name}</p><p><strong>Adresse e-mail:</strong> {email}</p><p><strong>Message:</strong></p><p>{message}</p>')
                            flash(('success', 'Votre message a été envoyé avec succès!'))
                                return redirect(url_for('contact'))

                                def send_email(subject, sender, recipients, text_body, html_body):
                                    msg = Message(subject, sender=sender, recipients=recipients)
                                        msg.body = text_body
                                            msg.html = html_body
                                                mail.send(msg)

                                                @app.errorhandler(500)
                                                def internal_server_error(e):
                                                    return 'Internal Server Error', 500

                                                    if __name__ == '__main__':
                                                        app.run(debug=True)
