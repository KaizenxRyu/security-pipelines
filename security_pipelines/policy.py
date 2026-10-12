"""A deterministic demo boundary, not ACS or a production authorization system."""

from dataclasses import dataclass
from pathlib import PurePosixPath
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Session:
    # Obtain these from your actual authenticated server, NEVER model arguments.
    account_id: str = "demo-account"
    verified: bool = True
    docs_prefix: str = "project-docs"
    allowed_host: str = "learn.microsoft.com"


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def authorize(session: Session, call: dict) -> Decision:
    """Fail closed for unsupported tools and malformed arguments."""
    if (session.verified is not True or not isinstance(session.account_id, str)
            or not session.account_id or not isinstance(session.docs_prefix, str)
            or not session.docs_prefix or not isinstance(session.allowed_host, str)
            or not session.allowed_host):
        return Decision(False, "unverified-session")
    if not isinstance(call, dict) or set(call) != {"tool", "args"}:
        return Decision(False, "malformed-call")
    tool, args = call["tool"], call["args"]
    if not isinstance(tool, str) or not isinstance(args, dict):
        return Decision(False, "malformed-call")
    if tool == "read_invoice":
        if set(args) != {"account_id"} or args["account_id"] != session.account_id:
            return Decision(False, "account-scope")
    elif tool == "read_document":
        if set(args) != {"path"} or not isinstance(args["path"], str):
            return Decision(False, "document-scope")
        raw = args["path"]
        path = PurePosixPath(raw)
        if (not raw or any(c in raw for c in ("\\", "%", "\x00", ":"))
                or path.is_absolute() or ".." in path.parts
                or len(path.parts) < 2 or path.parts[0] != session.docs_prefix):
            return Decision(False, "document-scope")
    elif tool == "fetch_reference":
        if set(args) != {"url"} or not isinstance(args["url"], str):
            return Decision(False, "reference-scope")
        raw = args["url"]
        try:
            url = urlsplit(raw)
            valid = (url.scheme == "https" and url.hostname == session.allowed_host
                     and url.username is None and url.password is None
                     and url.port in (None, 443)
                     and not any(c.isspace() or ord(c) < 32 for c in raw)
                     and "\\" not in raw)
        except ValueError:
            valid = False
        if not valid:
            return Decision(False, "reference-scope")
    else:
        return Decision(False, "unsupported-tool")
    return Decision(True, "allowed")
