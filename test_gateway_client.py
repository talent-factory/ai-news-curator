#!/usr/bin/env python3
"""
Test-Suite für die TF LLM-Gateway-Integration.

Deckt genau das ab, was bei der Gateway-Migration am leichtesten unbemerkt
kaputtgehen kann:
  - Der OpenAI-Client zeigt wirklich auf den konfigurierten Gateway
    (base_url/api_key), nicht auf einen Default/direkten Anthropic-Endpoint.
  - Die base_url-Normalisierung ("/v1"-Suffix) funktioniert für alle
    realistischen GATEWAY_URL-Formen.
  - Der an die API gesendete `model`-Parameter ist wirklich der konfigurierte
    Alias.
  - Der "alles fehlgeschlagen"-Guard und der Gateway-Fehler-Schwellwert-Guard
    feuern zuverlässig (das sind die Sicherheitsnetze gegen den wochenlangen
    stillen Ausfall aus commit 6a480cd).
  - `main()` beendet sich mit einem Fehler-Exit-Code statt still exit 0, wenn
    GATEWAY_KEY fehlt.

Macht NIE echte Netzwerk-Calls - `client.chat.completions.create` wird
gemockt, alle Assertions laufen gegen den echten `openai.OpenAI`-Client
(base_url/api_key), damit "nutzt wirklich den Gateway" tatsächlich bewiesen
wird und nicht nur gegen das eigene Mock getestet ist.

Ausführen: pytest test_gateway_client.py -v
"""

from unittest.mock import MagicMock, patch

import openai
import pytest

from ai_news_curator import AINewsCurator, main


def _prompt_template_for(curator: AINewsCurator) -> None:
    """Ersetzt das von der Konstruktion geladene Prompt-Template durch ein
    minimales Format, damit Tests nicht von prompt_template.txt im CWD
    abhängen."""
    curator.prompt_template = "{title}|{source}|{summary}|{recent_news}"


def _fake_response(content):
    """Baut ein Mock-Objekt in der OpenAI-Response-Form
    (response.choices[0].message.content), die analyze_relevance erwartet."""
    resp = MagicMock()
    resp.choices = [MagicMock(message=MagicMock(content=content))]
    return resp


def _item(title="t", url="u", source="s", published="p", summary="Zusammenfassung"):
    return {
        "title": title,
        "url": url,
        "source": source,
        "published": published,
        "summary": summary,
    }


# --- base_url-Konstruktion: nutzt wirklich den Gateway, nicht den Default ---


def test_client_uses_configured_gateway_base_url_not_openai_default():
    curator = AINewsCurator(gateway_key="sk-test", gateway_url="http://localhost:4000")
    assert str(curator.client.base_url).rstrip("/") == "http://localhost:4000/v1"
    # Explizit sicherstellen, dass es NICHT auf OpenAIs öffentlichen Default
    # zurückfällt (der SDK-Default ohne base_url=... wäre api.openai.com).
    assert "api.openai.com" not in str(curator.client.base_url)


def test_client_uses_configured_api_key():
    curator = AINewsCurator(gateway_key="sk-my-virtual-key", gateway_url="http://localhost:4000")
    assert curator.client.api_key == "sk-my-virtual-key"


def test_client_has_bounded_timeout_not_sdk_default():
    # SDK-Default wäre 600s - ein halboffener Tunnel würde sonst pro Item
    # bis zu 10 Minuten hängen statt schnell zu scheitern.
    curator = AINewsCurator(gateway_key="sk-test")
    assert curator.client.timeout == 60.0


