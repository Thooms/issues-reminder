Hello @everyone ! Here are the open issues and pull requests of the week! :gift:

{% for provider in data %}
### From {{ provider.name }}
{% for repo in provider.repos %}
{% if repo.issues %}
• `{{ repo.name }}` ({{ repo.url }})
{% for issue in repo.issues %}
_{{ issue.author}}_ *{{ issue.title }}* ({{ issue.url }})
{% endfor %}
{% endif %}

{% endfor %}
{% endfor %}
