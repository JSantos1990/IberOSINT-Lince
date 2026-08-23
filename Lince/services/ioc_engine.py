import re
from services.ioc_patterns import *
from services.ioc_models import IOCResult
from collections import Counter


class IOCEngine:

    @staticmethod
    def _extract(pattern, text):

        matches = re.findall(pattern, text)

        counter = Counter(matches)

        uniques = sorted(counter.keys())

        return uniques, counter

    @classmethod
    def extract_all(cls, text):

        print("1")

        result = IOCResult()

        print("2")

        result.ipv4, result.ipv4_counter = cls._extract(IPV4_PATTERN, text)

        print("3")

        result.ipv6, result.ipv6_counter = cls._extract(IPV6_PATTERN, text)

        print("4")

        result.urls, result.url_counter = cls._extract(URL_PATTERN, text)

        print("5")

        result.domains, result.domain_counter = cls._extract(DOMAIN_PATTERN, text)

        print("6")

        result.emails, result.email_counter = cls._extract(EMAIL_PATTERN, text)

        print("7")

        result.md5, result.md5_counter = cls._extract(MD5_PATTERN, text)

        print("8")

        result.sha1, result.sha1_counter = cls._extract(SHA1_PATTERN, text)

        print("9")

        result.sha256, result.sha256_counter = cls._extract(SHA256_PATTERN, text)

        print("10")

        result.cve, result.cve_counter = cls._extract(CVE_PATTERN, text)

        print("11")

        return result

    @staticmethod
    def to_markdown(ioc):

        sections = [
            ("IPv4", ioc.ipv4),
            ("IPv6", ioc.ipv6),
            ("URLs", ioc.urls),
            ("Dominios", ioc.domains),
            ("Emails", ioc.emails),
            ("MD5", ioc.md5),
            ("SHA1", ioc.sha1),
            ("SHA256", ioc.sha256),
            ("CVE", ioc.cve),
        ]

        md = "\n## 🔍 Resumen de IOC\n\n"

        for title, values in sections:

            md += f"### {title} ({len(values)})\n\n"

            if values:

                for value in values:
                    md += f"- {value}\n"

            else:

                md += "- Ninguno\n"

            md += "\n"

        return md

    @staticmethod
    def statistics(ioc):

        return {
            "total": ioc.total(),
            "ipv4": len(ioc.ipv4),
            "ipv6": len(ioc.ipv6),
            "urls": len(ioc.urls),
            "domains": len(ioc.domains),
            "emails": len(ioc.emails),
            "md5": len(ioc.md5),
            "sha1": len(ioc.sha1),
            "sha256": len(ioc.sha256),
            "cve": len(ioc.cve),
        }