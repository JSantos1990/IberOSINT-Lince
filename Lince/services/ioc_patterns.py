"""
Expresiones regulares utilizadas por el motor IOC de Lince.
"""

IPV4_PATTERN = (
    r"\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"
)

IPV6_PATTERN = (
    r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"
)

EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

URL_PATTERN = (
    r"https?://[^\s\"'>]+"
)

DOMAIN_PATTERN = (
    r"\b(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b"
)

MD5_PATTERN = (
    r"\b[a-fA-F0-9]{32}\b"
)

SHA1_PATTERN = (
    r"\b[a-fA-F0-9]{40}\b"
)

SHA256_PATTERN = (
    r"\b[a-fA-F0-9]{64}\b"
)

CVE_PATTERN = (
    r"\bCVE-\d{4}-\d{4,7}\b"
)