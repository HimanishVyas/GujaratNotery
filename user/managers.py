from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        business_name,
        first_name,
        last_name,
        email,
        password,
        user_role,
        username=None,
        other_email=None,
        profile_img=None,
        user_phone=None,
        notery_reg_number=None,
        estamp_number=None,
        office_address=None,
        user_reg_status=None,
        country=None,
        state=None,
        district=None,
        *args,
        **kwargs
    ):
        if not email:
            raise ValueError("User must have an email address")
        if super().get_queryset().filter(email=self.normalize_email(email), user_phone=user_phone):
            raise ValueError("User with this email address already exists")
        user = self.model(
            business_name=business_name,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
            user_role=user_role,
            username=username,
            other_email=other_email,
            profile_img=profile_img,
            user_phone=user_phone,
            notery_reg_number=notery_reg_number,
            estamp_number=estamp_number,
            office_address=office_address,
            user_reg_status=user_reg_status,
            country=country,
            state=state,
            district=district            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        business_name,
        first_name,
        last_name,
        email,
        password,
        user_role,
        username=None,
        other_email=None,
        profile_img=None,
        user_phone=None,
        notery_reg_number=None,
        estamp_number=None,
        office_address=None,
        user_reg_status=None,
        country=None,
        state=None,
        district=None,
    ):
        user = self.create_user(
            business_name=business_name,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
            user_role=user_role,
            username=username,
            other_email=other_email,
            profile_img=profile_img,
            user_phone=user_phone,
            notery_reg_number=notery_reg_number,
            estamp_number=estamp_number,
            office_address=office_address,
            user_reg_status=user_reg_status,
            country=country,
            state=state,
            district=district
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.model.objects.create_user(**kwargs)
