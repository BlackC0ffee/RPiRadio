# RPiRadio

Turn up the sound with a small Headless Raspberry Pi Internet receiver using a Bluetooth speaker

This is an abstract explanation  of the project more information can be found [on my blog](https://blog.stijn-dhaese.be/2020/06/rpiradio/)

## Install Software

```bash
sudo apt --yes install mpd mpc pulseaudio-module-bluetooth`
```

## Configuration

### PulseAudio

Add users to the correct groups

```bash
sudo gpasswd -a pi pulse-access
sudo gpasswd -a root pulse-access
sudo gpasswd -a pulse audio
sudo gpasswd -a pulse bluetooth
```

Change the autospawn variable in ``/etc/pulse/client.conf``

```bash
autospawn = no
```

In ``/etc/pulse/system.pa``

Add:

> ```bash
> .ifexists module-bluetooth-policy.so
> load-module module-bluetooth-policy
> .endif
> .ifexists module-bluetooth-discover.so
> load-module module-bluetooth-discover
> .endif
> ```

 Remove:

> ```bash
> load-module module-suspend-on-idle
> ```

Disable all services

```bash
sudo systemctl --global disable pulseaudio.service pulseaudio.socket
```

Create the file ``/etc/systemd/system/pulseaudio.service``

```bash
# systemd service for pulseaudio running in system mode
# start with: systemctl start pulseaudio.service
# enable on boot: systemctl enable pulseaudio.service
[Unit]
Description=Pulseaudio sound server
After=avahi-daemon.service network.target
 
[Service]
Type=forking
ExecStart=/usr/bin/pulseaudio --realtime --no-cpu-limit --system --disallow-exit --daemonize
KillMode=process
ExecReload=/bin/pkill pulseaudio
 
[Install]
WantedBy=multi-user.target
```

Enable the service

```bash
systemctl --system enable pulseaudio.service
```

Reboot and pray to the IT god Linus Benedict Torvalds that it works. ``} else { print("Meh") }``

### Bluetooth

Run bluetoothctl

```bash
sudo bluetoothctl
```

Scan for devices

```bash
scan on
```

Once found, stop the scan and pair, trust, connect

```bash
scan off
pair <MAC-address>
trust <MAC-address>
connect <MAC-address>
```

### Music Player Daemon

Give mpd user access to pulseaudio

```bash
sudo gpasswd -a mpd pulse-access
```

In ``/etc/mpd.conf``

Place in comment the audio_output of type alsa :

> ```bash
> #audio_output {
> #  type    "alsa"
> #  name    "My ALSA Device"
> #  device    "hw:0,0"  # optional
> #  mixer_type      "hardware"      # optional
> #  mixer_device  "default"  # optional
> #  mixer_control  "PCM"    # optional
> #  mixer_index  "0"    # optional
> #}
> ```

Enable the audio_output of the type pulse :

> ```bash
> audio_output {
> type    "pulse"
> name    "My Pulse Output"
> #  server    "remote_server"    # optional
> #  sink    "remote_server_sink"  # optional
> }
> ```

And... Have you tried turning off and on again?

Add some songs of my people

```bash
mpc add <mp3-stream>
mpc save RadioPlaylist
mpc load RadioPlaylist
mpc play
```

...

## The end

``$ Success? [Y/n]:``

If no: (╯°□°）╯︵ ┻━┻
