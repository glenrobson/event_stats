<!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">-->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">

    <title>{{ title }}</title>

    <link href="{{ path }}static/css/bootstrap-4-hover-navbar.css" rel="stylesheet">
</style>
</head>
<body>
<!-- navbar navbar-expand-md navbar-dark bg-dark mb-4-->
<nav class="navbar navbar-expand-md navbar-dark bg-dark btco-hover-menu">
    <a class="navbar-brand" href="https://iiif.io"><img src="https://i0.wp.com/www.clir.org/wp-content/uploads/sites/6/2016/09/IIIF-logo-500w.png?w=500&ssl=1" height="30px"/></a>
    <a class="navbar-brand" href="/index.html">IIIF Events dashboard</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    % if role == 'admin':
        <div class="navbar-collapse collapse w-100 order-2 dual-collapse2">
            <ul class="navbar-nav m1-auto">
                <li class="nav-item">
                    <a class="nav-link" href="/admin.html">Admin</a>
                </li>
            </ul>    
        </div>
    % end 
    <div class="navbar-collapse collapse w-100 order-3 dual-collapse2">
        <ul class="navbar-nav m1-auto" style="right: 20px; position: absolute;">
            <li class="nav-item">
                <a class="nav-link" href="/logout"></a>
            </li>
        </ul>    
    </div>
</nav>
