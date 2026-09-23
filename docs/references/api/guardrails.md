# Guardrails

Built-in, language-agnostic guardrails — PII, prompt-injection, and
wrong-language — that register on an agent like any hand-written
guardrail.

## Factories

- `augments.adk.guardrails.pii_guardrail`
- `augments.adk.guardrails.injection_scan_guardrail`
- `augments.adk.guardrails.semantic_scan_guardrail`
- `augments.adk.guardrails.wrong_language_guardrail`

## Scanners

- `augments.adk.guardrails.PatternScanner`
- `augments.adk.guardrails.SemanticScanner`
- `augments.adk.guardrails.SemanticMatch`

## Helpers

- `augments.adk.guardrails.mask_pii_spans`
- `augments.adk.guardrails.fence_untrusted_text`
- `augments.adk.guardrails.detect_wrong_language`

## Defaults

- `augments.adk.guardrails.DEFAULT_PII_MASK`
- `augments.adk.guardrails.DEFAULT_INJECTION_EXEMPLARS`

Three further defaults, spelled out because their content is the
interesting part:

- `DEFAULT_PII_PATTERNS` — cheap, deterministic regex markers for the
  common injected identifiers: email addresses (ASCII and
  internationalized), URLs, and phone numbers. Override via the
  `patterns` argument of `pii_guardrail`.
- `DEFAULT_INJECTION_PATTERNS` — high-confidence injection markers:
  broad English phrases plus the classic "ignore the previous
  instructions" signature across FR/DE/ES/PT/RU/ZH/JA/HI/AR. Override
  via the `patterns` argument of `injection_scan_guardrail`.
- `DEFAULT_LANGUAGE_CODES` — target-language name to ISO 639-1 code,
  spanning every language the detector supports. Override via the
  `language_codes` argument of `wrong_language_guardrail`.

Agent-level guardrail configuration is documented under the
[Guardrails guide](../../guardrails/guardrail_hub.md).
