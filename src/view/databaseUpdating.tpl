<% include('src/view/header.tpl', title='Event List', path='', role=None) %>

    <main role="main" class="container">
      <div class="jumbotron">
        <h1>Database updating</h1>
        <p class="lead">Database updating, this page will refresh once the update has finished...</p>
      </div>
    </main>
    <script>
        setTimeout(function(){
            console.log('refreshing');
           window.location.reload(1);
        }, 5000);

    </script>

<% include('src/view/footer.tpl') %>
