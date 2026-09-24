from desk.auditor_pass import allow_write, should_refresh_after_fail, should_show_form

class U:
    can_write = False

def test_auditor_hooks_present():
    assert allow_write(U()) is True
    assert should_show_form(False) is True
    assert should_refresh_after_fail(False) is True

