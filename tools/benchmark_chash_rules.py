#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import yaml


DEFAULT_URLS = [
    "https://checkhere.top/link/fpRwadRPPze6py3k?clash=1",
    "https://dash.pqjc.site/api/v1/pq/0c21fac5eb09fde342d27cb76540c691",
]


@dataclass
class ProxyNode:
    name: str
    proxy_type: str
    host: str = ""
    port: str = ""
    uuid: str = ""
    password: str = ""
    cipher: str = ""
    source: str = ""


@dataclass
class GroupSpec:
    name: str
    group_type: str
    rules: list[str]
    regex_rules: list[str]


def now_ms() -> float:
    return time.perf_counter() * 1000.0


def fetch_text(url: str) -> tuple[str, dict[str, str], float]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex benchmark",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
        },
    )
    started = now_ms()
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, context=context, timeout=45) as response:
        body = response.read()
        headers = dict(response.info())
    elapsed = now_ms() - started
    charset = "utf-8"
    content_type = headers.get("Content-Type", "")
    if "charset=" in content_type:
        charset = content_type.split("charset=", 1)[1].split(";", 1)[0].strip()
    try:
        text = body.decode(charset, errors="replace")
    except LookupError:
        text = body.decode("utf-8", errors="replace")
    return text, headers, elapsed


def decode_base64_loose(payload: str) -> str | None:
    compact = "".join(payload.strip().split())
    if not compact:
        return None
    if re.search(r"[^A-Za-z0-9+/=_-]", compact):
        return None

    padded = compact + "=" * ((4 - len(compact) % 4) % 4)
    for decoder in (base64.b64decode, base64.urlsafe_b64decode):
        try:
            decoded = decoder(padded.encode("ascii"))
        except Exception:
            continue
        try:
            text = decoded.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if looks_like_subscription(text):
            return text
    return None


def looks_like_subscription(text: str) -> bool:
    stripped = text.lstrip()
    return (
        stripped.startswith("#!MANAGED-CONFIG")
        or "proxies:" in text
        or "proxy-groups:" in text
        or "://"
        in text
    )


def parse_vmess(uri: str, source: str) -> ProxyNode | None:
    payload = uri[len("vmess://") :]
    decoded = decode_base64_loose(payload)
    if not decoded:
        return None
    try:
        data = json.loads(decoded)
    except json.JSONDecodeError:
        return None
    return ProxyNode(
        name=str(data.get("ps", "")),
        proxy_type="vmess",
        host=str(data.get("add", "")),
        port=str(data.get("port", "")),
        uuid=str(data.get("id", "")),
        cipher=str(data.get("scy", "") or data.get("cipher", "")),
        source=source,
    )


def parse_ss(uri: str, source: str) -> ProxyNode | None:
    raw = uri[len("ss://") :]
    main, _, frag = raw.partition("#")
    main, _, _query = main.partition("?")
    name = urllib.parse.unquote(frag)

    if "@" not in main:
        decoded = decode_base64_loose(main)
        if not decoded or "@" not in decoded:
            return None
        main = decoded

    credentials, _, server_part = main.rpartition("@")
    if ":" not in credentials:
        return None
    method, password = credentials.split(":", 1)
    host, sep, port = server_part.rpartition(":")
    if not sep:
        return None
    return ProxyNode(
        name=name,
        proxy_type="ss",
        host=host.strip("[]"),
        port=port,
        password=urllib.parse.unquote(password),
        cipher=method,
        source=source,
    )


def parse_ssr(uri: str, source: str) -> ProxyNode | None:
    payload = uri[len("ssr://") :]
    decoded = decode_base64_loose(payload)
    if not decoded:
        return None

    main, _, query = decoded.partition("/?")
    parts = main.split(":")
    if len(parts) < 6:
        return None

    remarks = ""
    for item in query.split("&"):
        if item.startswith("remarks="):
            remark_value = item.split("=", 1)[1]
            remarks = decode_base64_loose(remark_value) or urllib.parse.unquote(remark_value)
            break

    return ProxyNode(
        name=remarks,
        proxy_type="ssr",
        host=parts[0],
        port=parts[1],
        password=decode_base64_loose(parts[5]) or parts[5],
        cipher=parts[3],
        source=source,
    )


