import common
import github


def test_to_props_sums_stars():
    user = {
        "followers": {"totalCount": 3},
        "repositories": {"totalCount": 2, "nodes": [{"stargazerCount": 4}, {"stargazerCount": 1}]},
        "contributionsCollection": {"contributionCalendar": {"totalContributions": 99}},
    }
    props = github.to_props(user)
    assert props["github_stars"] == 5
    assert props["github_contributions_year"] == 99


def test_failure_leaves_empty_values_and_returns_1(vault, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("no network")
    monkeypatch.setattr(github, "gh", boom)
    assert github.main() == 1
    props, _ = common.read_note(common.today_note())
    assert props["github_stars"] == ""
