Hello there, here are the open issues and pull requests of the week! :gift:

{% for _, issues in data %}
• `{{ issues[0]['repository']['name'] }}` ({{ issues[0]['repository']['html_url'] }})
{% for issue in issues %}
_{{ issue['title'] }}_ ({{ issue['html_url'] }})
{% endfor %}

{% endfor %}
