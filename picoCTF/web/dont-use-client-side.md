#dont-use-client-side

## Analysis

- Simple field where we can verify a secret
- Simple inputs do not succeed
- Checking source code reveals secret which is the flag

## Solution

- The JS validation function hides the flag, we can simply restore it by assembling the parts in the correct order