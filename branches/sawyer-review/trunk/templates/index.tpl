<html>
<body>
<p>Hello world!</p>
<p><a href="/authenticate">Authentication test</a></p>
{% if user %}
<p>You are logged in as {{ user.screen_name }}.</>
{% endif %}
</body>
<html/>
