from main import app
import unittest

class FlaskTest(unittest.TestCase):
    def text_show_code(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertEqual(response.status_code,401)

    def text_show_content(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertTrue(b'Best Training' in response.data)

    def text_show_login_content(self):
        tester=app.test_client(self)
        response=tester.get('login',content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    def text_show_login_correct(self):
        tester=app.test_client(self)
        response=tester.post('login',data=dict(email="yongyee373@gmail.com",password="123456789"),
                             follow_redirects=True)
        self.assertIn(b'Successful Login',response.data)

    def text_show_login_incorrect(self):
        tester=app.test_client(self)
        response=tester.post('login',data=dict(email="error",password="error"),
                             follow_redirects=True)
        self.assertIn(b'Login',response.data)

    def text_show_signup_content(self):
        tester = app.test_client(self)
        response = tester.get('sign-up', content_type='html/text')
        self.assertTrue(b'Sign Up' in response.data)

    def text_show_signup_correct(self):
        tester=app.test_client(self)
        response=tester.post('sign-up',data=dict(email="yongyee@gmail.com",name="chunyee518",phone="012-22211222",password1="123456789",password2="123456789"),
                             follow_redirects=True)
        self.assertIn(b'Successful Sign Up',response.data)

    def text_show_signup_incorrect(self):
        tester=app.test_client(self)
        response=tester.post('sign-up',data=dict(email="yongyee373@gmail.com",name="chunyee518",phone="012-22211222",password1="123456789",password2="123456789"),
                             follow_redirects=True)
        self.assertIn(b'Sign Up',response.data)

    def text_show_home_content(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertTrue(b'Are you ready' in response.data)

    def text_show_home_content2(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertTrue(b'Best Training' in response.data)

    def text_show_home_content3(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertTrue(b'Join Our Membership Today' in response.data)

    def text_show_home_content4(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertTrue(b'Workout Gallery' in response.data)

    def text_show_home_content5(self):
        tester=app.test_client(self)
        response=tester.get('home',content_type='html/text')
        self.assertTrue(b'Send Message' in response.data)

if __name__=='__main__':
    unittest.main()