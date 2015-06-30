#!/usr/bin/env perl
use v5.12.0;
use warnings FATAL => "all";
use autodie;
use Data::Dumper;
use ZMQ::LibZMQ3;
use ZMQ::Constants ':all';
use Time::HiRes qw/usleep/;
use Pod::Usage;
use Getopt::Long;

use Cwd qw/abs_path/;
use File::Basename qw/dirname/;
use File::Spec::Functions qw/catfile/;

my $result = GetOptions (
    "input-file|i=s" => \(my $input_file = catfile(dirname(abs_path($0)), "dummy.txt")),
    "no-repeat|n"    => \(my $no_repeat),
    "port|p=i"       => \(my $zeromq_port = 5555),
    "binary|b" => \(my $binary),
    "zeromq-target|t=s" => \(my $zeromq_target = "tcp://127.0.0.1"),
);
pod2usage(-verbose => 2, -noperldoc => 1) if (!$result);  

# don't sleep if it is a serial port
my $sleep = -f $input_file ? 10_000 : 0;

### initialize
my $ctx = zmq_ctx_new() or die $!;
my $socket = zmq_socket($ctx, ZMQ_PUB) or die $!;
zmq_bind($socket, "$zeromq_target:$zeromq_port") == 0 or die $!;

if (! $binary){
    while (1){
        open my $fh, '<:crlf', $input_file;
        while (defined(my $line = <$fh>)){
            chomp $line;
            say $line;
            my $msg = zmq_msg_init_data($line) or die $!;
            zmq_msg_send($msg, $socket) != -1 or die $!;
            zmq_msg_close($msg) == 0 or die $!;
            usleep($sleep) if $sleep;
        }
        close $fh;
        break if ($no_repeat);
    }
}
else{
    my $msg_sent = 0;
    while (1){
        my $buf = "";
        open my $fh, '<', $input_file;

        # 8 bytes per frame
        # each starts with 0080 (-32768, which is unlikely)
        # then 3 16 bit unsigned integers (little endian)
        while (sysread($fh, $buf, 1024, length($buf)) > 0){
            INNER:
            while (1){
                # if there's 0 to 6 
                $buf =~ s/^.*?(?=\x00\x80)//;
                if (length($buf) > 8){
                    my $frame = substr $buf, 0, 8, '';
                    my ($header, $x, $y, $z) = unpack "s<s<s<s<", $frame;
                    my $line = join "\t", $header, $msg_sent, $x, $y, $z; # first col ignored...
                    say $line;

                    my $msg = zmq_msg_init_data($line) or die $!;
                    zmq_msg_send($msg, $socket) != -1 or die $!;
                    zmq_msg_close($msg) == 0 or die $!;
                    $msg_sent++;
                    usleep($sleep) if $sleep;
                }
                else{
                    last INNER;
                }
            }
        }

        close $fh;
        break if ($no_repeat);
    }
}

zmq_close($socket) == 0 or die $!;
zmq_ctx_destroy($ctx) == 0 or die $!;
