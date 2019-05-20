<% include('src/view/header.tpl', title='Göttingen', path='../', role=None) %>

    <main role="main" class="container">
      <div class="jumbotron">
        <h1>Göttingen Conference Statistics</h1>
        <p>Details:</p>
        <ul>
            <li><a href="https://iiif.io/event/2019/goettingen/">Overview / Logistics</a></li>
            <li><a href="https://iiif.io/event/2019/goettingen/showcase/">Monday 24th of June - showcase</a></li>
            <li><a href="https://iiif.io/event/2019/goettingen/workshops/">Tuesday 25th of June - Workshops</a></li>
            <li><a href="https://iiif.io/event/2019/goettingen/wednesday/">Wednesday 26th of June - Conference</a></li>
            <li><a href="https://iiif.io/event/2019/goettingen/thursday/">Thursday 27th of June - Conference</a></li>
            <li><a href="https://iiif.io/event/2019/goettingen/friday/">Friday 28th of June - Conference</a></li> 
        </ul>
        <%
        
            updateMsg = ''
            if updateDiff == '0':
                updateMsg = 'Database updated less than 1 minute ago.'
            elif updateDiff == '1':
                updateMsg = 'Database updated 1 minute ago.'
            else:
                updateMsg = 'Database updated {} minute ago.'.format(updateDiff)
            end    
        %>
        <p>{{ updateMsg}} Database updates every 30mins.</p>
        <h2>Showcase</h2>
        <p class="lead">Showcase attendees</p>
        <p><b>Total: </b>{{ ticket_counts['IIIF Showcase - Monday, June 24th'] }} / 270</p>
        <div id="showcase_attendees"></div>

        <br/>
        <h2>Conference</h2>
        <p class="lead">Ticket types</p>
        <p><b>Totals: </b>
            <ul>
                <li><b>Workshop Only: </b> {{ ticket_counts['Workshop Only - Tuesday, June 25th']}}</li>
                <br/>
                <li><b>Non-IIIF Consortium: </b> {{ ticket_counts['Non-IIIF Consortium Member']}}</li>
                <li><b>Consortium: </b> {{ ticket_counts['IIIF Consortium Member']}}</li>
                <li><b>Sponsor: </b> {{ ticket_counts['Sponsor Ticket']}}</li>
                <li><b>Staff: </b> {{ ticket_counts['IIIF Staff Ticket']}}</li>
                <li><b>Host: </b> {{ ticket_counts[u'G\xf6ttingen Host Ticket']}}</li>
                <%
                    totalCount = 0
                    for key in ticket_counts:
                        if key != 'IIIF Showcase - Monday, June 24th' and key != 'Workshop Only - Tuesday, June 25th':
                            totalCount += ticket_counts[key]
                        end    
                    end
                %>
                <li><b>Total Conference: </b> {{ totalCount }} / 270 </li>
            </ul>
        </p>
        <div id="conference_attendees"></div>
        <br/>
        <p>Ticket types:</p>
        <div id="conference_types"></div>

        <br/>
        <p>Workshops:</p>
        <div id="workshops"></div>
      </div>
    </main>

<!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script type="text/javascript">
    
    // Load the Visualization API and the piechart package.
    google.charts.load('current', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawCharts);
      
    function drawCharts() {
        drawChart('showcase-attendees.json', 'line', 'showcase_attendees');
        drawChart('conference-attendees.json', 'line', 'conference_attendees');
        drawChart('conference-types.json', 'pie', 'conference_types');
        drawChart('workshop-attendees.json', 'column', 'workshops');
    }

    function drawChart(data, type, dest) {
        fetch(data)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' + response.status  + ' for ' + data);
                return;
              }

              // Examine the text in the response
              response.json().then(function(jsonData) {
                  // Create our data table out of JSON data loaded from server.
                  var data = new google.visualization.DataTable(jsonData);

                  destEl = document.getElementById(dest);  
                  // Instantiate and draw our chart, passing in some options.
                  var chart = null;
                  var options = {};
                  if (type == 'pie'){ 
                    chart = new google.visualization.PieChart(destEl);
                    options = {
                        width: 400,
                        height: 240
                    };
                  } else if (type == 'line') {
                    chart = new google.visualization.LineChart(destEl);
                    options = {
                        height: 400,
                        title: 'Attendees',
                        curveType: 'function',
                        legend: { position: 'bottom' },
                        axes: {
                            x: {
                                0: {side: 'top'}
                               }
                        }
                     }   
                    } else if (type == 'column') {
                        chart = new google.visualization.ColumnChart(destEl);
                        options = {
                            title: 'Workshops',
                            height: 600,
                            bar: {groupWidth: "95%"},
                            legend: { position: "top", maxLines: 3 },
                            isStacked: true
                        };
                      }
                  chart.draw(data, options);
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch Error :-S', err);
          });
    }
</script>
    

<% include('src/view/footer.tpl') %>
