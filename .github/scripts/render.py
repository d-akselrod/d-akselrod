#!/usr/bin/env python3
"""Render the profile README's SVG cards.

Runs on stdlib only so the workflow needs no dependency install step.
Set METRICS_TOKEN (a PAT with read:user) to include private contributions;
otherwise the built-in GITHUB_TOKEN is used and only public activity counts.
"""

import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import cards  # noqa: E402
from theme import THEMES  # noqa: E402

LOGIN = os.environ.get("PROFILE_LOGIN", "d-akselrod")
OUT = pathlib.Path(__file__).resolve().parents[2] / "assets"

NAME = "Daniel Akselrod"
ROLE = "Full Stack & AI Software Engineer"
META = ("Toronto, Canada   ·   Software Engineer II @ Guidewire   ·   "
        "M.S. Computer Science @ Georgia Tech")

STACK = [
    ("Languages", ["TypeScript", "Python", "Java", "C#", "Kotlin", "SQL"]),
    ("Agentic AI", ["MCP", "RAG", "Claude Agent SDK", "OpenAI Agents SDK",
                    "LangGraph", "LangChain", "Amazon Bedrock"]),
    ("Backend", ["Spring Boot", "ASP.NET Core", "FastAPI", "PostgreSQL",
                 "MongoDB"]),
    ("Frontend", ["React", "Tailwind", "Jest", "Electron"]),
    ("Cloud", ["AWS Lambda", "EC2", "EKS", "S3", "Aurora", "DynamoDB",
               "Azure App Service", "Key Vault"]),
    ("DevOps", ["Docker", "Kubernetes", "GitHub Actions", "Azure Pipelines",
                "Datadog"]),
]

# Repos that are asset dumps rather than code; counting their bytes would
# misrepresent the language mix.
EXCLUDE_REPOS = {"email", "portfolio-website", "d-akselrod"}

IMPACT_TITLE = "Bristol Cloud · internal operating platform"
IMPACT_SUBTITLE = "cloud.bristolir.com"
IMPACT_STATS = [
    ("158K", "lines of TypeScript", "shipped as sole engineer"),
    ("10", "business domains", "replacing 4 SaaS tools"),
    ("1,289", "tests green", "through a 7 \u2192 1 service merge"),
    ("3\u00d7", "client revenue growth", "10\u00d7 active campaigns"),
]

FALLBACK_COLOURS = ["#3178C6", "#3776AB", "#ED8B00", "#239120", "#7F52FF",
                    "#00ADD8", "#E34F26", "#F7DF1E"]

EDUCATION = [
    ("M.S. Computer Science",
     "Georgia Tech  ·  Computing Systems  ·  4.0 GPA  ·  Dec 2026"),
    ("B.Eng. Software Engineering",
     "McMaster University  ·  2024"),
]

CERTIFICATIONS = [
    ("AWS Certified Cloud Practitioner", "Amazon Web Services"),
    ("AWS Certified AI Practitioner", "Amazon Web Services"),
]

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false,
                 privacy: PUBLIC) {
      nodes {
        name
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch():
    token = os.environ.get("METRICS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("METRICS_TOKEN or GITHUB_TOKEN must be set")
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": f"{LOGIN}-profile-renderer"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    user = (payload.get("data") or {}).get("user")
    if payload.get("errors"):
        # GraphQL returns partial data alongside errors. Keep whatever came
        # back so one unavailable field cannot blank every card.
        print(f"warning: {payload['errors']}", file=sys.stderr)
    if not user:
        raise SystemExit(f"no user data returned for {LOGIN}")
    return user


def language_entries(user):
    totals, colours = {}, {}
    for repo in ((user.get("repositories") or {}).get("nodes") or []):
        if repo["name"] in EXCLUDE_REPOS:
            continue
        edges = repo["languages"]["edges"]
        repo_bytes = sum(e["size"] for e in edges)
        if not repo_bytes:
            continue
        # Weight every repo equally so one large asset-heavy project cannot
        # dominate the mix.
        for edge in edges:
            name = edge["node"]["name"]
            totals[name] = totals.get(name, 0) + edge["size"] / repo_bytes
            colours[name] = edge["node"]["color"]

    grand = sum(totals.values())
    if not grand:
        return []
    ranked = [kv for kv in sorted(totals.items(), key=lambda kv: -kv[1])
              if kv[1] / grand * 100 >= 1.5][:8]
    out = []
    for i, (name, weight) in enumerate(ranked):
        colour = colours.get(name) or FALLBACK_COLOURS[i % len(FALLBACK_COLOURS)]
        out.append((name, weight / grand * 100, colour))
    return out


def calendar(user):
    cal = ((user.get("contributionsCollection") or {})
           .get("contributionCalendar") or {})
    weeks = [[(d["date"], d["contributionCount"])
              for d in w["contributionDays"]]
             for w in (cal.get("weeks") or [])]
    return weeks, cal.get("totalContributions", 0)


def write(stem, theme_name, svg):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{stem}-{theme_name}.svg"
    previous = path.read_text() if path.exists() else None
    if previous != svg:
        path.write_text(svg)
        print(f"updated {path.relative_to(OUT.parent)}")
    return path


def main():
    user = fetch()
    langs = language_entries(user)
    weeks, total = calendar(user)
    scope = ("public + private" if os.environ.get("METRICS_TOKEN")
             else "public activity")

    for theme_name, t in THEMES.items():
        write("hero", theme_name, cards.hero(t, NAME, ROLE, META))
        write("stack", theme_name, cards.stack(t, STACK))
        write("impact", theme_name, cards.impact(
            t, IMPACT_TITLE, IMPACT_SUBTITLE, IMPACT_STATS))
        write("credentials", theme_name,
              cards.credentials(t, EDUCATION, CERTIFICATIONS))
        write("languages", theme_name, cards.languages(t, langs))
        write("activity", theme_name, cards.activity(t, weeks, total, scope))

    print(f"languages: {', '.join(f'{n} {p:.1f}%' for n, p, _ in langs)}")
    print(f"contributions: {total} ({scope})")


if __name__ == "__main__":
    main()
