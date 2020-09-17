# payid_xrp_action

## What?
A Github Action that pays a contributor in XRP for every commit.
This means you can define an amount to be paid every time someone pushes
commits to you repository.

The address to send the payment to is looked up via [PayIds](https://payid.org/) 
in the commit messages.

## How to set it up?

An example workflow:

```yaml
name: Pay contributors

on:
  # Trigger the workflow on push or pull request,
  # but only for the master branch
  push:
    branches:
      - master

jobs:
  pay:
    runs-on: ubuntu-latest
    steps:

    - name: Checkout code
      uses: actions/checkout@v2

    - name: get commit message
      run: |
        echo ::set-env name=commit_log::$(git log --format=%B ${{ github.event.before }}..${{ github.event.after }})

    - name: Run PayID
      uses: hammertoe/payid_xrp_action@master
      with:
        commit_log: ${{ env.commit_log }}
        wallet_secret: ${{ secrets.PAYID_WALLET_SECRET }}
        amount: 1000000
```

The above workflow will pay each PayId it finds in the commit logs 1 XRP (1000000 drops) from the XRP
wallet with the secret key in the Github secret defined in `PAYID_WALLET_SECRET`.

## Parameters

The action takes the following input parameters:

```yaml
  amount:
    description: 'Amount of XRP in drops to pay each PayId found'
    default: 1000000
  commit_log:
    description: 'The commit message(s) to scan for PayIds'
    required: true
  wallet_secret:
    descrption: 'The secret key of the XRP wallet to pay from'
    required: true
  max_payout:
    description: 'Maximum number of drops to pay out'
    default: 10000000
  environment:
    description: 'Environment to use, TESTNET or LIVENET'
    default: 'TESTNET'
  server:
    description: 'XRP Ledger server to use'
    default: 'test.xrp.xpring.io:50051'
```

Note above: by default this runs on the XRP TESTNET, you need to set the `environment` input parameter
to `LIVENET` and set the correct production server in `server` order to make payments on the live network. 