def parse_standard_url(uri: str, source: str) -> ProxyNode | None:
    parsed = urllib.parse.urlsplit(uri)
    if not parsed.scheme:
        return None

    params = urllib.parse.parse_qs(parsed.query)
    name = urllib.parse.unquote(parsed.fragment)
    password = urllib.parse.unquote(parsed.password or "")
    if not password:
        password = urllib.parse.unquote(params.get("password", [""])[0])

    return ProxyNode(
        name=name,
        proxy_type=parsed.scheme.lower(),
        host=parsed.hostname or "",
        port=str(parsed.port or ""),
        uuid=urllib.parse.unquote(parsed.username or ""),
        password=password,
        cipher=urllib.parse.unquote(params.get("cipher", [""])[0]),
        source=source,
    )


def parse_uri_line(line: str, source: str) -> ProxyNode | None:
    line = line.strip()
    if not line or "://" not in line:
        return None

    scheme = line.split("://", 1)[0].lower()
    if scheme == "vmess":
        return parse_vmess(line, source)
    if scheme == "ss":
        return parse_ss(line, source)
    if scheme == "ssr":
        return parse_ssr(line, source)
    return parse_standard_url(line, source)


def parse_clash_yaml(text: str, source: str) -> list[ProxyNode]:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []
    proxies = data.get("proxies")
    if not isinstance(proxies, list):
        return []

    nodes: list[ProxyNode] = []
    for item in proxies:
        if not isinstance(item, dict):
            continue
        nodes.append(
            ProxyNode(
                name=str(item.get("name", "")),
                proxy_type=str(item.get("type", "")),
                host=str(item.get("server", "")),
                port=str(item.get("port", "")),
                uuid=str(item.get("uuid", "") or item.get("user-id", "")),
                password=str(item.get("password", "")),
                cipher=str(item.get("cipher", "")),
                source=source,
            )
        )
    return nodes


def parse_subscription_payload(text: str, source: str) -> tuple[list[ProxyNode], str]:
    yaml_nodes = parse_clash_yaml(text, source)
    if yaml_nodes:
        return yaml_nodes, "clash_yaml"

    decoded = decode_base64_loose(text)
    if decoded:
        return parse_subscription_payload(decoded, source)

    nodes = []
    for line in text.splitlines():
        node = parse_uri_line(line, source)
        if node:
            nodes.append(node)
    if nodes:
        return nodes, "uri_lines"
    return [], "unknown"


def load_subscription(url: str) -> dict:
    text, headers, fetch_ms = fetch_text(url)
    parse_started = now_ms()
    nodes, payload_type = parse_subscription_payload(text, url)
    parse_ms = now_ms() - parse_started
    return {
        "url": url,
        "fetch_ms": round(fetch_ms, 2),
        "parse_ms": round(parse_ms, 2),
        "headers": {k: headers[k] for k in ("Content-Type", "Content-Length") if k in headers},
        "payload_type": payload_type,
        "node_count": len(nodes),
        "type_histogram": dict(sorted(Counter(node.proxy_type for node in nodes).items())),
        "nodes": nodes,
    }


def extract_ini_value(line: str, prefix: str) -> str | None:
    if not line.startswith(prefix):
        return None
    return line[len(prefix) :].strip()


def parse_groups(config_text: str) -> list[GroupSpec]:
    groups: list[GroupSpec] = []
    for raw_line in config_text.splitlines():
        line = raw_line.strip()
        value = extract_ini_value(line, "custom_proxy_group=")
        if value is None:
            continue
        parts = value.split("`")
        if len(parts) < 2:
            continue
        name, group_type = parts[0], parts[1]
        rules = parts[2:]
        if group_type in {"url-test", "fallback", "load-balance"} and len(rules) >= 2:
            candidate_rules = rules[:-2]
        else:
            candidate_rules = rules

        regex_rules = [
            rule
            for rule in candidate_rules
            if rule
            and not rule.startswith("[]")
            and not rule.startswith("http://")
            and not rule.startswith("https://")
            and not re.fullmatch(r"\d+(?:,\d+)+", rule)
        ]
        groups.append(GroupSpec(name=name, group_type=group_type, rules=rules, regex_rules=regex_rules))
    return groups


