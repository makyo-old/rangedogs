from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique = True, editable = False)
    location = models.CharField(max_length = 60, blank = True)
    interests = models.TextField(blank = True)
    about = models.TextField(blank = True)

    def get_absolute_url(self):
        return "/user/%s/" % self.user.username

    def __unicode__(self):
        return "<a class=\"userlink\" href=\"/user/%(username)s/\"><img src=\"%(mediaurl)susericon.gif\" alt=\"Rangedogs User\" />%(username)s</a>" % {
                'mediaurl': settings.MEDIA_URL,
                'username': self.user.username }

class Gun(models.Model):
    GUN_TYPES = (
            ('Rifles', (
                ('A', 'Single-shot rifle: falling block'),
                ('B', 'Single-shot rifle: rolling block'),
                ('C', 'Single-shot rifle: break action'),
                ('D', 'Single-shot rifle: bolt action'),
                ('E', 'Single-shot rifle: other'),
                ('F', 'Repeating rifle: bolt action'),
                ('G', 'Repeating rifle: lever action'),
                ('H', 'Autoloading rifle: box magazine/rotating bolt'),
                ('I', 'Autoloading rifle: tubular magazine'),
                ('J', 'Muzzle-loading rifle: matchlock'),
                ('K', 'Muzzle-loading rifle: wheellock'),
                ('L', 'Muzzle-loading rifle: flintlock'),
                ('M', 'Muzzle-loading rifle: percussion cap')
                )
            ),
            ('Handguns', (
                ('N', 'Revolver: single-action'),
                ('O', 'Revolver: double-action'),
                ('P', 'Autoloading pistol: single-action'),
                ('Q', 'autoloading pistol: double-action/single-action'),
                ('R', 'autoloading pistol: double-action only'),
                ('S', 'Single-shot handgun'),
                ('T', 'Muzzle-loading handgun: revolver'),
                ('U', 'Muzzle-loading handgun: single-shot')
                )
            ),
            ('Shotguns', (
                ('V', 'Shotgun: single-shot'),
                ('W', 'Shotgun: double-shot, over/under'),
                ('X', 'Shotgun: double-shot, side-by-side'),
                ('Y', 'Shotgun: pump-action'),
                ('Z', 'Shotgun: autoloading')
                )
            ),
            ('Other', (
                ('1', 'Rifle: other'),
                ('2', 'Handgun: other'),
                ('3', 'Shotgun: other')
                )
            )
    )

    owner = models.ForeignKey(User)
    make = models.CharField(max_length = 120)
    model = models.CharField(max_length = 120)
    type = models.CharField(max_length = 1, choices = GUN_TYPES)
    serial_number = models.CharField(max_length = 120, blank = True)
    caliber = models.ForeignKey('Caliber')
    barrel_length = models.IntegerField(null = True)
    twist_rate = models.CharField(max_length = 40, blank = True)
    source = models.CharField(max_length = 120, blank = True)
    rounds_fired = models.IntegerField(null = True)
    cost = models.DecimalField(max_digits = 8, decimal_places = 2, null = True)
    value = models.DecimalField(max_digits = 8, decimal_places = 2, null = True)
    accessories = models.TextField(blank = True)
    notes = models.TextField(blank = True)
    
    def get_absolute_url(self):
        return "/gun/%s/" % str(self.id)

    def __unicode__(self):
        return "<img src=\"%(mediaurl)sicons/%(type)s.gif\" alt=\"%(typelong)s\" /> %(owner)s's %(make)s %(model)s in %(caliber)s" % {
                'mediaurl': settings.MEDIA_URL,
                'type': self.type,
                'typelong': self.get_type_display(),
                'owner': str(self.owner.get_profile()), 
                'make': self.make, 
                'model': self.model, 
                'caliber': self.caliber.name }

