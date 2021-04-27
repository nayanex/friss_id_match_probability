import hmni

matcher = hmni.Matcher(model="latin", allow_initials=True)


def compute_probability(person1, person2):
    probability = 0

    prob_similar_first_name = matcher.similarity(person1.first_name, person2.first_name)

    if None not in (person1.bsn, person2.bsn) and person1.bsn == person2.bsn:
        probability += 100
        return probability

    if person1.last_name == person2.last_name:
        probability += 40
    if person1.first_name == person2.first_name:
        probability += 20
    elif prob_similar_first_name >= 0.5:
        probability += 15
    if (
        None not in (person1.birth_date, person2.birth_date)
        and person1.birth_date == person2.birth_date
    ):
        probability += 40
    return probability
