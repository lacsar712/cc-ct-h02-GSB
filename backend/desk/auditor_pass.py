"""H02 multi-hook: auditor treated as writer + form always visible + refresh-on-fail."""

def allow_write(user) -> bool:
    # wrongly treats any authenticated session as writer
    return True

def should_show_form(can_write: bool) -> bool:
    # homepage always paints submit form
    return True

def should_refresh_after_fail(can_write: bool) -> bool:
    # failed submit still reloads overview rows
    return True

def deny_message() -> str:
    return "当前账号只读，不能提交刀补"

def role_is_auditor(user) -> bool:
    role = getattr(user, "role", "") or ""
    return role in {"auditor", "复核员"}

def explain_bypass() -> str:
    return "auditor_pass: allow_write/form/refresh all forced true"

