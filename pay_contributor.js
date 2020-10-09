const { PayIdClient, Wallet,
	XrpClient, XrplNetwork,
	XrpPayIdClient, XpringClient } = require('xpring-js')

const core = require('@actions/core')
const github = require('@actions/github');

require('dotenv').config()

async function run() {

    // Get our parameters from the environment
    const env = process.env
    const wallet_seed = process.env.INPUT_WALLET_SECRET
    const environment = process.env.INPUT_ENVIRONMENT.toLowerCase()
    const server = process.env.INPUT_SERVER
    const commitmsg = process.env.INPUT_COMMIT_LOG
    const amount = process.env.INPUT_AMOUNT
    const max_payout = process.env.INPUT_MAX_PAYOUT

    // If not commit message, then try to work out open opener of pull request
    const token = core.getInput('repo_token')
    const octokit = github.getOctokit(token)

    const context = github.context
    console.log(JSON.stringify(context, null, 4))

    
    // Abort if we don't have a wallet secret
    if (wallet_seed === undefined) {
	console.log("Missing INPUT_WALLET_SECRET")
	process.exit(1)
    }

    // Instantiate instance of a wallet with seed
    const wallet = Wallet.generateWalletFromSeed(
	wallet_seed,
    )

    // Create the clients we need
    const xrpClient = new XrpClient(server, environment)
    const payIdClient = new XrpPayIdClient(environment)
    const xpringClient = new XpringClient(payIdClient, xrpClient)

    // Find all payids in the commit message
    const payIds = commitmsg.match(/(\S+\$\S+\.\S+)/g)

    // If we have no payids found then exit with success
    const num = payIds.length
    if (num < 1) {
	console.log("No PayIDs found")
	process.exit(0)
    }

    // Calculate the amount to pay, paying each evenly
    const payid_amount = Math.floor(Math.min(amount, max_payout / num))

    // Make each payment and await success
    for(let i=0; i<num; i++) {
	let payId = payIds[i]
	console.log(`Paying ${payId} amount ${payid_amount}`)
	try {
	    const transactionHash = await xpringClient.send(payid_amount,
							    payId,
							    wallet)
	    console.log(transactionHash)
	} catch(e) {
	    console.log("Could not pay", payId, e)
	}
	
    }
}

run();
