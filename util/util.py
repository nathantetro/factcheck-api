import json

from flask import url_for


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def get_endpoints(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)
    return links


def convert_factchecks_to_json(factChecks):
    jsonFactChecks = json.dumps(factChecks, indent=4, ensure_ascii=False).encode('utf8')
    return jsonFactChecks.decode()
