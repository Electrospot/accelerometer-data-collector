#!/usr/bin/env perl
use v5.12.0;
use warnings FATAL => "all";
use autodie;
use Data::Dumper;
use Scalar::Util qw/looks_like_number/;
use List::MoreUtils qw/all/;
$|=1;

# https://github.com/PunchThrough/bean-documentation/blob/master/app_message_types.md
# https://github.com/PunchThrough/bean-documentation/blob/master/serial_message_protocol.md
# gatttool -i hci1 -b B4:99:4C:1E:C5:05 --char-write-req --handle=0x002f --value=0100  --listen | perl test.pl

sub parse_gt{
    my $line = shift;
    if ($line =~ s/.*value:\s//){
        my ($header, @payload) = ($line =~ /([0-9a-f][0-9a-f])/g);
        $header = unpack "C", pack "H2", $header;

        my $is_start      = ($header & 0b10000000 );
        my $message_count = ($header & 0b01100000 ) >> 5;
        my $packet_count  = ($header & 0b00011111 );
        return (1, $is_start, $message_count, $packet_count, \@payload );
    }
    else{
        return (0);
    }
}

sub new_parser{
    my @gt_buffer;
    return sub {
        my $line = shift;
        my ($success, $is_start, $message_count, $packet_count, $bytes) = parse_gt $line;
        # say "$line, $is_start, $message_count, $packet_count";
        if (! $success){
            @gt_buffer = ();
            return "";
        }
        elsif ($is_start && @gt_buffer == 0){
            push @gt_buffer, {is_start => $is_start, message_count => $message_count, packet_count => $packet_count, bytes => $bytes};
        }
        elsif ($is_start && @gt_buffer != 0){
            @gt_buffer = (); 
            return "";
        }
        elsif (@gt_buffer != 0 && $gt_buffer[-1]{packet_count} -1 == $packet_count){
            push @gt_buffer, {is_start => $is_start, message_count => $message_count, packet_count => $packet_count, bytes => $bytes};
        }
        elsif (@gt_buffer != 0 && $gt_buffer[-1]{packet_count} -1 != $packet_count){
            @gt_buffer = (); 
            return "";
        }

        if ($packet_count == 0 && @gt_buffer != 0){
            my @gst_bytes = map { @{ $_->{bytes} } } @gt_buffer;
            my $length = unpack "C", pack "H2", $gst_bytes[0];
            my $reserved = unpack "C", pack "H2", $gst_bytes[1];
            my $app_message_id = @gst_bytes[2,3];
            my $crc = @gst_bytes[-2,-1];
            my @app_message = @gst_bytes[4 .. scalar(@gst_bytes) - 3];

            # say join ",", @gst_bytes;
            # say "$length, @app_message";

            @gt_buffer = ();
            return join "", map { unpack "A", pack "H2", $_} @app_message;
        }
    };
}

#######################################################################

use Pod::Usage;
use Getopt::Long;
use ZMQ::LibZMQ3;
use ZMQ::Constants ':all';

my $result = GetOptions (
    "acc-range|r=f"   => \(my $acc_range = 4.0),
    "interface|i=s"   => \(my $interface),
    "address|b=s"     => \(my $address),
    "pub-address|s=s" => \(my $pub_address = "tcp://127.0.0.1:5555"),
);
pod2usage(-verbose => 2, -noperldoc => 1) if (!$result);  

# setup socket
my $ctx = zmq_ctx_new() or die $!;
my $socket = zmq_socket($ctx, ZMQ_PUB) or die $!;
zmq_bind($socket, $pub_address) == 0 or die $!;

sub publish{
    my $data = shift;
    my $msg = zmq_msg_init_data("$data") or die $!;
    zmq_msg_send($msg, $socket) != -1 or die $!;
    zmq_msg_close($msg) == 0 or die $!;
}

# convert to actual gravitational units
sub to_grav_units{
    my $x = shift;
    return $x * (2 * 4.0 / 1024);
}

