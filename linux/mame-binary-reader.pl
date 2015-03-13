#!/usr/bin/env perl
use v5.12.0;
use warnings FATAL => "all";
use autodie;
use Data::Dumper;
use Expect;
use Pod::Usage;
use Getopt::Long;
use ZMQ::LibZMQ3;
use ZMQ::Constants ':all';

my $result = GetOptions (
    "acc-range|r=f"   => \(my $acc_range = 16.0),
    "interface|i=s"   => \(my $interface),
    "address|b=s"     => \(my $address),
    "port|p=i"        => \(my $pub_port = 5555),
    "output-file|o=s" => \(my $output_file),
);
pod2usage(-verbose => 2, -noperldoc => 1) if (!$result || ! $interface || ! $address);  

#######################################################################
# zeromq output

my $pub_address = "tcp://127.0.0.1:$pub_port";
my $ctx = zmq_ctx_new() or die $!;
my $socket = zmq_socket($ctx, ZMQ_PUB) or die $!;
zmq_bind($socket, $pub_address) == 0 or die $!;

sub publish{
    my $data = shift;
    my $msg = zmq_msg_init_data("$data") or die $!;
    zmq_msg_send($msg, $socket) != -1 or die $!;
    zmq_msg_close($msg) == 0 or die $!;
}

#######################################################################
# file output

my $output_fh;
if ($output_file){
    open $output_fh, '>', $output_file;
}

#######################################################################
# expect

my $exp = Expect->spawn('gatttool', '-i', $interface, '-b', $address, '-I') 
    or die "Cannot spawn";

$exp->expect(1, "LE");
$exp->send("connect\n");
$exp->expect(1, "Connection succesful");
sleep 1;
$exp->send("char-write-cmd 0x0034 0100\n");
sleep 1;

my $num_notifications = 0;
while (1){
    $exp->expect(undef, 
        [ qr/.*(0x00[0-9a-f]{2}) value: ([^\n]+)\n/ => sub { 
                my @ml = $exp->matchlist;
                on_message(@ml);
                say $num_notifications++;
                # exp_continue();
            } ],
    );
}

sub on_message{
    state $absolute_count = 0;
    my ($scratch_handle, $line) = @_;

    my @packet = split /\s/, $line;
    # say "PACKET = " . join "-", @packet;
    # say "PACKETSIZE = " . scalar @packet;
    my ($millis, @xyz) = unpack "s<s<*", pack "H40", join "", @packet;
    # say "XYZ size = " . scalar @xyz;
    while (@xyz >= 3){
        my $x = to_grav_units(shift @xyz);
        my $y = to_grav_units(shift @xyz);
        my $z = to_grav_units(shift @xyz);
        my $s = join "\t", $absolute_count, $absolute_count, $x,$y,$z;


        publish($s);
        say $output_fh $s if $output_fh;
        say $s;

        $absolute_count++;
    }
}

sub to_grav_units{
    my $x = shift;
    return $x * (2 * $acc_range / 8192);
}

if ($output_file){
    close $output_fh;
}

=head1 singlescratch-to-zmq.pl 

Usage examples:

 beanbinary-capture.pl -i hci1 -b B4:99:4C:1E:C0:D0 

=cut

