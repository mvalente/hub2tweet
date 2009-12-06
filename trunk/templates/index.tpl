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

    <p>(Well, it will when we're done with it.  It's still a work in progress.  But
      you can log in and tweet from hub2tweet for now.)</p>

    {% if user %}
      <p>You are logged in as {{ user.screen_name }}.
        <a href="/logout">Log out</a>.
      </p>    

      <p>
        <form action="/tweet" method=POST>
          <h4>Tweet from hub2tweet</h4>
          <div style="padding: 0px 30px;">
            <textarea style="width: 100%; border: 1px solid#ccc; font-size: 16px" 
                      rows="4" name="tweet"></textarea>
            <div style="text-align: right">
              <input type="submit" value="update">
            </div>
          </div>
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
