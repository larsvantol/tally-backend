from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from transactions.models import Customer
from . import settings


class CustomerOIDCAB(OIDCAuthenticationBackend):
    def get_username(self, claims):
        return claims.get("sub")

    def get_email(self, claims):
        return claims.get("email")

    def get_groups(self, claims):
        ldap_groups = claims.get("ldap_groups", [])
        google_groups = claims.get("google_groups", [])
        groups = ldap_groups + google_groups
        return groups

    def filter_users_by_claims(self, claims):
        sub = claims.get("sub")

        if not sub:
            return self.UserModel.objects.none()

        try:
            customer = Customer.objects.get(sub=sub)
            if customer.user:
                return [customer.user]
            else:
                return self.UserModel.objects.none()

        except Customer.DoesNotExist:
            return self.UserModel.objects.none()

    def create_user(self, claims):
        # check if customer with sub already exists if not stop creation
        # This is because the treasurer has to create the customer first to set the relation code
        sub = claims.get("sub")
        if not sub:
            return self.UserModel.objects.none()
        # check if customer with sub already exists if not stop creation
        if not Customer.objects.filter(sub=sub).exists():
            return self.UserModel.objects.none()
        customer = Customer.objects.filter(sub=sub).first()

        user = super(CustomerOIDCAB, self).create_user(claims)
        self.set_attributes(user, claims)
        user.save()

        customer.user = user
        customer.save()

        return user

    def update_user(self, user, claims):
        self.set_attributes(user, claims)
        user.save()
        return user

    def set_attributes(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")

        user.is_active = True
        is_admin = settings.OIDC_TALLY_ADMIN_GROUP in self.get_groups(claims)
        user.is_staff = is_admin
        user.is_superuser = is_admin

        user.set_unusable_password()
