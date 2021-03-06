import os
import unittest
import tempfile
import ButterSalt


class ButterSaltTestCase(unittest.TestCase):

    testapp = ButterSalt.app.test_client()
    ButterSalt.app.config['TESTING'] = True
    ButterSalt.app.config['WTF_CSRF_ENABLED'] = False
    ButterSalt.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ButterSalt:ButterSalt@192.168.1.73/test'

    @classmethod
    def setUpClass(cls):
        ButterSalt.db.create_all()

    @classmethod
    def tearDownClass(cls):
        ButterSalt.db.drop_all()

    def signup(self, username, email, password):
        return self.testapp.post('/user/signup', data=dict(
            username=username,
            email=email,
            password0=password,
            password1=password,
        ), follow_redirects=True)

    def login(self, username, password):
        return self.testapp.post('/user/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.testapp.get('/user/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.testapp.get('/')
        assert 'Redirecting' in rv.data.decode()
        rv = self.testapp.get('/', follow_redirects=True)
        assert 'Sign up' in rv.data.decode()

    def test_login_logout_signup(self):
        rv = self.login('admin', '123456')
        assert 'Logged in successfully.' in rv.data.decode()
        rv = self.logout()
        assert 'You have been logged out.' in rv.data.decode()
        rv = self.login('adminx', 'default')
        assert 'Invalid usename or password.' in rv.data.decode()
        rv = self.login('admin', 'defaultx')
        assert 'Invalid usename or password.' in rv.data.decode()
        rv = self.signup('admin', 'admin@admin.com', '123456')
        assert 'Username already in use.' in rv.data.decode()
        assert 'Email already registered.' in rv.data.decode()

    def test_home(self):
        self.signup('admin', 'admin@admin.com', '123456')
        self.login('admin', '123456')
        rv = self.testapp.get('/', follow_redirects=True)
        assert 'id="tgt" name="tgt" type="text" value="" placeholder="Required"' in rv.data.decode()

    def test_salt_jobs(self):
        self.login('admin', '123456')
        rv = self.testapp.get('/salt/jobs/', follow_redirects=True)
        assert '<table class="table table-striped">' in rv.data.decode()

    def test_salt_minions(self):
        self.login('admin', '123456')
        rv = self.testapp.get('/salt/minions/', follow_redirects=True)
        assert '<table class="table table-striped">' in rv.data.decode()

    def test_salt_keys(self):
        self.login('admin', '123456')
        rv = self.testapp.get('/salt/keys/', follow_redirects=True)
        assert '<table class="table table-hover">' in rv.data.decode()

    def test_salt_stats(self):
        self.login('admin', '123456')
        rv = self.testapp.get('/salt/stats/', follow_redirects=True)
        assert '<table class="table table-striped">' in rv.data.decode()


if __name__ == '__main__':
    unittest.main()