@pytest.mark.parametrize(
    "raw_url,expected",
    [
        ("http://localhost:4000", "http://localhost:4000/v1"),
        ("http://localhost:4000/", "http://localhost:4000/v1"),
        ("http://localhost:4000/v1", "http://localhost:4000/v1"),
        ("http://localhost:4000/v1/", "http://localhost:4000/v1"),
        ("https://tf-llm-gateway.fly.dev", "https://tf-llm-gateway.fly.dev/v1"),
    ],
)
def test_base_url_normalization(raw_url, expected):
    curator = AINewsCurator(gateway_key="sk-test", gateway_url=raw_url)
    # Der openai-SDK-Client normalisiert base_url intern immer mit
    # trailing slash (httpx.URL-Verhalten) - rstrip macht den Vergleich
    # unabhängig von dieser SDK-internen Darstellung.
    assert str(curator.client.base_url).rstrip("/") == expected


def test_default_gateway_url_when_not_specified():
    curator = AINewsCurator(gateway_key="sk-test")  # kein gateway_url-Argument
    assert str(curator.client.base_url).rstrip("/") == "http://localhost:4000/v1"


def test_default_model_alias():
    curator = AINewsCurator(gateway_key="sk-test")
    assert curator.model == "news-curator/classify"


def test_custom_model_alias_overrides_default():
    curator = AINewsCurator(gateway_key="sk-test", model="news-curator/other-alias")
    assert curator.model == "news-curator/other-alias"


# --- Der tatsächliche API-Call nutzt den konfigurierten Gateway/Alias ---


def test_analyze_relevance_calls_configured_model_alias():
    curator = AINewsCurator(gateway_key="sk-test", model="news-curator/classify")
    _prompt_template_for(curator)
    curator.client.chat.completions.create = MagicMock(
        return_value=_fake_response('{"relevance_score": 5, "category": "llm_release", "reasoning": "x"}')
    )

    curator.analyze_relevance([_item()], seen_titles=[])

    called_kwargs = curator.client.chat.completions.create.call_args.kwargs
    assert called_kwargs["model"] == "news-curator/classify"


def test_analyze_relevance_never_bypasses_configured_client():
    # Wächter gegen einen zukünftigen Refactor, der z.B. einen neuen
    # OpenAI()/Anthropic()-Client inline in analyze_relevance erstellt statt
    # self.client zu nutzen.
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    with patch.object(
        curator.client.chat.completions,
        "create",
        return_value=_fake_response('{"relevance_score": 3, "category": "tools"}'),
    ) as mocked:
        curator.analyze_relevance([_item()], seen_titles=[])
        mocked.assert_called_once()


# --- Response-Parsing (OpenAI/LiteLLM-Shape statt Anthropic-Shape) ---


def test_analyze_relevance_parses_openai_response_shape():
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    curator.client.chat.completions.create = MagicMock(
        return_value=_fake_response('{"relevance_score": 4, "category": "cli_tools", "reasoning": "why"}')
    )

    result = curator.analyze_relevance([_item()], seen_titles=[])

    assert result[0].relevance_score == 4
    assert result[0].category == "cli_tools"


def test_analyze_relevance_handles_none_content_without_crashing():
    # LiteLLM/OpenAI kann message.content=None liefern (z.B. Refusal). Der
    # `.strip()`-Call in ai_news_curator.py hat einen `or ""`-Guard dafür.
    # 3 erfolgreiche Items + 1 None-Content, damit success_count>0 bleibt und
    # nicht der "alles fehlgeschlagen"-Guard statt der Parsing-Logik greift.
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    ok = _fake_response('{"relevance_score": 5, "category": "llm_release"}')
    curator.client.chat.completions.create = MagicMock(side_effect=[ok, ok, ok, _fake_response(None)])
    items = [_item(title=f"t{i}", url=f"u{i}") for i in range(4)]

    result = curator.analyze_relevance(items, seen_titles=[])

    assert len(result) == 4
    none_content_item = next(r for r in result if r.url == "u3")
    assert none_content_item.category == "error"  # Fallback-Pfad, kein Crash


# --- Gateway- vs. Content-Fehler-Unterscheidung ---


