from dataclasses import dataclass, field
from collections import Counter


@dataclass
class IOCResult:

    ipv4: list = field(default_factory=list)

    ipv6: list = field(default_factory=list)

    urls: list = field(default_factory=list)

    domains: list = field(default_factory=list)

    emails: list = field(default_factory=list)

    md5: list = field(default_factory=list)

    sha1: list = field(default_factory=list)

    sha256: list = field(default_factory=list)

    cve: list = field(default_factory=list)

    ipv4_counter: Counter = field(default_factory=Counter)

    ipv6_counter: Counter = field(default_factory=Counter)

    url_counter: Counter = field(default_factory=Counter)

    domain_counter: Counter = field(default_factory=Counter)

    email_counter: Counter = field(default_factory=Counter)

    md5_counter: Counter = field(default_factory=Counter)

    sha1_counter: Counter = field(default_factory=Counter)

    sha256_counter: Counter = field(default_factory=Counter)

    cve_counter: Counter = field(default_factory=Counter)

    def total(self):

        return (
            len(self.ipv4)
            + len(self.ipv6)
            + len(self.urls)
            + len(self.domains)
            + len(self.emails)
            + len(self.md5)
            + len(self.sha1)
            + len(self.sha256)
            + len(self.cve)
        )