"""This module contains the custom OIDC authentication backend for the Tally app."""

from django.conf import settings
from django.db.models import Q
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from transactions.models import Customer


class CustomerOIDCAB(OIDCAuthenticationBackend):
    """This class handles the authentication, it overwrites some mehtods from the library."""

    def get_username(self, claims):
        """Specify the username to use for the user. This is the sub from the OIDC claims."""

        return self.get_sub(claims)

    def get_email(self, claims):
        """Return the email address from the OIDC claims."""

        return claims.get("email")

    def get_groups(self, claims):
        """Return the groups from the OIDC claims. Adds ldap_groups and google_groups together."""

        ldap_groups = claims.get("ldap_groups", [])
        google_groups = claims.get("google_groups", [])
        groups = ldap_groups + google_groups
        return groups

    def get_netid(self, claims):
        """Return the netid from the OIDC claims."""

        return claims.get("netid")

    def get_sub(self, claims):
        """Return the sub from the OIDC claims."""

        return claims.get("sub")

    def filter_users_by_claims(self, claims):
        """Return the user(s) with the given claims. If no user is found, return an empty queryset."""

        sub = self.get_sub(claims)
        nedid = self.get_netid(claims)

        try:
            if sub and nedid:
                customer = Customer.objects.get(Q(sub=sub) | Q(netid=nedid))
            elif sub:
                customer = Customer.objects.get(sub=sub)
            elif nedid:
                customer = Customer.objects.get(netid=nedid)
            else:
                raise Customer.DoesNotExist

            if customer.user:
                return [customer.user]
            else:
                return self.UserModel.objects.none()

        except Customer.DoesNotExist:
            return self.UserModel.objects.none()

    def create_user(self, claims):
        """
        Create a user based on the OIDC claims. Overwrites the current values.
        Only creates a user if a customer with the sub/netid exists to make sure they registered with a SEPA.
        """

        # check if customer with sub already exists if not stop creation
        # This is because the treasurer has to create the customer first to set the relation code
        sub = self.get_sub(claims)
        netid = self.get_netid(claims)
        if not sub and not netid:
            self.append_error_to_session(
                "No sub or netid in claims found. Please contact the board."
            )
            return self.UserModel.objects.none()

        # check if customer with sub/netid already exists, if so, stop creation
        if not Customer.objects.filter(Q(sub=sub) | Q(netid=netid)).exists():
            self.append_error_to_session(
                "No user with this sub/netid found. If you haven't registered yet, please contact the board."
            )
            return self.UserModel.objects.none()

        customer = Customer.objects.filter(Q(sub=sub) | Q(netid=netid))
        if customer.count() > 1:
            self.append_error_to_session(
                "Multiple users with the same sub/netid found. Please contact the board."
            )
            return self.UserModel.objects.none()
        customer = customer.first()

        user = super().create_user(claims)
        self.set_attributes(user, claims)
        user.save()

        customer.user = user
        customer.netid = netid
        customer.sub = sub
        customer.save()

        return user

    def update_user(self, user, claims):
        """Update a user based on the OIDC claims. Overwrites the current values."""
        self.set_attributes(user, claims)
        user.save()
        return user

    def set_attributes(self, user, claims):
        """Set the user's attributes based on the OIDC claims. Overwrites the current values."""
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")

        user.is_active = True
        is_admin = settings.OIDC_TALLY_ADMIN_GROUP in self.get_groups(claims)
        user.is_staff = is_admin
        user.is_superuser = is_admin

        user.set_unusable_password()

    def append_error_to_session(self, error):
        """Append an error to the session. These are shown to the user on the login failure page."""
        if self.request:
            if "authentication_errors" not in self.request.session:
                self.request.session["authentication_errors"] = [error]
            else:
                self.request.session["authentication_errors"].append(error)