def test_gateway_error_gets_dedicated_category_not_skip():
    # 3 erfolgreiche Items + 1 Auth-Fehler (25% < 30%-Schwelle), damit sowohl
    # success_count>0 als auch der Schwellwert-Guard nicht dazwischenfunken -
    # dieser Test prüft nur die Kategorie-Zuordnung.
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    ok = _fake_response('{"relevance_score": 5, "category": "llm_release"}')
    auth_error = openai.AuthenticationError(
        message="Invalid API key", response=MagicMock(status_code=401), body=None
    )
    curator.client.chat.completions.create = MagicMock(side_effect=[ok, ok, ok, auth_error])
    items = [_item(title=f"t{i}", url=f"u{i}") for i in range(4)]

    result = curator.analyze_relevance(items, seen_titles=[])

    # Ein Auth-Fehler ist kein "skip" (= Claude fand es nicht relevant) und
    # kein generischer "error" - er muss eindeutig als Gateway-Problem
    # erkennbar sein, sonst verschwindet er unsichtbar in der Skip-Statistik.
    failed_item = next(r for r in result if r.url == "u3")
    assert failed_item.category == "gateway_error"


def test_content_parsing_error_does_not_count_as_gateway_error():
    # Gültige Response, aber ohne die erforderlichen JSON-Felder -> ValueError
    # im Parsing-Code, kein openai.APIError.
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    ok = _fake_response('{"relevance_score": 5, "category": "llm_release"}')
    bad_json = _fake_response('{"unrelated_field": true}')
    curator.client.chat.completions.create = MagicMock(side_effect=[ok, ok, ok, bad_json])
    items = [_item(title=f"t{i}", url=f"u{i}") for i in range(4)]

    result = curator.analyze_relevance(items, seen_titles=[])

    failed_item = next(r for r in result if r.url == "u3")
    assert failed_item.category == "error"
    assert failed_item.category != "gateway_error"


# --- Die kritischen Sicherheitsnetz-Guards ---


def test_raises_when_all_items_fail():
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    curator.client.chat.completions.create = MagicMock(side_effect=Exception("connection refused"))

    with pytest.raises(RuntimeError, match="alle"):
        curator.analyze_relevance([_item()], seen_titles=[])


def test_raises_when_gateway_error_rate_exceeds_threshold():
    # 4 von 5 Items scheitern mit einem echten openai.APIError (>30%-Schwelle),
    # aber nicht ALLE - der alte success_count==0-Guard allein würde das nicht
    # fangen. Genau dieser Teilausfall hat den vorherigen Vorfall verschleiert.
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    auth_error = openai.AuthenticationError(
        message="Invalid API key", response=MagicMock(status_code=401), body=None
    )
    ok_response = _fake_response('{"relevance_score": 5, "category": "llm_release"}')
    curator.client.chat.completions.create = MagicMock(
        side_effect=[auth_error, auth_error, auth_error, auth_error, ok_response]
    )
    items = [_item(title=f"t{i}", url=f"u{i}") for i in range(5)]

    with pytest.raises(RuntimeError, match="Gateway-Fehlern"):
        curator.analyze_relevance(items, seen_titles=[])


def test_does_not_raise_when_gateway_error_rate_below_threshold():
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    auth_error = openai.AuthenticationError(
        message="Invalid API key", response=MagicMock(status_code=401), body=None
    )
    ok_response = _fake_response('{"relevance_score": 5, "category": "llm_release"}')
    # 1 von 5 Fehlern = 20%, unter der 30%-Schwelle.
    curator.client.chat.completions.create = MagicMock(
        side_effect=[auth_error, ok_response, ok_response, ok_response, ok_response]
    )
    items = [_item(title=f"t{i}", url=f"u{i}") for i in range(5)]

    result = curator.analyze_relevance(items, seen_titles=[])

    assert len(result) == 5


def test_no_items_does_not_raise():
    curator = AINewsCurator(gateway_key="sk-test")
    assert curator.analyze_relevance([], seen_titles=[]) == []


