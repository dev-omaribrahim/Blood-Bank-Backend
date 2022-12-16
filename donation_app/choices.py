# Donation Type Choices
INSIDE_DONATION = "inside_donation"
OUTSIDE_DONATION = "outside_donation"
REPLACE_DONATION = "replace_donation"

# Unit Type Choices
FULL_BLOOD = "full_blood"
RBCs = "rbcs"
PLASMA = "plasma"
BLOOD_PLATELETS = "blood_platelets"
CRYO = "cryo"

# Blood Type Choices
A_POSITIVE = "a_positive"
A_MINUS = "a_minus"
B_POSITIVE = "b_positive"
B_MINUS = "b_minus"
O_POSITIVE = "o_positive"
O_MINUS = "o_minus"
AB_POSITIVE = "ab_positive"
AB_MINUS = "ab_minus"
A_GROUP = "a_group"
B_GROUP = "b_group"
O_GROUP = "o_group"
AB_GROUP = "ab_group"


# Donor Blood Type
DONOR_A_POSITIVE = "a_positive"
DONOR_A_MINUS = "a_minus"
DONOR_B_POSITIVE = "b_positive"
DONOR_B_MINUS = "b_minus"
DONOR_O_POSITIVE = "o_positive"
DONOR_O_MINUS = "o_minus"
DONOR_AB_POSITIVE = "ab_positive"
DONOR_AB_MINUS = "ab_minus"

# Unit Notes
PLACE_HOLDER_1 = "place_holder1"
PLACE_HOLDER_2 = "place_holder2"

# Exchange Status
AVAILABLE_FOR_EXCHANGE = "available_for_exchange"
NOT_AVAILABLE_FOR_EXCHANGE = "not_available_for_exchange"
EXECUTED = "executed"

# Gender Choices
MALE = "male"
FEMALE = "female"

# Analyse Status Choices
FREE = "free"
DAMAGED = "damaged"
PENDING = "pending"

# Operation Type Choices
IMPORT = "import"
EXPORT = "export"

# Expiration Scope Choices
SCOPE_35 = 35
SCOPE_42 = 42
SCOPE_180 = 180
SCOPE_365 = 365
SCOPE_5 = 5


DONATION_TYPE_CHOICES = (
    (INSIDE_DONATION, "تبرع داخلى"),
    (OUTSIDE_DONATION, "تبرع خارجى"),
    (REPLACE_DONATION, "تبرع إستبدال"),
)


UNIT_TYPE_CHOICES = (
    (FULL_BLOOD, "كيس دم كامل"),
    (RBCs, "RPCs"),
    (PLASMA, "بلازما"),
    (BLOOD_PLATELETS, "صفائح دموية"),
    (CRYO, "cryo"),
)


BLOOD_TYPE_CHOICES = (
    (A_POSITIVE, "A+"),
    (A_MINUS, "A-"),
    (B_POSITIVE, "B+"),
    (B_MINUS, "B-"),
    (O_POSITIVE, "O+"),
    (O_MINUS, "O-"),
    (AB_POSITIVE, "AB+"),
    (AB_MINUS, "AB-"),
    (A_GROUP, "A"),
    (B_GROUP, "B"),
    (O_GROUP, "O"),
    (AB_GROUP, "AB"),
)


DONOR_BLOOD_TYPE_CHOICES = (
    (DONOR_A_POSITIVE, "A+"),
    (DONOR_A_MINUS, "A-"),
    (DONOR_B_POSITIVE, "B+"),
    (DONOR_B_MINUS, "B-"),
    (DONOR_O_POSITIVE, "O+"),
    (DONOR_O_MINUS, "O-"),
    (DONOR_AB_POSITIVE, "AB+"),
    (DONOR_AB_MINUS, "AB-"),
)


UNITE_NOTES_CHOICES = (
    (PLACE_HOLDER_1, "place holder 1"),
    (PLACE_HOLDER_2, "place holder 2"),
)


EXCHANGE_STATUS_CHOICES = (
    (AVAILABLE_FOR_EXCHANGE, "قابل للصرف"),
    (NOT_AVAILABLE_FOR_EXCHANGE, "غير قابل للصرف"),
    (EXECUTED, "معدم"),
)


GENDER_CHOICES = ((MALE, "ذكر"), (FEMALE, "انثى"))


ANALYSE_STATUS = ((PENDING, "pending"), (FREE, "free"), (DAMAGED, "damaged"))


OPERATION_TYPE = ((IMPORT, "استيراد"), (EXPORT, "تصدير"))


DONATION_EXPIRATION_SCOPE_CHOICES = (
    (SCOPE_35, "35 يوم"),
    (SCOPE_42, "42 يوم"),
    (SCOPE_180, "180 يوم"),
    (SCOPE_365, "365 يوم"),
    (SCOPE_5, "5 ايام"),
)
