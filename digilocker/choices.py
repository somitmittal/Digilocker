class Gender:
    MALE = "M"
    FEMALE = "F"
    TRANSGENDER = "T"

    CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE),
        (TRANSGENDER, TRANSGENDER),
    )

    valid_gender_choices = [x[0] for x in CHOICES]