# if interface and mac address are given, read from gatttool instead of file
my $pipe = \*ARGV;
if ($interface and $address){
    open $pipe, "gatttool -i $interface -b $address --char-write-req --handle=0x002f --value=0100  --listen| ";
}

my $p = new_parser();
my $accum = "";
my $local_count = 0;
while (defined(my $line = <$pipe>)){
    # chomp $line;
    $accum .= $p->($line);
    if ($accum =~ s/([^;]+);//){
        my $serial_line = $1;
        my ($timestamp, $count, @xyz) = split /,/, $serial_line;

        if (@xyz == 24 and all {looks_like_number $_} @xyz){
            for (my $i = 0; $i < 8; $i++){
                # my $data = join "\t", $timestamp, $count - 8 + $i, $xyz[$i * 3 + 0], $xyz[$i * 3 + 1], $xyz[$i * 3 + 2];
                my $data = join "\t", 
                    $timestamp, 
                    ++$local_count, 
                    to_grav_units($xyz[$i * 3 + 0]), 
                    to_grav_units($xyz[$i * 3 + 1]), 
                    to_grav_units($xyz[$i * 3 + 2]);
                say $data;
                publish($data);
            }
        }
    }
}

close $pipe if ($interface and $address);
zmq_close($socket);
zmq_ctx_destroy($ctx);

