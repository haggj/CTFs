use strict;
use warnings;

my $file = "/root/root.txt";

open(my $fh, '<', $file) or die "Could not open file '$file' $!";

while (my $line = <$fh>) {
  chomp $line;
  print "$line\n";
}

close($fh);
