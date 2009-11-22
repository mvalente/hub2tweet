<html>
  <body>
  <p>Current consumer key: {{consumer_key}}</p>
  <p>Current consumer secret: {{consumer_secret}}</p>
  <h2>Update application config:</h2>
  <form action="/admin/oauth_config" method="POST">
    Consumer key <input name="consumer_key"><br>
    Consumer secret <input name="consumer_secret"><br>
    <input type="submit">
  </form>
   </body>
</html>
