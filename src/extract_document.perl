#!/usr/bin/perl -w

my $inf;
my $holdTerminator = $/;
undef $/;
open $inf, "<" . $ARGV[0];
my $buf = <$inf>;
#print $buf;
$/ = $holdTerminator;
undef $holdTerminator;

$buf =~ /\\begin\{document\}(.*)\\end\{document\}/s;
my $documentBody = $1;
while ($documentBody =~ /\R\s*\R([A-Za-z,.;\r\n])*\s*\R\s*\R/sg) {
    print $1;
}