__DATA__
Notification handle = 0x002e value: c3 41 00 00 00 31 39 37 34 32 2c 34 33 32 2c 38 32 2c 2d 31 
Notification handle = 0x002e value: 42 30 30 2c 34 30 2c 31 30 30 2c 2d 39 34 2c 2d 34 2c 38 33 
Notification handle = 0x002e value: 41 2c 2d 31 30 30 2c 32 32 2c 37 33 2c 2d 39 32 2c 38 2c 38 
Notification handle = 0x002e value: 40 39 2c 2d 31 30 30 2c 31 36 2c 0d 23 
Notification handle = 0x002e value: e1 20 00 00 00 39 33 2c 2d 39 37 2c 31 38 2c 38 31 2c 2d 38 
Notification handle = 0x002e value: 60 34 2c 32 38 2c 38 36 2c 2d 38 33 2c 33 34 3b 36 93 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 30 30 30 32 2c 34 34 30 2c 35 36 2c 2d 31 
Notification handle = 0x002e value: 42 30 39 2c 2d 32 37 2c 37 37 2c 2d 31 30 34 2c 31 37 2c 36 
Notification handle = 0x002e value: 41 30 2c 2d 31 30 33 2c 31 32 2c 37 33 2c 2d 31 30 33 2c 38 
Notification handle = 0x002e value: 40 2c 37 31 2c 2d 31 30 30 2c 30 91 54 
Notification handle = 0x002e value: e2 24 00 00 00 2c 37 36 2c 2d 31 30 39 2c 31 30 2c 36 32 2c 
Notification handle = 0x002e value: 61 2d 31 31 35 2c 34 2c 35 36 2c 2d 31 32 33 2c 2d 31 36 3b 
Notification handle = 0x002e value: 60 e9 2f 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 30 32 36 30 2c 34 34 38 2c 36 39 2c 2d 38 
Notification handle = 0x002e value: 42 37 2c 38 2c 33 31 2c 2d 31 30 38 2c 2d 38 33 2c 31 36 2c 
Notification handle = 0x002e value: 41 2d 31 31 30 2c 2d 31 31 31 2c 39 2c 2d 39 34 2c 2d 31 32 
Notification handle = 0x002e value: 40 35 2c 2d 34 30 2c 2d 38 39 2c 69 6e 
Notification handle = 0x002e value: e2 29 00 00 00 2d 31 37 37 2c 2d 32 36 2c 2d 36 38 2c 2d 31 
Notification handle = 0x002e value: 61 32 35 2c 31 2c 2d 36 39 2c 2d 37 39 2c 32 39 2c 2d 37 32 
Notification handle = 0x002e value: 60 2c 2d 33 34 3b d3 bc 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 30 35 31 38 2c 34 35 36 2c 38 34 2c 2d 37 
Notification handle = 0x002e value: 42 37 2c 32 36 2c 35 32 2c 2d 34 37 2c 31 30 30 2c 31 32 34 
Notification handle = 0x002e value: 41 2c 2d 38 33 2c 36 31 2c 39 38 2c 2d 39 33 2c 31 31 2c 31 
Notification handle = 0x002e value: 40 30 31 2c 2d 36 34 2c 31 37 2c e4 b3 
Notification handle = 0x002e value: e1 1f 00 00 00 37 38 2c 2d 35 37 2c 34 37 2c 38 34 2c 2d 37 
Notification handle = 0x002e value: 60 32 2c 32 31 2c 38 36 2c 2d 36 39 2c 36 3b db b4 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 30 37 37 36 2c 34 36 34 2c 33 32 2c 2d 32 
Notification handle = 0x002e value: 42 33 2c 31 30 37 2c 37 37 2c 2d 36 38 2c 38 35 2c 36 38 2c 
Notification handle = 0x002e value: 41 2d 36 33 2c 39 35 2c 36 36 2c 2d 35 34 2c 39 39 2c 37 37 
Notification handle = 0x002e value: 40 2c 2d 34 38 2c 31 30 30 2c 35 c6 79 
Notification handle = 0x002e value: e1 1f 00 00 00 30 2c 2d 33 32 2c 39 35 2c 35 35 2c 2d 33 31 
Notification handle = 0x002e value: 60 2c 39 32 2c 34 31 2c 2d 32 39 2c 38 39 3b 78 89 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 31 30 33 32 2c 34 37 32 2c 31 36 2c 2d 32 
Notification handle = 0x002e value: 42 36 2c 31 32 30 2c 31 38 2c 2d 32 31 2c 2d 31 32 38 2c 31 
Notification handle = 0x002e value: 41 31 2c 2d 31 39 2c 2d 31 32 38 2c 31 30 2c 2d 32 37 2c 31 
Notification handle = 0x002e value: 40 32 37 2c 31 32 2c 2d 32 35 2c 53 3f 
Notification handle = 0x002e value: e2 27 00 00 00 31 32 30 2c 31 36 2c 2d 31 39 2c 31 31 39 2c 
Notification handle = 0x002e value: 61 31 35 2c 2d 31 37 2c 31 32 33 2c 31 33 2c 2d 31 39 2c 31 
Notification handle = 0x002e value: 60 32 30 3b c9 08 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 31 32 39 33 2c 34 38 30 2c 36 2c 2d 31 33 
Notification handle = 0x002e value: 42 2c 31 32 35 2c 31 31 2c 2d 32 30 2c 2d 31 32 34 2c 39 2c 
Notification handle = 0x002e value: 41 2d 31 38 2c 2d 31 32 36 2c 38 2c 2d 31 39 2c 31 32 34 2c 
Notification handle = 0x002e value: 40 38 2c 2d 31 34 2c 31 32 33 2c aa a7 
Notification handle = 0x002e value: e1 20 00 00 00 37 2c 2d 31 36 2c 31 32 35 2c 35 2c 2d 31 34 
Notification handle = 0x002e value: 60 2c 31 32 35 2c 34 2c 2d 31 32 2c 31 32 35 3b 96 91 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 31 35 35 31 2c 34 38 38 2c 31 32 2c 2d 32 
Notification handle = 0x002e value: 42 30 2c 31 30 35 2c 34 2c 2d 31 32 2c 31 32 30 2c 39 2c 2d 
Notification handle = 0x002e value: 41 31 33 2c 31 31 37 2c 38 2c 2d 37 2c 31 32 31 2c 36 2c 2d 
Notification handle = 0x002e value: 40 31 30 2c 31 32 30 2c 31 35 2c 63 00 
Notification handle = 0x002e value: e1 1f 00 00 00 2d 31 34 2c 31 31 36 2c 32 31 2c 2d 36 2c 31 
Notification handle = 0x002e value: 60 31 36 2c 32 32 2c 2d 31 32 2c 31 31 30 3b 05 c1 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 31 38 31 31 2c 34 39 36 2c 2d 31 2c 2d 31 
Notification handle = 0x002e value: 42 30 2c 31 32 32 2c 31 36 2c 2d 32 33 2c 31 32 35 2c 2d 38 
Notification handle = 0x002e value: 41 2c 2d 33 30 2c 2d 31 30 37 2c 38 2c 2d 31 37 2c 31 31 34 
Notification handle = 0x002e value: 40 2c 2d 39 2c 2d 39 2c 31 32 34 b9 14 
Notification handle = 0x002e value: e1 21 00 00 00 2c 33 2c 2d 39 2c 31 32 33 2c 2d 34 2c 2d 31 
Notification handle = 0x002e value: 60 30 2c 31 32 32 2c 30 2c 2d 31 31 2c 31 32 32 3b 8a 4a 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 32 30 36 39 2c 35 30 34 2c 2d 31 2c 2d 31 
Notification handle = 0x002e value: 42 30 2c 31 32 32 2c 2d 31 2c 2d 31 30 2c 31 32 33 2c 2d 31 
Notification handle = 0x002e value: 41 2c 2d 31 30 2c 31 32 33 2c 2d 31 2c 2d 31 31 2c 31 32 32 
Notification handle = 0x002e value: 40 2c 2d 31 2c 2d 31 30 2c 31 32 cc 0f 
Notification handle = 0x002e value: e2 23 00 00 00 32 2c 2d 31 2c 2d 31 30 2c 31 32 32 2c 30 2c 
Notification handle = 0x002e value: 61 2d 31 30 2c 31 32 32 2c 30 2c 2d 31 31 2c 31 32 32 3b ee 
Notification handle = 0x002e value: 60 bb 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 32 33 32 39 2c 35 31 32 2c 2d 31 2c 2d 31 
Notification handle = 0x002e value: 42 31 2c 31 32 32 2c 30 2c 2d 39 2c 31 32 33 2c 30 2c 2d 31 
Notification handle = 0x002e value: 41 30 2c 31 32 32 2c 2d 31 2c 2d 31 30 2c 31 32 32 2c 2d 31 
Notification handle = 0x002e value: 40 2c 2d 31 30 2c 31 32 32 2c 2d 08 c1 
Notification handle = 0x002e value: e1 21 00 00 00 31 2c 2d 31 31 2c 31 32 32 2c 2d 31 2c 2d 31 
Notification handle = 0x002e value: 60 31 2c 31 32 31 2c 30 2c 2d 31 30 2c 31 32 32 3b 2e 92 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
Notification handle = 0x002e value: c3 41 00 00 00 32 32 35 38 39 2c 35 32 30 2c 2d 31 2c 2d 31 
Notification handle = 0x002e value: 42 31 2c 31 32 32 2c 2d 31 2c 2d 31 30 2c 31 32 32 2c 2d 31 
Notification handle = 0x002e value: 41 2c 2d 31 30 2c 31 32 33 2c 2d 31 2c 2d 31 30 2c 31 32 32 
Notification handle = 0x002e value: 40 2c 2d 31 2c 2d 39 2c 31 32 32 c3 dd 
Notification handle = 0x002e value: e2 23 00 00 00 2c 2d 31 2c 2d 31 30 2c 31 32 33 2c 30 2c 2d 
Notification handle = 0x002e value: 61 31 30 2c 31 32 32 2c 2d 31 2c 2d 31 30 2c 31 32 32 3b 94 
Notification handle = 0x002e value: 60 86 
Notification handle = 0x002e value: 80 03 00 00 00 0d 73 2e 
Notification handle = 0x002e value: a0 03 00 00 00 0a 94 5e 