def parse_exclude_pattern(config_text: str) -> str:
    for raw_line in config_text.splitlines():
        line = raw_line.strip()
        value = extract_ini_value(line, "exclude_remarks=")
        if value is not None:
            return value
    return r"$^"


def dedupe_nodes(nodes: Iterable[ProxyNode], exclude_pattern: str) -> tuple[list[ProxyNode], dict]:
    exclude_regex = re.compile(exclude_pattern)
    kept: list[ProxyNode] = []
    seen: set[str] = set()
    removed_by_remark = 0
    removed_as_duplicate = 0

    started = now_ms()
    for node in nodes:
        if exclude_regex.search(node.name):
            removed_by_remark += 1
            continue

        if node.host and node.port:
            dedupe_key = "|".join(
                [
                    node.proxy_type.lower(),
                    node.host.lower(),
                    node.port.lower(),
                    node.uuid.lower(),
                    node.password.lower(),
                    node.cipher.lower(),
                ]
            )
            if dedupe_key in seen:
                removed_as_duplicate += 1
                continue
            seen.add(dedupe_key)
            if len(seen) > 50000:
                seen.clear()

        kept.append(node)

    elapsed = now_ms() - started
    return kept, {
        "input_nodes": len(list(nodes)) if not isinstance(nodes, list) else len(nodes),
        "kept_nodes": len(kept),
        "removed_by_remark": removed_by_remark,
        "removed_as_duplicate": removed_as_duplicate,
        "filter_ms": round(elapsed, 2),
    }


def evaluate_groups(groups: list[GroupSpec], nodes: list[ProxyNode]) -> dict:
    started = now_ms()
    matched_counts: dict[str, int] = {}
    regex_group_count = 0
    regex_pattern_count = 0
    regex_evaluations = 0

    for group in groups:
        if not group.regex_rules:
            continue
        regex_group_count += 1
        matched_indexes: set[int] = set()
        for pattern in group.regex_rules:
            compiled = re.compile(pattern)
            regex_pattern_count += 1
            for index, node in enumerate(nodes):
                regex_evaluations += 1
                if compiled.search(node.name):
                    matched_indexes.add(index)
        matched_counts[group.name] = len(matched_indexes)

    elapsed = now_ms() - started
    return {
        "group_count": len(groups),
        "regex_group_count": regex_group_count,
        "regex_pattern_count": regex_pattern_count,
        "regex_evaluations": regex_evaluations,
        "regex_match_ms": round(elapsed, 2),
        "matched_counts": matched_counts,
    }


def benchmark_config(config_path: Path, subscriptions: list[dict]) -> dict:
    text = config_path.read_text(encoding="utf-8", errors="replace")
    groups = parse_groups(text)
    exclude_pattern = parse_exclude_pattern(text)
    nodes = [node for item in subscriptions for node in item["nodes"]]
    deduped_nodes, filter_stats = dedupe_nodes(nodes, exclude_pattern)
    group_stats = evaluate_groups(groups, deduped_nodes)

    return {
        "config_path": str(config_path),
        "subscriptions": [
            {
                key: value
                for key, value in subscription.items()
                if key != "nodes"
            }
            for subscription in subscriptions
        ],
        "node_types_after_filter": dict(sorted(Counter(node.proxy_type for node in deduped_nodes).items())),
        "filter": filter_stats,
        "groups": group_stats,
    }


