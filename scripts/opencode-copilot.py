#!/usr/bin/env python3

import argparse
import json
import os
import sys
from typing import NoReturn


def resolve_value(value: str) -> str:
    """Support {env:NAME} syntax."""
    if isinstance(value, str) and value.startswith("{env:") and value.endswith("}"):
        env_name = value[5:-1]
        return os.environ.get(env_name, "")
    return value


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description="Launch Copilot CLI with model settings from opencode config")
    parser.add_argument("model", nargs="?", default="kimi", help="Model name (default: kimi)")
    parser.add_argument("--config", default="~/.config/opencode/opencode.json", help="Path to opencode config")
    parser.add_argument("--list", action="store_true", help="List all known models")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass through to copilot")
    args = parser.parse_args()

    config_path = os.path.expanduser(args.config)

    with open(config_path) as f:
        config = json.load(f)

    if args.list:
        print("Known models:")
        for provider_name, provider in config.get("provider", {}).items():
            for model_name in provider.get("models", {}):
                print(f"  {model_name}")
        sys.exit(0)

    model_name = args.model

    provider_info = None
    model_info = None

    for provider_name, provider in config.get("provider", {}).items():
        models = provider.get("models", {})
        if model_name in models:
            provider_info = provider
            model_info = models[model_name]
            break

    if provider_info is None:
        print(f"Model '{model_name}' not found in config", file=sys.stderr)
        sys.exit(1)

    options = provider_info.get("options", {})
    limits = model_info.get("limit", {})

    env = os.environ.copy()
    env["COPILOT_PROVIDER_BASE_URL"] = resolve_value(options.get("baseURL", ""))
    env["COPILOT_PROVIDER_API_KEY"] = resolve_value(options.get("apiKey", ""))
    env["COPILOT_MODEL"] = model_name
    env["COPILOT_PROVIDER_MAX_PROMPT_TOKENS"] = str(limits.get("context", ""))
    env["COPILOT_PROVIDER_MAX_OUTPUT_TOKENS"] = str(limits.get("output", ""))

    os.execvpe("copilot", ["copilot"] + args.args, env)


if __name__ == "__main__":
    main()