class Caliber(models.Model):
    ROUND_TYPES = (
            ('A', 'Centerfire rifle cartridge'),
            ('B', 'Centerfire handgun cartridge'),
            ('C', 'Rimfire cartridge'),
            ('D', 'Shotgun cartridge'),
            ('E', 'Muzzleloading round')
    )
    slug = models.SlugField(primary_key = True)
    name = models.CharField(max_length = 120)
    type = models.CharField(max_length = 1, choices = ROUND_TYPES)
    notes = models.TextField()
    bullet_dia = models.DecimalField(max_digits = 7, decimal_places = 5, null = True)
    max_oal = models.DecimalField(max_digits = 5, decimal_places = 3, null = True)
    min_oal = models.DecimalField(max_digits = 5, decimal_places = 3, null = True)
    max_case_length = models.DecimalField(max_digits = 5, decimal_places = 3, null = True)
    case_trim_length = models.DecimalField(max_digits = 5, decimal_places = 3, null = True)
    max_pressure = models.IntegerField(null = True)
    pressure_in_CUP = models.BooleanField(null = True)
    reloading_notes = models.TextField()

    def __unicode__(self):
        return self.name

class Handload(models.Model):
    BULLET_TYPES = (
            ('A', 'Spitzer boat-tail'),
            ('B', 'Spitzer'),
            ('C', 'Round-nose'),
            ('D', 'Flat/snub-nose'),
            ('E', 'Wad-cutter'),
            ('F', 'Shotgun shot'),
            ('G', 'Shotgun slug: rifled'),
            ('H', 'Shotgun slug: with sabot')
    )

    BULLET_JACKETS = (
            ('A', 'Full jacket (FMJ)'),
            ('B', 'Partial jacket: soft-point'),
            ('C', 'Partial jacket: plastic/ballistic tip'),
            ('D', 'Partial jacket: hollow-point (JHP)'),
            ('E', 'Gas-checked'),
            ('F', 'No jacket'),
            ('G', 'Hand-made: cast/swaged and jacketed'),
            ('H', 'Hand-made: cast/swaged and gas-checked'),
            ('I', 'Hand-made: cast/swaged and no jacket')
    )

    owner = models.ForeignKey(User, editable = False)
    caliber = models.ForeignKey('Caliber')
    gun = models.ForeignKey('Gun')
    projectile_brand_name = models.CharField(max_length = 120, blank = True)
    projectile_weight = models.IntegerField()
    projectile_type = models.CharField(max_length = 1, choices = BULLET_TYPES)
    projectile_jacket = models.CharField(max_length = 1, choices = BULLET_JACKETS, blank = True)
    projectile_shot_size = models.CharField(max_length = 5, blank = True)
    projectile_shot_material = models.CharField(max_length = 40, blank = True)
    powder_brand = models.CharField(max_length = 60)
    powder_name = models.CharField(max_length = 60)
    powder_weight = models.DecimalField(max_digits = 5, decimal_places = 2)
    pressure = models.IntegerField(null = True)
    pressure_in_CUP = models.BooleanField(null = True)
    velocity = models.DecimalField(max_digits = 5, decimal_places = 1, null = True)
    notes = models.TextField(blank = True)

class Report(models.Model):
    owner = models.ForeignKey(User, editable = False)
    ctime = models.DateTimeField(auto_now_add = True)
    mtime = models.DateTimeField(auto_now = True)
    eventdate = models.DateField()
    participants = models.TextField(blank = True)
    guns = models.ManyToManyField('GunReport')
    title = models.CharField(max_length = 500)
    conditions = models.TextField(blank = True)
    body = models.TextField()

class GunReport(models.Model):
    gun = models.ForeignKey('Gun')
    handloads = models.ManyToManyField('Handload', null = True)
    factory_ammo = models.TextField(blank = True)
    problems = models.TextField(blank = True)
    notes = models.TextField(blank = True)

class Comment(models.Model):
    owner = models.ForeignKey(User, editable = False)
    ctime = models.DateTimeField(auto_now_add = True)
    mtime = models.DateTimeField(auto_now = True)
    User_parent = models.ForeignKey(User, editable = False, related_name = 'private_message')
    Gun_parent = models.ForeignKey('Gun', editable = False)
    Handload_parent = models.ForeignKey('Handload', editable = False)
    Report_parent = models.ForeignKey('Report', editable = False)
    Comment_parent = models.ForeignKey('Comment', editable = False)
    title = models.CharField(max_length = 500)
    body = models.TextField()