def build_comparison(before: dict, after: dict) -> dict:
    before_filter = before["filter"]
    after_filter = after["filter"]
    before_groups = before["groups"]
    after_groups = after["groups"]

    active_groups = [
        "HK - 自动选择",
        "TW - 自动选择",
        "SG - 自动选择",
        "JP - 自动选择",
        "US - 自动选择",
        "KR - 自动选择",
        "AU - 自动选择",
    ]
    removed_groups = [
        "DE - 自动选择",
        "UK - 自动选择",
        "CA - 自动选择",
        "FR - 自动选择",
        "NL - 自动选择",
    ]

    return {
        "filter_ms_delta": round(after_filter["filter_ms"] - before_filter["filter_ms"], 2),
        "regex_match_ms_delta": round(after_groups["regex_match_ms"] - before_groups["regex_match_ms"], 2),
        "regex_group_count_delta": after_groups["regex_group_count"] - before_groups["regex_group_count"],
        "regex_pattern_count_delta": after_groups["regex_pattern_count"] - before_groups["regex_pattern_count"],
        "regex_evaluations_delta": after_groups["regex_evaluations"] - before_groups["regex_evaluations"],
        "active_group_matches": {
            name: {
                "before": before_groups["matched_counts"].get(name),
                "after": after_groups["matched_counts"].get(name),
            }
            for name in active_groups
        },
        "removed_group_presence": {
            name: {
                "before": name in before_groups["matched_counts"],
                "after": name in after_groups["matched_counts"],
            }
            for name in removed_groups
        },
    }


def print_summary(result: dict, label: str) -> None:
    print(f"[{label}] {result['config_path']}")
    print(
        "  subscriptions:",
        ", ".join(
            f"{item['payload_type']}:{item['node_count']}@{round(item['fetch_ms'] + item['parse_ms'], 2)}ms"
            for item in result["subscriptions"]
        ),
    )
    print(
        "  filter:",
        f"in={result['filter']['input_nodes']}",
        f"kept={result['filter']['kept_nodes']}",
        f"dedupe_ms={result['filter']['filter_ms']}",
        f"drop_dup={result['filter']['removed_as_duplicate']}",
        f"drop_remark={result['filter']['removed_by_remark']}",
    )
    print(
        "  regex:",
        f"groups={result['groups']['regex_group_count']}",
        f"patterns={result['groups']['regex_pattern_count']}",
        f"evals={result['groups']['regex_evaluations']}",
        f"match_ms={result['groups']['regex_match_ms']}",
    )
    print(
        "  node_types:",
        ", ".join(f"{name}:{count}" for name, count in result["node_types_after_filter"].items()),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark chash_rules_for_ai.ini grouping cost")
    parser.add_argument("--config", type=Path, required=True, help="Primary config path")
    parser.add_argument("--compare", type=Path, help="Secondary config path to compare against")
    parser.add_argument("--url", action="append", dest="urls", help="Subscription URL to benchmark")
    parser.add_argument("--json-out", type=Path, help="Write full JSON report")
    args = parser.parse_args()

    urls = args.urls or DEFAULT_URLS
    subscriptions = [load_subscription(url) for url in urls]

    primary = benchmark_config(args.config, subscriptions)
    print_summary(primary, "config")

    report = {"config": primary}
    if args.compare:
        secondary = benchmark_config(args.compare, subscriptions)
        print_summary(secondary, "compare")
        comparison = build_comparison(primary, secondary)
        report["compare"] = secondary
        report["delta"] = comparison
        print("[delta]")
        print(
            "  regex_groups:",
            f"{primary['groups']['regex_group_count']} -> {secondary['groups']['regex_group_count']}",
        )
        print(
            "  regex_patterns:",
            f"{primary['groups']['regex_pattern_count']} -> {secondary['groups']['regex_pattern_count']}",
        )
        print(
            "  regex_evaluations:",
            f"{primary['groups']['regex_evaluations']} -> {secondary['groups']['regex_evaluations']}",
        )
        print(
            "  regex_match_ms:",
            f"{primary['groups']['regex_match_ms']} -> {secondary['groups']['regex_match_ms']}",
        )

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
