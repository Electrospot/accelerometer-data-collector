#!/usr/bin/env perl
use v5.12.0;
use warnings FATAL => "all";
use autodie;
use Data::Dumper;
use ZMQ::LibZMQ3;
use ZMQ::Constants ':all';
use Time::HiRes qw/usleep/;
# ZMQ_PUB ZMQ_SUB ZMQ_PUSH ZMQ_PULL ZMQ_REQ ZMQ_REP
use Pod::Usage;
use Getopt::Long;

use Cwd qw/abs_path/;
use File::Basename qw/dirname/;
use File::Spec::Functions qw/catfile/;

my $result = GetOptions (
    "input-file|i=s" => \(my $input_file = catfile(dirname(abs_path($0)), "dummy.txt")),
    "no-repeat|n"    => \(my $no_repeat),
    "port|p=i"       => \(my $zeromq_port = 5555),
    "zeromq-target|t=s" => \(my $zeromq_target = "tcp://127.0.0.1"),
);
pod2usage(-verbose => 2, -noperldoc => 1) if (!$result);  

### initialize
my $ctx = zmq_ctx_new() or die $!;
my $socket = zmq_socket($ctx, ZMQ_PUB) or die $!;
zmq_bind($socket, "$zeromq_target:$zeromq_port") == 0 or die $!;

while (1){
    open my $fh, '<:crlf', $input_file;
    while (defined(my $line = <$fh>)){
        chomp $line;
        say $line;
        my $msg = zmq_msg_init_data($line) or die $!;
        zmq_msg_send($msg, $socket) != -1 or die $!;
        zmq_msg_close($msg) == 0 or die $!;
        usleep(10_000);
    }
    close $fh;
    break if ($no_repeat);
}

zmq_close($socket) == 0 or die $!;
zmq_ctx_destroy($ctx) == 0 or die $!;
