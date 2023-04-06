# Setup

1. Start kali linux via UTM
2. Connect to project via ssh
    - this gives you full access to all kali tools within IDE terminals
3. Connect to challenges on port 80 via browser on host:
    - establish jump host connection via kali to target
    - `ssh -L 80:<target-ip>:80 <user>@<kali-ip>`