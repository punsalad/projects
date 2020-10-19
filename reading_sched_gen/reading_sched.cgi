#!/usr/bin/perl
#
# generate page-goal html (calendar format)
#

use local::lib;

use strict;
use warnings;

use CGI;
use CGI::Carp 'fatalsToBrowser';
use Const::Fast;
use English qw( -no_match_vars );
use HTML::Template;
use POSIX;
use Time::Piece;
use Time::Seconds;
use version; our $VERSION = qv('v2020.10.19');

const my $DAYS_PER_WEEK => 7;

my $q             = CGI->new;
my $template_file = '/home/pas/public_html/misc/templates/cal_bookmark.tmpl';
my $template      = HTML::Template->new(
    filename  => $template_file,
    associate => $q,
    utf8      => 1,
);

#
# get CGI params ....
#
( my $title = $q->param('title') ) or die "Must enter title\n";

my $startdate_str = $q->param('startdate');
( my $startdate
        = eval { Time::Piece->strptime( $startdate_str, '%Y-%m-%d' ) } )
    or die "Can't parse startdate\n";

my $startpage = $q->param('startpage');
( $startpage =~ /^[-+]?\d+/ ) or die "Sorry, can't parse startpage\n";

my $page0 = $startpage - 1;    # "pages already read"

my $endpage = $q->param('endpage');
( $endpage =~ /^[-+]?\d++$/ ) or die "Sorry, can't parse endpage\n";
my $npages = $endpage - $page0;
( $npages > 0 ) || die "Sorry, end must come after start\n";

my $ndays;
my $enddate;
my $ppd = 0;

#
# if number of scheduled days is specified, calculate the end date.
#
if ( $q->param('ndays') ) {
    $ndays = $q->param('ndays');
    ( $ndays =~ /^\d+$/ && $ndays > 0 ) or die "Invalid days parameter\n";
    $enddate = ( $ndays - 1 ) * ONE_DAY + $startdate;
}
#
# if the end date is specified, calculate number of days in schedule...
#
elsif ( $q->param('enddate') ) {
    my $enddate_str = $q->param('enddate');
    ( $enddate = eval { Time::Piece->strptime( $enddate_str, '%Y-%m-%d' ) } )
        or die "Can't parse enddate\n";

    ( $startdate < $enddate )
        or die "Sorry, end date must be after start date\n";
    $ndays = 1 + ( $enddate - $startdate ) / ONE_DAY;
}
#
# otherwise if pages/day is specified
#
elsif ( $q->param('ppd') ) {
    $ppd = $q->param('ppd');
    ( $ppd =~ /^\d+$/ && $ppd > 0 ) or die "Invalid pages/day parameter\n";
    $ndays   = ceil( $npages / $ppd );
    $enddate = ( $ndays - 1 ) * ONE_DAY + $startdate;
}
#
# oh oh
#
else {
    die "Can't figure out end of schedule\n";
}

#
# start calendar on Sunday...
#
my $dayno = 1 - $startdate->day_of_week;
my $dt    = $startdate - $startdate->day_of_week * ONE_DAY;

#
# loop over as many weeks as needed...
#
my @wl = ();
while ( $dt <= $enddate ) {
    my @dl = ();
    #
    # loop over days of week...
    #
    for ( 1 .. $DAYS_PER_WEEK ) {
        my $pg;
        if ( $dayno > $ndays || $dayno <= 0 ) {
            $pg = '&nbsp;';
        }
        elsif ( $dayno == $ndays ) {    # last day, last page
            $pg = sprintf '%d', $endpage;
        }
        else {
            $pg
                = ( $ppd > 0 )
                ? sprintf '%d', $page0 + $dayno * $ppd
                : sprintf '%.0f', $page0 + $dayno / $ndays * $npages;
        }
        my $ddd = $dt->mon . q{/} . $dt->day_of_month;
        push @dl, { 'date' => $ddd, 'goal' => $pg, };
        $dt += ONE_DAY;
        $dayno++;
    }
    push @wl, { 'days' => \@dl };
}

$template->param( 'weeks' => \@wl );
$template->param( 'title' => $title );

print "Content-Type: text/html\n\n";
print $template->output;
