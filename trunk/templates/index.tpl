{% extends "base.tpl" %}

{% block content %}
  <h3>Welcome to hub2tweet!</h3>
  <p>
    hub2tweet is an <a href="http://code.google.com/p/hub2tweet/">
    open-source project</a> that allows you to link
    <a href="http://code.google.com/p/pubsubhubbub/">PubSubHubBub</a>-enabled 
    <a href="http://en.wikipedia.org/wiki/Atom_(standard)">Atom</a> feeds to
    your Twitter account.  Updates to your feeds will appear on Twitter
    instantly!

    {% if user %}
      <p>You are logged in as {{ user.screen_name }}.
        <a href="/logout">Log out</a>.
      </p>    


    {% else %}
      <p>
        <a href="/authenticate">
          <img src="/images/sign_in_twitter.png" />
        </a>
      </p>
    {% endif %}

  <div style="text-align: right;">
    <a href="http://code.google.com/appengine/">
      <img src="http://code.google.com/appengine/images/appengine-noborder-120x30.gif"
           alt="Powered by Google App Engine" />
    </a>
  </div>
{% endblock %}
