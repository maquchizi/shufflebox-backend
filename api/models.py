from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Brownbag(models.Model):
    """Class definition for the BrownBag model."""

    # Helper callable model variables
    NEXT_IN_LINE = "next_in_line"
    DONE = "done"
    NOT_DONE = "not_done"

    brownbag_choices = (
        (NEXT_IN_LINE, "Next In Line"),
        (DONE, "Done"),
        (NOT_DONE, "Not Done")
    )

    date = models.DateField(unique=True)
    status = models.CharField(
        max_length=12, choices=brownbag_choices, default=NOT_DONE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model instance."""
        return "{} Status: {}".format(self.user, self.status)


class Profile(models.Model):
    """Class definition for the User Profile model.

    Extends default django User model that stores username, email, pword etc
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(default="", max_length=500, blank=True)

    def __unicode__(self):
        return u'User Profile for: {}'.format(self.user.username)

    def __str__(self):
        """Return a string representation of the model instance."""
        return "{}".format(self.user.username)


class Hangout(models.Model):
    """Class definition for the Hangout model."""
    date = models.DateField(unique=True)

    def __str__(self):
        """Return a string representation of the model instance."""
        return str(self.date)


class Group(models.Model):
    """Class definition for the Group model."""
    members = models.ManyToManyField(User, related_name="group")
    hangout = models.ForeignKey(
        Hangout, on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        """Return a string representation of the model instance."""
        return "{}".format(self.pk)


class SecretSanta(models.Model):
    """Class definition for the Secret santa model."""
    date = models.DateField()
    santa = models.ForeignKey(
        User, related_name="santa", on_delete=models.CASCADE)
    giftee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model instance."""
        return "Santa: {}, Giftee: {}".format(self.santa, self.giftee)


# Decorator to pass in a post_save signal
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to create a user profile when a User instance is created."""

    if created:
        Profile.objects.create(user=instance)


# Decorator to pass in a post_save signal
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal to update a user profile when a User instance is updated."""
    instance.profile.save()
