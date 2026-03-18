# TETHER GALACTICA: DISCORD INTEL DROP ZONE
**Status:** AWAITING ARCHITECT INPUT | **Fidelity:** 1=1=1

*Architect: Paste any raw text, announcements, or mentor conversations from the Tether Discord below this line. I will assimilate the logic and integrate it into the SovereignNexus.*

---
## [Raw Data Entry]

*(barukimang — 10/20/25, 7:12 AM
Am using the react native quick start: https://docs.wallet.tether.io/start-building/react-native-quickstart

On running npm run gen:bundle am getting error:

npm run gen:bundle
npm error Missing script: "gen:bundle"
npm error
npm error To see a list of scripts, run:
npm error   npm run


Was able to add script to package.json manually: 
"gen:bundle": "npm --prefix node_modules/@tetherto/pear-wrk-wdk run gen:mobile-bundle",


Then when running the wdk on iOS simulator am getting error  ERROR  Failed to generate mnemonic: [Error: The user name or passphrase you entered is not correct.]  

Also see video attached. First I thought it could have to do with API connection, but not sure. Wdyt?
React Native Quickstart | Wallet Development Kit by Tether
Get started with WDK in React Native by running the production-ready starter wallet in 3 minutes
React Native Quickstart | Wallet Development Kit by Tether
Rachel | WDK DevRelRole icon, Tether Team — 10/22/25, 10:32 AM
Thanks for the details.  I'll try to reproduce the issue on my end and get back to you ASAP with what I find. Thanks for letting me know about the error and for attaching the video. Talk soon!

@Snezik we had this issue open, we will follow the "gen:bundle" error in this thred, thanks for your feedback
Rachel | WDK DevRelRole icon, Tether Team — 10/27/25, 10:23 AM
Hi all! 

The documentation for the React Native Starter has been updated! As well as the project repository, make sure you have the newest version, which should be fine now. 👍

https://docs.wallet.tether.io/start-building/react-native-quickstart

(potential problems)  Hi guys, 

Does the Tether WDK SDK has issues with Vercel or is it my configuration issue ?

I've my project deployed to Vercel ( free plan ) , I use signin with google method integrated it with supabase, there's a callback url that supabase sends requests in case of successful signups , in the callback function I've added method for creating smart wallets for my app users , but I'm getting below error : 

Wallet creation failed during OAuth callback: Error: Failed to load external module @tetherto/wdk-wallet-evm-erc-4337-f33009ffeb337f71: Error: Cannot find addon '.' imported from 'file:///var/task/node_modules/sodium-native/binding.js'
Candidates:
file:///var/task/node_modules/sodium-native/prebuilds/linux-x64/sodium-native@5.0.10.node
file:///var/task/node_modules/sodium-native/prebuilds/linux-x64/sodium-native.node
file:///var/task/node_modules/prebuilds/linux-x64/sodium-native@5.0.10.node
file:///var/task/node_modules/prebuilds/linux-x64/sodium-native.node
file:///var/task/prebuilds/linux-x64/sodium-native@5.0.10.node
file:///var/task/prebuilds/linux-x64/sodium-native.node
file:///var/prebuilds/linux-x64/sodium-native@5.0.10.node
file:///var/prebuilds/linux-x64/sodium-native.node
file:///prebuilds/linux-x64/sodium-native@5.0.10.node
file:///prebuilds/linux-x64/sodium-native.node
linked:libsodium-native.5.0.10.so
linked:libsodium-native.so
  at Context.externalImport [as y] (.next/server/chunks/[turbopack]runtime.js:518:15)
  at async (.next/server/chunks/[root-of-the-server]__78637a98..js:1:178)
I'm using this package of yours :     "@tetherto/wdk-wallet-evm-erc-4337": "^1.0.0-beta.5",
@Rachel | WDK DevRel can I get a quick look of this issue from your dev team
I have less than a day to submit my project for a hackathon
 [POL], 
smilingdibba [POL],  — 3/9/26, 5:26 AM
this error only comes in vercel deployment , when I run my app locally , I never get this error
 [POL], 
Rachel | WDK DevRelRole icon, Tether Team — 3/9/26, 7:41 AM
Let me double-check, let's see if I'm having the same error (I've never tried personally tbh), and if I do have the same or similar problem, I will align with the team to find out what could be!
smilingdibba [POL],  — 3/9/26, 8:06 AM
yes please check after deploying your app to vercel
smilingdibba [POL],  — 3/9/26, 10:08 AM
heya @Rachel | WDK DevRel , I moved away from Vercel , bought a domain , deployed my app to AWS EC2 , and the error is gone 

hoping that the team will fix it soon
DevQueen [BASE],  — 3/9/26, 12:12 PM
Hello

(rules) Hackathon Galáctica: WDK Edition 1 — Rules & FAQ

━━━━━━━━━━━━━━━━━━━━━━
KEY DATES
━━━━━━━━━━━━━━━━━━━━━━
Feb 25 — Registrations open
Mar 9 — Submissions portal opens
Mar 22 — Submissions close at 11:59 PM UTC

━━━━━━━━━━━━━━━━━━━━━━
RULES
━━━━━━━━━━━━━━━━━━━━━━
Open to everyone — solo or team
You may only submit one entry and belong to one team
WDK by Tether integration is mandatory in your project
Your project must be hosted on a public GitHub repo under Apache 2.0 license
All team members must be added to the project page on DoraHacks to be eligible
Your project must be easy for judges to evaluate — accessible via browser or runnable out of the box
All third-party services, APIs, or pre-built components must be disclosed

Full rules on Dorahacks

━━━━━━━━━━━━━━━━━━━━━━
SUBMISSION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━
Product name and brief description
Which track(s) you're submitting to
List of teammates with background and experience
Team location
Public GitHub repo link(s)
A demo video (max 5 min, uploaded to YouTube as unlisted)
→ Must include a project overview AND a live demo

━━━━━━━━━━━━━━━━━━━━━━
JUDGING CRITERIA
━━━━━━━━━━━━━━━━━━━━━━
Agent Intelligence — Strong use of LLMs, autonomous agents, clear decision-making logic
WDK Wallet Integration — Secure, correct, non-custodial wallet implementation
Technical Execution — Architecture quality, code, integrations, payment flow reliability
Agentic Payment Design — Programmable flows: conditional payments, subscriptions, commerce logic
Originality — Innovative use case and creative rethinking of agent–wallet interaction
Polish & Ship-ability — UX clarity, completeness, readiness for real-world deployment
Presentation & Demo — Clear explanation of agent logic, wallet flow, and payment lifecycle

━━━━━━━━━━━━━━━━━━━━━━
TRACKS
━━━━━━━━━━━━━━━━━━━━━━
Agent Wallets (WDK / Openclaw) — 3,000 / 2,000 USD₮
Lending Bot — 3,000 / 2,000 USD₮
Autonomous DeFi Agent — 3,000 / 2,000 USD₮
Tipping Bot — 3,000 / 2,000 USD₮
Best Overall — 6,000 / 3,000 / 1,000 USD₮

━━━━━━━━━━━━━━━━━━━━━━
LINKS
━━━━━━━━━━━━━━━━━━━━━━
Register on Dorahacks
WDK Docs
Rules
 
Rachel | WDK DevRel
 pinned a message to this channel. See all pinned messages. — 2/26/26, 11:44 AM



(mining)  we did a news story on Tether's MiningOS, and it's also on Yahoo Finance through our syndication deal with them

https://blockspace.media/insight/tether-launches-open-source-bitcoin-mining-management-software-mining-os/
https://finance.yahoo.com/news/tether-launches-open-source-bitcoin-160416238.html
Blockspace Media
Tether launches open-source bitcoin mining management software, Min...
Tether's MiningOS will serve as an open-source alternative to other mining management softwares.

Different.  I’ve talked to Gio in person about possibly making asic-rs implement some kind of worker interface for this, but there might be an oppurtunity to add bindings for JavaScript so it can be used directly in these workers.

From what I’ve seen of the Whatsminer worker, it is going to take a lot of work to catch up to where asic-rs or pyasic is at…. There seems to be support for the V2 API, but the V1 (M20) and V3 (2024.11 and newer) are missing.  There also probably needs to be some way of versioning this.
I have to get more in depth into the project, but I will hopefully have more feedback.  The hard part is that I don’t do much with JS, so I might struggle to actually do much contribution without putting a lot of other stuff on the back burner, but I can help with feedback and ideas.

Hey, just opened an issue on this (https://github.com/tetherto/miningos-wrk-miner-whatsminer/issues/3), but the Whatsminer worker probably needs to be changed to handle submodels rather than top level models, since there are hardware variations (indicated by submodel) inside of each model.  Think of it like:

M30S++ => “Antminer X19 Series Miner”
M30S++VG10 => S19XP

You have to include the submodel in order to derive hardware information like chip counts per board. 
GitHub
tetherto/miningos-wrk-miner-whatsminer
Contribute to tetherto/miningos-wrk-miner-whatsminer development by creating an account on GitHub.
tetherto/miningos-wrk-miner-whatsminer


GioRole icon, Tether Team — 1/26/26, 3:40 PM
📌 M-SDK — Start Here (Quick Guide)

Welcome! This pinned message explains what M-SDK is, where to find resources, and how to contribute.

What is M-SDK (Mining SDK)?
M-SDK is an open developer toolkit to build mining apps, dashboards, and automations on top of real mining + energy infrastructure.

The key idea:
each manufacturer or service provider (miners, PDUs, sensors, meters, pools, energy orchestrators, etc.) builds and maintains its own worker — a lightweight driver that knows how to talk to that device or service.

Once workers exist, builders can use M-SDK to:
combine them into higher-level tools
build monitoring, control, and automation logic
focus on product value instead of rewriting integrations

--> This removes a lot of low-value glue code and lets developers move faster.


Repos & Docs
🔗 GitHub BE: https://github.com/tetherto/m-sdk-be/:link
🔗 GitHub FE: https://github.com/tetherto/m-sdk-ui-dev-kit
🔗 Docs / Architecture: https://github.com/tetherto/m-sdk-be/blob/main/ARCHITECTURE.md
🔗 Contribute: https://github.com/tetherto/m-sdk-be/blob/main/CONTRIBUTING.md
🔗 Roadmap : TBD


Discord vs GitHub
✅ Discord → onboarding, questions, coordination, early brainstorming
✅ GitHub → issues, tracking, PRs, reviews

📌 If it needs tracking or ownership → open a GitHub issue.



Channels (quick map)
🔹 ⁠m-sdk-start-here → onboarding + links
🔹 ⁠m-sdk-introductions → say hi 👋 + GitHub link
🔹 ⁠m-sdk-planning → roadmap + priorities
🔹 ⁠m-sdk-build-log → progress + shipped updates
🔹 ⁠m-sdk-design-reviews → architecture + decisions
🔹 ⁠mos → MOS context + how it connects to M-SDK

Need help? Ask here or introduce yourself in ⁠m-sdk-introductions 👋 
GitHub
GitHub - tetherto/m-sdk-ui-dev-kit
Contribute to tetherto/m-sdk-ui-dev-kit development by creating an account on GitHub.
Contribute to tetherto/m-sdk-ui-dev-kit development by creating an account on GitHub.
GitHub
m-sdk-be/ARCHITECTURE.md at main · tetherto/m-sdk-be
Contribute to tetherto/m-sdk-be development by creating an account on GitHub.
m-sdk-be/ARCHITECTURE.md at main · tetherto/m-sdk-be
GitHub
m-sdk-be/CONTRIBUTING.md at main · tetherto/m-sdk-be
Contribute to tetherto/m-sdk-be development by creating an account on GitHub.
m-sdk-be/CONTRIBUTING.md at main · tetherto/m-sdk-be
Gio
 pinned a message to this channel. See all pinned messages. — 1/26/26, 3:40 PM
)*
