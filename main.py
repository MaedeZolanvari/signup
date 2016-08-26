import webapp2
import re
from string import letters



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        error_username = self.request.get('error_username')
        error_password = self.request.get('error_password')
        error_verify = self.request.get('error_verify')
        error_email = self.request.get('error_email')

        form = """
        <form method="post">
                    <table>
                        <tr>
                            <td><label for="username">Username</label></td>
                            <td>
                                <input name="username" type="text" value="{}" required>
                                <span class="error">{}</span>
                            </td>
                        </tr>
                        <tr>
                            <td><label for="password">Password</label></td>
                            <td>
                                <input name="password" type="password" required>
                                <span class="error">{}</span>
                            </td>
                        </tr>
                        <tr>
                            <td><label for="verify">Verify Password</label></td>
                            <td>
                                <input name="verify" type="password" required>
                                <span class="error">{}</span>
                            </td>
                        </tr>
                        <tr>
                            <td><label for="email">Email (optional)</label></td>
                            <td>
                                <input name="email" type="email" value="">
                                <span class="error">{}</span>
                            </td>
                        </tr>
                    </table>
                    <input type="submit">
                </form>
        """.format(username,error_username,error_password,error_verify,error_email)

        self.response.out.write(form)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        error_username = ""
        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error = True

        error_password = ""
        if not valid_password(password):
            error_password = "That wasn't a valid password."
            have_error = True

        error_verify = ""
        if password != verify:
            error_verify = "Your passwords didn't match."
            have_error = True

        error_email = ""
        if not valid_email(email):
            error_email = "That's not a valid email."
            have_error = True

        if have_error:
            self.redirect("/?error_username={}&error_password={}&error_verify={}&error_email={}&username={}".format(error_username,error_password,error_verify,error_email,username))
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.out.write("welcome")
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
                               ('/', Signup),
                               ('/welcome', Welcome)],
                              debug=True)
