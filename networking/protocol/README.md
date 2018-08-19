### protocol

Hi there!

We need to extract secret data from a special file server.

We don't have much details about this server, but we did manage to intercept traffic containing communication with the server.

We also know that this secret file's path is: /usr/7Op_sECreT.txt

You can find the sniff file here.

Please tell us what the secret is!

Good luck!

### solution

1) open the pcap file with wireshark
2) filter : frame contains 'usr'
3) find the protocol session
4) connect with nc to the server, request the secret file and xor decode it