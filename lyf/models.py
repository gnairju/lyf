# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminpanelCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(db_column='Name', unique=True, max_length=50)  # Field name made lowercase.
    description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'adminPanel_categories'


class AdminpanelCategoryoffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.ForeignKey(AdminpanelCategories, models.DO_NOTHING)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'adminPanel_categoryoffer'


class AdminpanelCoupons(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    created = models.DateTimeField()
    is_active = models.BooleanField()
    num = models.BigIntegerField()
    coupon_type = models.CharField(max_length=30)
    discount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'adminPanel_coupons'


class AdminpanelMultipleimage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey('AdminpanelProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'adminPanel_multipleimage'


class AdminpanelProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category = models.ForeignKey(AdminpanelCategories, models.DO_NOTHING)
    user = models.ForeignKey('UserCustomuser', models.DO_NOTHING)
    image = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField()
    pincodepro = models.CharField(db_column='pincodePro', max_length=20)  # Field name made lowercase.
    security = models.IntegerField()
    address = models.CharField(max_length=50)
    availability = models.BooleanField()
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    rentable = models.BooleanField()
    discounted_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'adminPanel_product'


class AdminpanelProductoffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    product = models.ForeignKey(AdminpanelProduct, models.DO_NOTHING)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'adminPanel_productoffer'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CartCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    days_needed = models.IntegerField()
    product = models.ForeignKey(AdminpanelProduct, models.DO_NOTHING)
    user = models.ForeignKey('UserCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_cart'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UserCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class OrderOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    address = models.ForeignKey('UserUseraddress', models.DO_NOTHING)
    user = models.ForeignKey('UserCustomuser', models.DO_NOTHING)
    days_needed = models.IntegerField()
    product = models.ForeignKey(AdminpanelProduct, models.DO_NOTHING)
    quantity = models.IntegerField()
    is_active = models.BooleanField()
    total_price = models.BigIntegerField()
    payment = models.BooleanField()
    status = models.CharField(max_length=20)
    ret_date = models.DateField()
    del_date = models.DateField()
    total_charges = models.BigIntegerField()
    platform_charges = models.BigIntegerField()
    caution_deposit = models.BigIntegerField()
    delivery_charge = models.BigIntegerField()
    coupon = models.OneToOneField(AdminpanelCoupons, models.DO_NOTHING, blank=True, null=True)
    offer_delivery_charge = models.BigIntegerField()
    offer_total_charges = models.BigIntegerField()
    offer_total_price = models.BigIntegerField()
    offer_caution_deposit = models.BigIntegerField()
    payment_provider = models.BooleanField()
    cancelled_rental = models.BooleanField()
    payment_choice = models.CharField(max_length=20)
    distance = models.FloatField()

    class Meta:
        managed = False
        db_table = 'order_order'


class PaymentsUserWallet(models.Model):
    id = models.BigAutoField(primary_key=True)
    balance_amount = models.BigIntegerField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('UserCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'payments_user_wallet'


class PaypalIpn(models.Model):
    id = models.BigAutoField(primary_key=True)
    business = models.CharField(max_length=127)
    charset = models.CharField(max_length=255)
    custom = models.CharField(max_length=256)
    notify_version = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    parent_txn_id = models.CharField(max_length=19)
    receiver_email = models.CharField(max_length=254)
    receiver_id = models.CharField(max_length=255)
    residence_country = models.CharField(max_length=2)
    test_ipn = models.BooleanField()
    txn_id = models.CharField(max_length=255)
    txn_type = models.CharField(max_length=255)
    verify_sign = models.CharField(max_length=255)
    address_country = models.CharField(max_length=64)
    address_city = models.CharField(max_length=40)
    address_country_code = models.CharField(max_length=64)
    address_name = models.CharField(max_length=128)
    address_state = models.CharField(max_length=40)
    address_status = models.CharField(max_length=255)
    address_street = models.CharField(max_length=200)
    address_zip = models.CharField(max_length=20)
    contact_phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    payer_business_name = models.CharField(max_length=127)
    payer_email = models.CharField(max_length=127)
    payer_id = models.CharField(max_length=13)
    auth_amount = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    auth_exp = models.CharField(max_length=28)
    auth_id = models.CharField(max_length=19)
    auth_status = models.CharField(max_length=255)
    exchange_rate = models.DecimalField(max_digits=64, decimal_places=16, blank=True, null=True)
    invoice = models.CharField(max_length=127)
    item_name = models.CharField(max_length=127)
    item_number = models.CharField(max_length=127)
    mc_currency = models.CharField(max_length=32)
    mc_fee = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mc_gross = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mc_handling = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mc_shipping = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    memo = models.CharField(max_length=255)
    num_cart_items = models.IntegerField(blank=True, null=True)
    option_name1 = models.CharField(max_length=64)
    option_name2 = models.CharField(max_length=64)
    payer_status = models.CharField(max_length=255)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_gross = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    pending_reason = models.CharField(max_length=255)
    protection_eligibility = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    reason_code = models.CharField(max_length=255)
    remaining_settle = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    settle_amount = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    settle_currency = models.CharField(max_length=32)
    shipping = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    shipping_method = models.CharField(max_length=255)
    tax = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    transaction_entity = models.CharField(max_length=255)
    auction_buyer_id = models.CharField(max_length=64)
    auction_closing_date = models.DateTimeField(blank=True, null=True)
    auction_multi_item = models.IntegerField(blank=True, null=True)
    for_auction = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    amount_per_cycle = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    initial_payment_amount = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    next_payment_date = models.DateTimeField(blank=True, null=True)
    outstanding_balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    payment_cycle = models.CharField(max_length=255)
    period_type = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    profile_status = models.CharField(max_length=255)
    recurring_payment_id = models.CharField(max_length=255)
    rp_invoice_id = models.CharField(max_length=127)
    time_created = models.DateTimeField(blank=True, null=True)
    amount1 = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    amount2 = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    amount3 = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mc_amount1 = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mc_amount2 = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mc_amount3 = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    password = models.CharField(max_length=24)
    period1 = models.CharField(max_length=255)
    period2 = models.CharField(max_length=255)
    period3 = models.CharField(max_length=255)
    reattempt = models.CharField(max_length=1)
    recur_times = models.IntegerField(blank=True, null=True)
    recurring = models.CharField(max_length=1)
    retry_at = models.DateTimeField(blank=True, null=True)
    subscr_date = models.DateTimeField(blank=True, null=True)
    subscr_effective = models.DateTimeField(blank=True, null=True)
    subscr_id = models.CharField(max_length=19)
    username = models.CharField(max_length=64)
    case_creation_date = models.DateTimeField(blank=True, null=True)
    case_id = models.CharField(max_length=255)
    case_type = models.CharField(max_length=255)
    receipt_id = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=32)
    handling_amount = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    transaction_subject = models.CharField(max_length=256)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)
    flag = models.BooleanField()
    flag_code = models.CharField(max_length=16)
    flag_info = models.TextField()
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    from_view = models.CharField(max_length=6, blank=True, null=True)
    mp_id = models.CharField(max_length=128, blank=True, null=True)
    option_selection1 = models.CharField(max_length=200)
    option_selection2 = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'paypal_ipn'


class ProviderProviderCredentials(models.Model):
    id = models.BigAutoField(primary_key=True)
    pan_card = models.CharField(max_length=35)
    pan_photo = models.CharField(max_length=100, blank=True, null=True)
    paypal_id = models.CharField(max_length=254)
    provider = models.ForeignKey('UserCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'provider_provider_credentials'


class UserCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    email = models.CharField(unique=True, max_length=254)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    is_staff = models.BooleanField()
    is_super = models.BooleanField()
    referral_code = models.CharField(unique=True, max_length=10, blank=True, null=True)
    referrer = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_customuser'


class UserCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UserCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UserCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UserCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class UserUseraddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    user = models.ForeignKey(UserCustomuser, models.DO_NOTHING)
    addresstype = models.CharField(db_column='addressType', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_useraddress'
