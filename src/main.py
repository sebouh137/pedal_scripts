#!/usr/bin/env python3
import global_settings, scipy.signal

"""
Modified from

https://app.assembla.com/spaces/portaudio/git/source/master/test/patest_wire.c

"""
import argparse

import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-c', '--channels', type=int, default=1,
    help='number of channels')
parser.add_argument('--dtype', help='audio data type')
parser.add_argument('--samplerate', default=48000., type=float, help='sampling rate')
parser.add_argument('--blocksize', default=30, type=int, help='block size')
parser.add_argument('--latency', default=0.033, type=float, help='latency in seconds')
parser.add_argument('--load', type=str, help='load the pedalboard configuration from a file')
parser.add_argument('--mute',action='store_true', help='mute the pedalboard at the beginning of the program')
args = parser.parse_args(remaining)


global_settings.samplerate=args.samplerate
global_settings.channels =args.channels
#def callback(indata, outdata, frames, time, status):
#    if status:
#        print(status)
#    outdata[:] = indata


#module = __import__(args.scriptname)
#callback = getattr(module, "callback")

import effect_chain
chain=effect_chain.EffectChain()
if(args.load):
    chain.load(args.load)
callback=chain

if args.mute:
    chain.mute=True


    
try:
    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=args.channels, callback=callback):
        #print('#' * 80)
        #print('press Return to quit')
        #print('#' * 80)
        #input()
        chain.cli()
#except KeyboardInterrupt:
#    parser.exit('')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
