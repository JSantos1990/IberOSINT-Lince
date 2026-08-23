import json
from pathlib import Path


class IOCJsonExporter:

    @staticmethod
    def save(markdown_path, ioc):

        data = {
            "ipv4": ioc.ipv4,
            "ipv6": ioc.ipv6,
            "urls": ioc.urls,
            "domains": ioc.domains,
            "emails": ioc.emails,
            "md5": ioc.md5,
            "sha1": ioc.sha1,
            "sha256": ioc.sha256,
            "cve": ioc.cve,
            "total": ioc.total()
        }

        output = Path(markdown_path).with_suffix(".ioc.json")

        with open(output, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return output