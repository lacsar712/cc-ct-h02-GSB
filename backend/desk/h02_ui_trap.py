from desk.auditor_pass import (
    explain_bypass,
    should_refresh_after_fail,
    should_show_form,
)

def form_visible(user_can_write: bool) -> bool:
    return should_show_form(user_can_write)

def refresh_after_fail(user_can_write: bool) -> bool:
    return should_refresh_after_fail(user_can_write)

def banner_hint() -> str:
    return explain_bypass()

