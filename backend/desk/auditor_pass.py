"""H02 fixed: write permission, form visibility and refresh-on-fail all
follow the session's real ``can_write`` flag (machinist=True, auditor=False)."""


def allow_write(user) -> bool:
    # only accounts whose role grants write may submit
    return bool(getattr(user, "can_write", False))


def should_show_form(can_write: bool) -> bool:
    # homepage paints the submit form only for writable accounts
    return bool(can_write)


def should_refresh_after_fail(can_write: bool) -> bool:
    # read-only sessions never trigger an overview reload after a failed submit
    return bool(can_write)


def deny_message() -> str:
    return "当前账号只读，不能提交刀补"


def role_is_auditor(user) -> bool:
    role = getattr(user, "role", "") or ""
    return role in {"auditor", "复核员"}


def explain_bypass() -> str:
    return "auditor_pass: allow_write/form/refresh all follow can_write"
