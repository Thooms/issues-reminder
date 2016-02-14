Hello everyone! Here are the open issues and pull requests of the week!

{% for provider in data %}
### From {{ provider.name }}
{% for repo in provider.repos %}
• {{ repo.name }} ({{ repo.url }})
{% for issue in repo.issues %}
{{ issue.author}} | {{ issue.title }} ({{ issue.url }})
{% endfor %}

{% endfor %}
{% endfor %}
