#!/usr/bin/perl
##
##  printenv -- demo CGI program which just prints its environment
##

use MIME::Base64;
use CGI qw/:standard *table *td *tr *ul/;
use utf8;
use encoding 'utf8';

print header(-type=>'text/html',-charset=>'utf-8'),
      start_html(-title=>'SWAMID Test SP',
                 -script=>[{-type=>'javascript',-src=>'//code.jquery.com/jquery-1.11.2.min.js'},
                           {-type=>'javascript',-src=>'//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js'}],
                 -head=>[meta({-http_equiv => 'Content-Type',
                               -content    => 'text/html; charset=utf-8'}),
                         Link({-rel=>'stylesheet',-href=>'//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css'}),
                         ]),
      '<div class="container">',
      h1({-class=>'page-header'},'Federation Authentication Information');

print <<EOH;
<div class="panel panel-default">
<div class="panel-heading">Attributes</div>
<div class="panel-body">
<p>
   These attributes were send from the Identity Provider ($ENV{Shib_Identity_Provider}). The 'eppn' attribute if present is often
   used as a permanent identifier for you.
</p>
</div>
<table class="table table-striped table-bordered">
EOH

foreach $var (sort(keys(%ENV))) {
    #next unless ($var =~ /^[a-z]/ || $var =~ /^Shib/);
    next unless $var =~ /^[a-z]/;
    $val = $ENV{$var};
    $val =~ s|\n|\\n|g;
    $val =~ s|"|\\"|g;
    print "<tr><th>$var</th><td>$val</td></tr>\n";
}
print "</table></div>\n";

print h2('See Also');
print<<EOH;
   <p>
     This information is mostly meant to be interesting for expert users. Access to logs is restricted. Contact operations@swamid.se for access
   </p>
   <ul>
      <li><a href="/Shibboleth.sso/Session">Session</a></li>
      <li><a href="/Shibboleth.sso/Metadata">Metadata</a></li>
      <li><a href="/Shibboleth.sso/Logout">Logout</a></li>
      <li><a href=\"/logs/\">shibboleth logs</a></li>
      <li><a href=\"/info\">server info</a></li>
      <li><a href=\"/status\">server status</a></li>
   </ul>
EOH

print '</div>',end_html;
