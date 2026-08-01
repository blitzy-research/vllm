# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project

"""Unit tests for the ``bad_words`` field on the Completions request model.

These tests construct the request model directly: no server, no model, and no
accelerator is required.
"""

from vllm.entrypoints.openai.completion.protocol import CompletionRequest


def test_bad_words_forwarded_to_sampling_params():
    # A supplied list must reach SamplingParams unchanged.
    request = CompletionRequest(model="m", prompt="hi", bad_words=["foo", "bar"])
    sampling_params = request.to_sampling_params(
        max_tokens=16, logits_processor_pattern=None
    )
    assert sampling_params.bad_words == ["foo", "bar"]


def test_bad_words_defaults_to_empty_list():
    # An omitted parameter must yield [] at both layers, never None.
    request = CompletionRequest(model="m", prompt="hi")
    assert request.bad_words == []
    sampling_params = request.to_sampling_params(
        max_tokens=16, logits_processor_pattern=None
    )
    assert sampling_params.bad_words == []


def test_bad_words_parsed_from_json_payload():
    # The field must be a declared field, so a JSON body parses into it.
    request = CompletionRequest.model_validate(
        {"model": "m", "prompt": "hi", "bad_words": ["foo"]}
    )
    assert request.bad_words == ["foo"]


def test_bad_words_default_is_not_shared_between_requests():
    # default_factory=list must give each request its own list object.
    first = CompletionRequest(model="m", prompt="hi")
    second = CompletionRequest(model="m", prompt="hi")
    first.bad_words.append("foo")
    assert second.bad_words == []
