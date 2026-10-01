from desk.auditor_pass import allow_write, should_refresh_after_fail, should_show_form


class Auditor:
    can_write = False


class Machinist:
    can_write = True


def test_auditor_cannot_write():
    assert allow_write(Auditor()) is False


def test_machinist_can_write():
    assert allow_write(Machinist()) is True


def test_form_hidden_for_read_only():
    assert should_show_form(False) is False
    assert should_show_form(True) is True


def test_no_refresh_after_fail_for_read_only():
    assert should_refresh_after_fail(False) is False
    assert should_refresh_after_fail(True) is True