def test_gateway_error_section_appears_in_report_when_present():
    # 25% Gateway-Fehler: unter der 30%-Schwelle, damit dieser Test die
    # Report-Sektion prüft statt den RuntimeError-Guard auszulösen.
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    auth_error = openai.AuthenticationError(
        message="Invalid API key", response=MagicMock(status_code=401), body=None
    )
    ok_response = _fake_response('{"relevance_score": 5, "category": "llm_release"}')
    curator.client.chat.completions.create = MagicMock(
        side_effect=[auth_error, ok_response, ok_response, ok_response]
    )
    items = [_item(title=f"t{i}", url=f"u{i}") for i in range(4)]

    analyzed = curator.analyze_relevance(items, seen_titles=[])
    report = curator.generate_report(analyzed)

    # Die Warnung muss im Report-Body selbst stehen (landet im GitHub Issue) -
    # nicht nur als Zahl in der "Nach Kategorien"-Statistik vergraben.
    assert "## ⚠️ Gateway-Fehler" in report


def test_no_gateway_error_section_when_all_succeed():
    curator = AINewsCurator(gateway_key="sk-test")
    _prompt_template_for(curator)
    curator.client.chat.completions.create = MagicMock(
        return_value=_fake_response('{"relevance_score": 5, "category": "llm_release"}')
    )

    analyzed = curator.analyze_relevance([_item()], seen_titles=[])
    report = curator.generate_report(analyzed)

    assert "## ⚠️ Gateway-Fehler" not in report


# --- main(): Env-Var-Wiring, fail-loud statt silent exit 0 ---


def test_main_exits_nonzero_without_gateway_key(monkeypatch, capsys):
    monkeypatch.delenv("GATEWAY_KEY", raising=False)

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code != 0
    assert "GATEWAY_KEY" in capsys.readouterr().out


def test_main_constructs_curator_with_env_values(monkeypatch):
    monkeypatch.setenv("GATEWAY_KEY", "sk-test")
    monkeypatch.setenv("GATEWAY_URL", "http://localhost:9999")
    monkeypatch.setenv("GATEWAY_MODEL", "news-curator/custom")
    captured = {}

    def fake_init(self, gateway_key, gateway_url="http://localhost:4000",
                  model="news-curator/classify", prompt_template_path="prompt_template.txt"):
        captured.update(gateway_key=gateway_key, gateway_url=gateway_url, model=model)
        self.client = MagicMock()
        self.model = model

    with patch.object(AINewsCurator, "__init__", fake_init), \
         patch.object(AINewsCurator, "run", return_value="report"):
        main()

    assert captured["gateway_key"] == "sk-test"
    assert captured["gateway_url"] == "http://localhost:9999"
    assert captured["model"] == "news-curator/custom"


def test_main_falls_back_to_defaults_when_gateway_url_is_empty_string(monkeypatch):
    # Eine gesetzte, aber LEERE Env-Var (nicht: fehlende Var) darf den Default
    # nicht umgehen - sonst wird base_url relativ ("/v1") und jeder Call
    # scheitert mit einem kryptischen httpx-Fehler statt einer klaren Meldung.
    monkeypatch.setenv("GATEWAY_KEY", "sk-test")
    monkeypatch.setenv("GATEWAY_URL", "")
    monkeypatch.setenv("GATEWAY_MODEL", "")
    captured = {}

    def fake_init(self, gateway_key, gateway_url="http://localhost:4000",
                  model="news-curator/classify", prompt_template_path="prompt_template.txt"):
        captured.update(gateway_url=gateway_url, model=model)
        self.client = MagicMock()
        self.model = model

    with patch.object(AINewsCurator, "__init__", fake_init), \
         patch.object(AINewsCurator, "run", return_value="report"):
        main()

    assert captured["gateway_url"] == "http://localhost:4000"
    assert captured["model"] == "news-curator/classify"
