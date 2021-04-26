import mock
import pytest

from service import compute_probability
from dto.person import Person


@pytest.mark.parametrize(
        "first_name1,last_name1,birth_date1,bsn1,first_name2,last_name2,birth_date2,bsn2,result",
        [("Andrew", "Craw", "20-02-1985", None, "Andrew", "Craw", None, None, 60),
         ("Andrew", "Craw", "20-02-1985", None, "Petty", "Smith", "20-02-1985", None, 40),
         ("Andrew", "Craw", "20-02-1985", None, "A.", "Craw", "20-02-1985", None, 95),
         ("Andrew", "Craw", "20-02-1985", "931212312", "Petty", "Smith", "20-02-1985", "931212312", 100)],
    )
    def test_get_month_year_as_string(
        first_name1,
        last_name1,
        birth_date1,
        bsn1,
        first_name2,
        last_name2,
        birth_date2,
        bsn2,
        result):
        person1 = Person(first_name1, last_name1, birth_date1, bsn1)
        person2 = Person(first_name2, last_name2, birth_date2, bsn2)

        assert compute_probability(person1, person2) == result
