from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, email, username, fname, lname, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fname=fname,
            lname=lname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fname, lname, password=None):
        user = self.create_user(
            email=email,
            username=username,
            fname=fname,
            lname=lname,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
