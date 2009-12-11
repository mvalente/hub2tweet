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
</p>

<p>
This is beta, naturally, so please give it a whirl.  Report any issues you have
on our <a href="http://code.google.com/p/hub2tweet/issues/list">issues</a> page.
</p>

{% if user %}
<p>You are logged in as {{ user.screen_name }}.
  <a href="/logout">Log out</a>.
</p>    

<h4>Your linked feeds</h4>

{% if subscriptions %}
  <ul>
  {% for subscription in subscriptions %}
    <li>{{ subscription.topic|escape }}
    <br>
    <form action="/pubsub/delete_subscription" method=POST>
      <input type="hidden" name="id" value="{{ subscription.key.id|escape }}"/>
      <input type="submit" value="Delete"/>
    </form>
    </li>
  {% endfor %}
  </ul>
{% else %}
<p>No feeds added.</p>
{% endif %}

<h4>Add a linked feed</h4>
<p>Enter the URL of a PubSubHubBub-enabled Atom feed:<br/>
  <form action="/pubsub/add_subscription" method=POST>
    <input type="text" size=40 name="feed"
           style="border: 1px solid #ccc; font-size: 16px;"/>
    <input type="submit" value="Add" />
  </form>
</p>


{% else %}
<p style="text-align: center">
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
