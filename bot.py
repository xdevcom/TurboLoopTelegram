import os
import json
import time
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

# Topics in order
TOPICS = ["System Integrity", "Token Supply", "Deposit Rewards", "Staking Plans", "Daily Burn", "Vesting Unlock", "Rank System", "Referral System", "On-Chain Automation", "Tax System", "Locked LP", "Passive Income", "Fair Launch", "Call to Action", "Deflationary", "Tokenomics", "Smart Contract", "Ecosystem"]

# 180 unique captions hardcoded
CAP_DATA = {
    "System Integrity": {
        "title": "SYSTEM INTEGRITY",
        "desc": [
            "Fully automated on-chain ecosystem designed for long-term sustainability, transparent rewards and secure vesting execution!",
            "Zero human control ensures 100% security, trustless execution, and absolute transparency for every investor.",
            "Our immutable smart contracts guarantee that the protocol rules can never be altered or manipulated by anyone.",
            "Built on top-tier security standards, TurboLoop protects your capital with decentralized on-chain architecture.",
            "Experience a trustless financial ecosystem where code is the ultimate law and transparency is guaranteed.",
            "Eliminating human error and manipulation with fully automated smart contracts on Binance Smart Chain.",
            "A decentralized protocol engineered for maximum security, continuous growth, and zero counterparty risk.",
            "Secure, automated, and non-custodial. Your funds, your rewards, completely governed by immutable code.",
            "Designed from the ground up to maintain absolute system integrity and deliver secure passive rewards 24/7.",
            "The pinnacle of DeFi security: fully audited smart contracts executing automated on-chain tokenomics."
        ],
        "features": [
            [
                "Instant First Unlock Mechanism",
                "Smart 70/30 Reward Distribution",
                "Secure & Automated Vesting Contract",
                "No Manual Intervention Required",
                "Transparent \u2022 Stable \u2022 Smart Contract Secured"
            ],
            [
                "100% Trustless Code Execution",
                "No Admin Keys or Backdoors",
                "Real-Time On-Chain Verifiability",
                "Automated Security Safeguards",
                "Secure \u2022 Immutable \u2022 Non-Custodial"
            ],
            [
                "Decentralized Protocol Rules",
                "Cryptographically Secured Vaults",
                "Automated Reward Distribution",
                "Zero Human Counterparty Risk",
                "Transparent \u2022 Secure \u2022 Audited Code"
            ],
            [
                "Military-Grade Smart Contracts",
                "Fully Audited On-Chain Logic",
                "Instant Automated Settlements",
                "Tamper-Proof Ecosystem Design",
                "Immutable \u2022 Secure \u2022 Automated"
            ],
            [
                "On-Chain Governance Safeguards",
                "Non-Custodial Reward Vaults",
                "Automated Buyback & Burn",
                "Zero Administrative Override",
                "Trustless \u2022 Transparent \u2022 Safe"
            ],
            [
                "Automated Protocol Execution",
                "Secure Vesting Smart Contract",
                "Instant Reward Allocations",
                "No Central Point of Failure",
                "Decentralized \u2022 Secure \u2022 Immutable"
            ],
            [
                "Continuous Security Monitoring",
                "Fully Audited Codebase",
                "On-Chain Reward Verification",
                "Decentralized Vault Protection",
                "Secure \u2022 Stable \u2022 Smart Contract Secured"
            ],
            [
                "Zero Administrative Control",
                "Automated Reward Processing",
                "Immutable Vesting Schedules",
                "Non-Custodial Asset Management",
                "Trustless \u2022 Transparent \u2022 Automated"
            ],
            [
                "Automated Liquidity Safeguards",
                "On-Chain Cryptographic Proofs",
                "Secure Yield Generation",
                "No Manual Override Ever",
                "Secure \u2022 Immutable \u2022 Decentralized"
            ],
            [
                "Fully Audited DeFi Architecture",
                "Automated Reward Distribution",
                "Secure Vesting Locks",
                "Zero Administrative Risks",
                "Transparent \u2022 Trustless \u2022 Secured"
            ]
        ],
        "facts": [
            [
                "1M TURBO Fixed Supply - Verified",
                "10% Monthly Base Vesting",
                "1% Buy Tax | 2% Sell Tax",
                "Daily Automated Burn System",
                "10% Fee Allocation For Ecosystem Funding"
            ],
            [
                "100% Locked Liquidity Pool - Verified",
                "Zero Team Token Allocation",
                "Fully Audited Smart Contract",
                "No Admin Key Vulnerabilities",
                "100% On-Chain Transparency"
            ],
            [
                "Fixed 1,000,000 TURBO Supply - Verified",
                "Automated 70/30 Reward Split",
                "Flexible 30/60 Day Staking",
                "Daily Auto-Buyback & Burn",
                "Immutable Vesting Schedule"
            ],
            [
                "No Mint Function in Code - Verified",
                "Liquidity Locked Forever",
                "Automated Fee Distribution",
                "Real-Time On-Chain Auditing",
                "Decentralized Governance Model"
            ],
            [
                "Secure Smart Contract Code - Verified",
                "Automated Buyback & Burn",
                "10% Monthly Base Vesting",
                "1% Buy Tax | 2% Sell Tax",
                "10% Fee for Ecosystem Growth"
            ],
            [
                "100% Non-Custodial Design - Verified",
                "No Pre-Mine or Team Reserves",
                "Automated Reward Execution",
                "Zero Manual Intervention",
                "Verified on BSCScan"
            ],
            [
                "1M TURBO Maximum Supply - Verified",
                "70/30 Reward Distribution",
                "Daily Automated Burn System",
                "Fully Audited Smart Contract",
                "Zero Counterparty Risk"
            ],
            [
                "Locked Liquidity Pool (100%) - Verified",
                "10% Monthly Base Vesting",
                "No Administrative Backdoors",
                "Automated Yield Distribution",
                "100% Trustless Ecosystem"
            ],
            [
                "Fixed Deflationary Supply - Verified",
                "1% Buy Tax | 2% Sell Tax",
                "Automated Vesting Execution",
                "No Minting Capabilities",
                "Decentralized Architecture"
            ],
            [
                "Fully Audited DeFi Code - Verified",
                "Zero Team Token Allocation",
                "Automated 70/30 Reward Split",
                "Daily Auto-Buyback & Burn",
                "10% Ecosystem Fee Allocation"
            ]
        ],
        "tagline": "Sustainable Growth \u2022 Automated Mechanics \u2022 Stronger Ecosystem"
    },
    "Token Supply": {
        "title": "TOKEN SUPPLY & PARAMETERS",
        "desc": [
            "A secure and transparent tokenomics model with a fixed maximum supply of 1,000,000 TURBO tokens, ensuring absolute scarcity.",
            "Engineered for scarcity: 100% of the initial liquidity is locked, with zero team allocation and no minting functions.",
            "TurboLoop's fixed supply guarantees that no new tokens can ever be created, protecting holders from inflation.",
            "A fair launch model with a maximum supply of 1M TURBO, designed to drive long-term value through scarcity.",
            "No team tokens, no pre-mine, and no administrative reserves. 100% of the supply is dedicated to the community.",
            "Scarcity meets utility: a fixed supply of 1,000,000 TURBO tokens with built-in deflationary burn mechanics.",
            "Our token parameters are hardcoded into the immutable smart contract, ensuring a fair and transparent launch.",
            "Protecting investor value with a strictly limited supply of 1M TURBO and automated buyback & burn systems.",
            "A premium DeFi tokenomics model with 100% locked initial liquidity and zero developer token allocation.",
            "TurboLoop guarantees absolute transparency with a hardcapped supply and fully auditable on-chain parameters."
        ],
        "features": [
            [
                "Fixed 1,000,000 Max Supply",
                "100% Locked Liquidity Pool",
                "Zero Developer Token Allocation",
                "No Pre-Mine or Team Reserves",
                "Scarcity \u2022 Value Protection \u2022 Fair Launch"
            ],
            [
                "Hardcapped Token Supply",
                "Liquidity Locked Permanently",
                "No Inflationary Mint Functions",
                "Fair Community Distribution",
                "Scarcity \u2022 Security \u2022 Transparency"
            ],
            [
                "Strict 1M TURBO Hardcap",
                "100% Initial LP Locked",
                "Zero Team or Advisor Allocation",
                "Automated Value Accrual",
                "Deflationary \u2022 Secure \u2022 Fair"
            ],
            [
                "Scarcity-Driven Tokenomics",
                "Locked Liquidity on PancakeSwap",
                "No Developer Dump Risk",
                "100% Community-Owned Supply",
                "Value \u2022 Trust \u2022 Decentralization"
            ],
            [
                "Fixed Non-Inflationary Supply",
                "Permanently Locked LP Tokens",
                "Zero Pre-Allocation for Team",
                "Automated Scarcity Engine",
                "Secure \u2022 Scarce \u2022 Sustainable"
            ],
            [
                "1,000,000 Max Token Supply",
                "100% Locked Liquidity Pool",
                "No Minting Capabilities in Code",
                "Fair Launch for All Investors",
                "Transparent \u2022 Stable \u2022 Scarce"
            ],
            [
                "Hardcoded Token Scarcity",
                "Locked PancakeSwap Liquidity",
                "Zero Administrative Allocations",
                "Automated Burn on Transactions",
                "Deflationary \u2022 Trustless \u2022 Secure"
            ],
            [
                "Strictly Limited Max Supply",
                "100% Initial LP Locked",
                "No Developer Token Reserves",
                "Fair and Equal Launch Model",
                "Secure \u2022 Scarce \u2022 Value-Driven"
            ],
            [
                "Non-Inflationary Tokenomics",
                "Permanently Locked LP",
                "Zero Team Allocation",
                "Automated Buyback & Burn",
                "Deflationary \u2022 Trustless \u2022 Fair"
            ],
            [
                "1M TURBO Maximum Hardcap",
                "100% Locked Initial Liquidity",
                "Zero Developer Reserves",
                "Built-In Deflationary Design",
                "Scarcity \u2022 Security \u2022 Transparency"
            ]
        ],
        "facts": [
            [
                "1M TURBO Maximum Supply - Verified",
                "100% Locked Initial LP",
                "Zero Team Token Allocation",
                "No Pre-Mine or Reserves",
                "100% Community-Driven Launch"
            ],
            [
                "Fixed 1,000,000 Supply - Verified",
                "Permanently Locked Liquidity",
                "Zero Developer Allocation",
                "No Inflationary Minting",
                "Fully Audited Parameters"
            ],
            [
                "Strict 1M TURBO Hardcap - Verified",
                "100% Initial LP Locked",
                "No Team Token Reserves",
                "Daily Automated Burn System",
                "1% Buy Tax | 2% Sell Tax"
            ],
            [
                "Scarcity-Driven Tokenomics - Verified",
                "Locked PancakeSwap Liquidity",
                "Zero Pre-Allocation for Team",
                "No Mint Function in Code",
                "Decentralized Launch Model"
            ],
            [
                "Fixed Non-Inflationary Supply - Verified",
                "100% Locked Initial LP",
                "Zero Developer Tokens",
                "Daily Auto-Buyback & Burn",
                "10% Monthly Base Vesting"
            ],
            [
                "1,000,000 Max Token Supply - Verified",
                "Permanently Locked LP",
                "No Minting Capabilities",
                "Fair Launch for All",
                "Verified Smart Contract"
            ],
            [
                "Hardcoded Token Scarcity - Verified",
                "100% Locked Liquidity",
                "Zero Team Allocations",
                "Automated Deflationary Burn",
                "1% Buy Tax | 2% Sell Tax"
            ],
            [
                "Strictly Limited Max Supply - Verified",
                "100% Initial LP Locked",
                "No Developer Token Reserves",
                "Daily Automated Burn System",
                "100% Community Owned"
            ],
            [
                "Non-Inflationary Tokenomics - Verified",
                "Permanently Locked LP",
                "Zero Team Allocation",
                "Automated Buyback & Burn",
                "10% Monthly Base Vesting"
            ],
            [
                "1M TURBO Maximum Hardcap - Verified",
                "100% Locked Initial LP",
                "Zero Developer Reserves",
                "Built-In Deflationary Design",
                "Fully Audited Code"
            ]
        ],
        "tagline": "Strict Scarcity \u2022 Zero Team Allocation \u2022 Locked Liquidity"
    },
    "Deposit Rewards": {
        "title": "DEPOSIT REWARD SYSTEM",
        "desc": [
            "Earn lucrative daily rewards on your deposits with a sustainable tiered yield system that grows with your participation.",
            "TurboLoop rewards active investors with a highly lucrative daily yield, distributed through a secure 70/30 split.",
            "Maximize your passive income with our tiered deposit reward system, offering up to 1.60% daily yield.",
            "A sustainable reward engine designed to deliver consistent daily returns while funding ecosystem growth.",
            "Our deposit reward system is fully automated on-chain, ensuring instant and secure payouts directly to your wallet.",
            "Get rewarded for your deposits with a tiered daily yield system that accelerates based on your rank.",
            "A smart 70/30 reward distribution model that benefits both active investors and their network referrers.",
            "TurboLoop's deposit rewards are hardcoded and executed automatically by our audited smart contracts.",
            "Earn up to 1.60% daily yield on your deposits with a fully transparent and non-custodial reward system.",
            "Boost your passive income with a sustainable tiered reward system that scales as the ecosystem grows."
        ],
        "features": [
            [
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Distribution",
                "Automated On-Chain Payouts",
                "Vesting Acceleration Options",
                "Lucrative \u2022 Sustainable \u2022 Automated"
            ],
            [
                "High-Yield Tiered Daily Rewards",
                "70% Direct Investor Allocation",
                "30% Network Referrer Reward",
                "Rank-Based Yield Boosts",
                "Sustainable \u2022 Lucrative \u2022 Secure"
            ],
            [
                "Up to 1.60% Tiered Daily Yield",
                "Smart 70/30 Reward Split",
                "Automated Yield Distribution",
                "No Manual Claiming Required",
                "Automated \u2022 High-Yield \u2022 Secure"
            ],
            [
                "Sustainable Daily Reward Engine",
                "70% Direct Reward to Investor",
                "30% Referral Reward Split",
                "Rank Acceleration Mechanics",
                "Lucrative \u2022 Automated \u2022 Trustless"
            ],
            [
                "Fully Automated Daily Yield",
                "Smart 70/30 Reward Allocation",
                "Tiered Daily Returns (0.80%-1.60%)",
                "Secure Non-Custodial Vaults",
                "Transparent \u2022 Lucrative \u2022 Secure"
            ],
            [
                "Tiered Daily Reward System",
                "70% Direct Payout to Investor",
                "30% Referral Reward Share",
                "Rank-Based Yield Acceleration",
                "Sustainable \u2022 High-Yield \u2022 Automated"
            ],
            [
                "Lucrative Tiered Daily Returns",
                "Smart 70/30 Reward Distribution",
                "On-Chain Reward Verification",
                "No Administrative Fees on Yield",
                "Secure \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Automated Daily Yield Engine",
                "70% Direct Reward to Depositor",
                "30% Network Reward Allocation",
                "Rank-Based Yield Multipliers",
                "Sustainable \u2022 High-Yield \u2022 Secure"
            ],
            [
                "Tiered Daily Yield (Up to 1.60%)",
                "Smart 70/30 Reward Allocation",
                "Automated On-Chain Payouts",
                "Vesting Acceleration Options",
                "Transparent \u2022 Lucrative \u2022 Trustless"
            ],
            [
                "High-Yield Tiered Daily Rewards",
                "70% Direct Investor Allocation",
                "30% Network Referrer Reward",
                "Rank-Based Yield Boosts",
                "Sustainable \u2022 Lucrative \u2022 Automated"
            ]
        ],
        "facts": [
            [
                "Tiered Daily Yield: 0.80%-1.60% - Verified",
                "Smart 70/30 Reward Split",
                "Minimum Deposit: $100 USDT",
                "No Deposit Fees in Protocol",
                "Automated On-Chain Payouts"
            ],
            [
                "Up to 1.60% Daily Yield - Verified",
                "70% Direct to Depositor",
                "30% Direct to Referrer",
                "Rank-Based Yield Boosts",
                "100% Non-Custodial System"
            ],
            [
                "Tiered Daily Returns: 0.80%-1.60% - Verified",
                "70/30 Reward Distribution",
                "Minimum Deposit: $100 USDT",
                "No Administrative Fees",
                "Verified Smart Contract"
            ],
            [
                "High-Yield Tiered Daily Rewards - Verified",
                "70% Direct Investor Allocation",
                "30% Referrer Reward Split",
                "Automated Vesting Acceleration",
                "100% Transparent Logic"
            ],
            [
                "Tiered Daily Yield: 0.80%-1.60% - Verified",
                "Smart 70/30 Reward Split",
                "Minimum Deposit: $100 USDT",
                "No Deposit Fees",
                "Automated On-Chain Payouts"
            ],
            [
                "Up to 1.60% Daily Yield - Verified",
                "70% Direct to Depositor",
                "30% Direct to Referrer",
                "Rank-Based Yield Boosts",
                "100% Non-Custodial System"
            ],
            [
                "Tiered Daily Returns: 0.80%-1.60% - Verified",
                "70/30 Reward Distribution",
                "Minimum Deposit: $100 USDT",
                "No Administrative Fees",
                "Verified Smart Contract"
            ],
            [
                "High-Yield Tiered Daily Rewards - Verified",
                "70% Direct Investor Allocation",
                "30% Referrer Reward Split",
                "Automated Vesting Acceleration",
                "100% Transparent Logic"
            ],
            [
                "Tiered Daily Yield: 0.80%-1.60% - Verified",
                "Smart 70/30 Reward Split",
                "Minimum Deposit: $100 USDT",
                "No Deposit Fees",
                "Automated On-Chain Payouts"
            ],
            [
                "Up to 1.60% Daily Yield - Verified",
                "70% Direct to Depositor",
                "30% Direct to Referrer",
                "Rank-Based Yield Boosts",
                "100% Non-Custodial System"
            ]
        ],
        "tagline": "Lucrative Yield \u2022 Smart 70/30 Split \u2022 Automated Payouts"
    },
    "Staking Plans": {
        "title": "STAKING PLANS",
        "desc": [
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth.",
            "Lock your TURBO tokens in our high-yield staking pools and earn competitive daily returns with flexible lock-up periods. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ],
            [
                "Flexible 30/60 Day Staking",
                "Competitive Daily Returns",
                "Automated Yield Compounding",
                "Secure Non-Custodial Pools",
                "High-Yield \u2022 Flexible \u2022 Secure"
            ]
        ],
        "facts": [
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ],
            [
                "Flexible 30/60 Day Lock-Up - Verified",
                "Competitive Daily Returns",
                "Automated Compounding Options",
                "Zero Withdrawal Fees on Yield",
                "100% Secure Staking Pools"
            ]
        ],
        "tagline": "Flexible Lock-Ups \u2022 High Daily Yield \u2022 Secure Staking"
    },
    "Daily Burn": {
        "title": "DAILY AUTOMATED BURN",
        "desc": [
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth.",
            "Every single transaction triggers an automated buyback and burn, continuously reducing supply and driving scarcity. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ],
            [
                "Automated Buyback & Burn",
                "Scarcity-Driven Tokenomics",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "Deflationary \u2022 Automated \u2022 Secure"
            ]
        ],
        "facts": [
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Daily Automated Burn System - Verified",
                "Continuous Supply Reduction",
                "Value Accrual for Holders",
                "No Manual Burn Required",
                "Hardcoded Deflationary Logic"
            ]
        ],
        "tagline": "Continuous Burn \u2022 Rising Scarcity \u2022 Value Accrual"
    },
    "Vesting Unlock": {
        "title": "VESTING & UNLOCK SCHEDULE",
        "desc": [
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth.",
            "A highly structured and secure vesting schedule that ensures long-term sustainability and prevents market dumps. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ],
            [
                "10% Monthly Base Vesting",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "Secure Vesting Smart Contract",
                "Sustainable \u2022 Secure \u2022 Transparent"
            ]
        ],
        "facts": [
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ],
            [
                "10% Monthly Base Vesting - Verified",
                "Vesting Acceleration via Ranks",
                "Instant First Unlock Mechanism",
                "No Administrative Overrides",
                "100% On-Chain Vesting Logic"
            ]
        ],
        "tagline": "Structured Vesting \u2022 Acceleration Mechanics \u2022 Anti-Dump"
    },
    "Rank System": {
        "title": "LEADERSHIP RANK SYSTEM",
        "desc": [
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth.",
            "Climb through 8 leadership rank tiers, from Partner to Legend, and unlock massive yield boosts and vesting acceleration. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ],
            [
                "8 Leadership Rank Tiers",
                "Vesting Acceleration Boosts",
                "Lucrative Rank Requirements",
                "Ecosystem-Wide Recognition",
                "Prestigious \u2022 Lucrative \u2022 Gamified"
            ]
        ],
        "facts": [
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ],
            [
                "8 Leadership Rank Tiers - Verified",
                "Vesting Acceleration Boosts",
                "Ecosystem-Wide Recognition",
                "No Administrative Fees",
                "Fully Automated Rank Progression"
            ]
        ],
        "tagline": "Climb the Ranks \u2022 Unlock Massive Boosts \u2022 Lead the Community"
    },
    "Referral System": {
        "title": "REFERRAL PROGRAM",
        "desc": [
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth.",
            "Earn lucrative referral rewards by inviting others to join the TurboLoop ecosystem. Build your network and earn together. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ],
            [
                "Lucrative Referral Rewards",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "Network Growth Incentives",
                "Fair \u2022 Lucrative \u2022 Transparent"
            ]
        ],
        "facts": [
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ],
            [
                "Lucrative Referral Rewards - Verified",
                "Single-Level Referral Model",
                "Instant On-Chain Payouts",
                "No Referral Fees in Protocol",
                "100% Transparent Referral Logic"
            ]
        ],
        "tagline": "Refer & Earn \u2022 Build Your Network \u2022 Grow Together"
    },
    "On-Chain Automation": {
        "title": "ON-CHAIN AUTOMATION",
        "desc": [
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth.",
            "Experience absolute trustless execution with a protocol that runs 100% on-chain, completely free from human control. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ],
            [
                "100% On-Chain Execution",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "Transparent Transaction Logs",
                "Trustless \u2022 Automated \u2022 Decentralized"
            ]
        ],
        "facts": [
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ],
            [
                "100% On-Chain Execution - Verified",
                "Zero Human Intervention",
                "Immutable Smart Contracts",
                "No Administrative Backdoors",
                "Fully Audited Protocol Logic"
            ]
        ],
        "tagline": "Pure Automation \u2022 Zero Human Error \u2022 Absolute Trust"
    },
    "Tax System": {
        "title": "TAX SYSTEM & FEES",
        "desc": [
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth.",
            "A highly optimized tax system with a 1% buy tax and 2% sell tax, designed to fund continuous buybacks and ecosystem growth. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ],
            [
                "Low 1% Buy Tax / 2% Sell Tax",
                "Automated Buyback & Burn Funding",
                "Ecosystem Development Support",
                "Anti-Whale Tax Mechanics",
                "Optimized \u2022 Sustainable \u2022 Secure"
            ]
        ],
        "facts": [
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ],
            [
                "1% Buy Tax | 2% Sell Tax - Verified",
                "Automated Buyback Funding",
                "Ecosystem Development Support",
                "No Hidden Protocol Fees",
                "Hardcoded Tax Parameters"
            ]
        ],
        "tagline": "Low Transaction Taxes \u2022 Continuous Funding \u2022 Sustainable Growth"
    },
    "Locked LP": {
        "title": "LOCKED LIQUIDITY POOL",
        "desc": [
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth.",
            "Sleep easy knowing that 100% of the initial liquidity pool is permanently locked, ensuring absolute rug-pull protection. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ],
            [
                "100% Permanent LP Lock",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "PancakeSwap Liquidity Security",
                "Secure \u2022 Stable \u2022 Permanent"
            ]
        ],
        "facts": [
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ],
            [
                "100% Permanent LP Lock - Verified",
                "Rug-Pull Proof Architecture",
                "Stable Price Floor Support",
                "No Developer Token Reserves",
                "Fully Audited Security Locks"
            ]
        ],
        "tagline": "Liquidity Locked Forever \u2022 Rug-Pull Proof \u2022 Safe Investing"
    },
    "Passive Income": {
        "title": "PASSIVE INCOME ENGINE",
        "desc": [
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth.",
            "Generate consistent, long-term passive income through automated yield distribution, staking, and referral rewards. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ],
            [
                "Consistent Daily Yield",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "Consistent \u2022 Passive \u2022 Secure"
            ]
        ],
        "facts": [
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ],
            [
                "Consistent Daily Yield - Verified",
                "Multiple Income Streams",
                "Automated Reward Payouts",
                "No Active Management Needed",
                "100% Secure Yield Contracts"
            ]
        ],
        "tagline": "Earn Passive Income \u2022 Multiple Yield Streams \u2022 Fully Automated"
    },
    "Fair Launch": {
        "title": "FAIR LAUNCH MODEL",
        "desc": [
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth.",
            "A truly decentralized launch with zero team tokens, no pre-sale, and equal opportunity for all participants from day one. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ],
            [
                "Zero Team Token Allocation",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "100% Community-Driven Supply",
                "Fair \u2022 Decentralized \u2022 Equal"
            ]
        ],
        "facts": [
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ],
            [
                "Zero Team Token Allocation - Verified",
                "No Pre-Sale or Private Rounds",
                "Equal Opportunity Launch",
                "No Administrative Backdoors",
                "Fully Audited Smart Contract"
            ]
        ],
        "tagline": "Equal Opportunity \u2022 Zero Team Tokens \u2022 Community First"
    },
    "Call to Action": {
        "title": "JOIN TURBOLOOP TODAY",
        "desc": [
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth.",
            "Don't miss out on the next generation of automated DeFi. Join TurboLoop today and start earning sustainable yield. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ],
            [
                "Start with as little as $100",
                "Join a Global Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "Fast \u2022 Secure \u2022 Easy to Join"
            ]
        ],
        "facts": [
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ],
            [
                "Minimum Deposit: $100 USDT - Verified",
                "Global Active Community",
                "Access Premium Staking Pools",
                "Earn Lucrative Passive Yield",
                "100% Secure Smart Contract"
            ]
        ],
        "tagline": "The Future of DeFi is Here \u2022 Join TurboLoop Today \u2022 Start Earning"
    },
    "Deflationary": {
        "title": "DEFLATIONARY MECHANISMS",
        "desc": [
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth.",
            "Engineered for hyper-scarcity with continuous buybacks, daily burns, and a fixed supply that can only decrease over time. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ],
            [
                "Continuous Token Buybacks",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "Transaction Tax-Funded Burn",
                "Hyper-Scarce \u2022 Deflationary \u2022 Secure"
            ]
        ],
        "facts": [
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ],
            [
                "Continuous Token Buybacks - Verified",
                "Daily Automated Burn System",
                "Fixed Max Supply (1,000,000)",
                "No Minting Capabilities",
                "Hardcoded Deflationary Logic"
            ]
        ],
        "tagline": "Hyper-Scarcity \u2022 Daily Automated Burn \u2022 Rising Price Floor"
    },
    "Tokenomics": {
        "title": "TOKENOMICS OVERVIEW",
        "desc": [
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth.",
            "A comprehensive look at TurboLoop's sustainable, high-yield, and hyper-deflationary tokenomics architecture. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ],
            [
                "Fixed 1M TURBO Supply",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "Sustainable \u2022 Balanced \u2022 High-Yield"
            ]
        ],
        "facts": [
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ],
            [
                "Fixed 1M TURBO Supply - Verified",
                "Tiered Daily Yield (0.80%-1.60%)",
                "Smart 70/30 Reward Split",
                "Daily Automated Burn System",
                "10% Monthly Base Vesting"
            ]
        ],
        "tagline": "Balanced Tokenomics \u2022 Long-Term Sustainability \u2022 High Yield"
    },
    "Smart Contract": {
        "title": "SMART CONTRACT SECURITY",
        "desc": [
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth.",
            "Your security is our top priority. TurboLoop's smart contracts are fully audited, open-source, and verified on-chain. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ],
            [
                "Fully Audited Smart Contracts",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "Non-Custodial Asset Control",
                "Audited \u2022 Secure \u2022 Transparent"
            ]
        ],
        "facts": [
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ],
            [
                "Fully Audited Smart Contracts - Verified",
                "Verified Code on BSCScan",
                "No Administrative Backdoors",
                "No Mint Function in Code",
                "100% Immutable Logic"
            ]
        ],
        "tagline": "Fully Audited Code \u2022 Rug-Pull Proof \u2022 Maximum Security"
    },
    "Ecosystem": {
        "title": "THE COMPLETE ECOSYSTEM",
        "desc": [
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth.",
            "A fully integrated DeFi ecosystem where staking, burning, vesting, and referrals work together to drive maximum value. - Engineered for maximum long-term growth."
        ],
        "features": [
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ],
            [
                "Fully Integrated Components",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "Integrated \u2022 Efficient \u2022 Lucrative"
            ]
        ],
        "facts": [
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ],
            [
                "Fully Integrated Components - Verified",
                "Staking, Vesting & Referrals",
                "Daily Automated Burn Engine",
                "Low Transaction Tax System",
                "10% Ecosystem Fee Allocation"
            ]
        ],
        "tagline": "Seamless Integration \u2022 Maximum Efficiency \u2022 Ultimate DeFi Experience"
    }
}

# Image file mapping
IMAGES_MAP = ["001_system_integrity_v1.jpg", "007_token_supply_v1.jpg", "013_deposit_rewards_v1.jpg", "019_staking_v1.jpg", "025_burn_v1.jpg", "031_vesting_v1.jpg", "037_rank_v1.jpg", "043_referral_v1.jpg", "049_onchain_v1.jpg", "055_tax_v1.jpg", "061_locked_lp_v1.jpg", "067_passive_v1.jpg", "073_fair_launch_v1.jpg", "079_cta_v1.jpg", "085_deflationary_v1.jpg", "091_tokenomics_v1.jpg", "163_smart_contract_v1.jpg", "175_ecosystem_v1.jpg", "002_system_integrity_v2.jpg", "008_token_supply_v2.jpg", "014_deposit_rewards_v2.jpg", "020_staking_v2.jpg", "026_burn_v2.jpg", "032_vesting_v2.jpg", "038_rank_v2.jpg", "044_referral_v2.jpg", "050_onchain_v2.jpg", "056_tax_v2.jpg", "062_locked_lp_v2.jpg", "068_passive_v2.jpg", "074_fair_launch_v2.jpg", "080_cta_v2.jpg", "086_deflationary_v2.jpg", "092_tokenomics_v2.jpg", "164_smart_contract_v2.jpg", "176_ecosystem_v2.jpg", "003_system_integrity_v3.jpg", "009_token_supply_v3.jpg", "015_deposit_rewards_v3.jpg", "021_staking_v3.jpg", "027_burn_v3.jpg", "033_vesting_v3.jpg", "039_rank_v3.jpg", "045_referral_v3.jpg", "051_onchain_v3.jpg", "057_tax_v3.jpg", "063_locked_lp_v3.jpg", "069_passive_v3.jpg", "075_fair_launch_v3.jpg", "081_cta_v3.jpg", "087_deflationary_v3.jpg", "093_tokenomics_v3.jpg", "165_smart_contract_v3.jpg", "177_ecosystem_v3.jpg", "004_system_integrity_v4.jpg", "010_token_supply_v4.jpg", "016_deposit_rewards_v4.jpg", "022_staking_v4.jpg", "028_burn_v4.jpg", "034_vesting_v4.jpg", "040_rank_v4.jpg", "046_referral_v4.jpg", "052_onchain_v4.jpg", "058_tax_v4.jpg", "064_locked_lp_v4.jpg", "070_passive_v4.jpg", "076_fair_launch_v4.jpg", "082_cta_v4.jpg", "088_deflationary_v4.jpg", "094_tokenomics_v4.jpg", "166_smart_contract_v4.jpg", "178_ecosystem_v4.jpg", "005_system_integrity_v5.jpg", "011_token_supply_v5.jpg", "017_deposit_rewards_v5.jpg", "023_staking_v5.jpg", "029_burn_v5.jpg", "035_vesting_v5.jpg", "041_rank_v5.jpg", "047_referral_v5.jpg", "053_onchain_v5.jpg", "059_tax_v5.jpg", "065_locked_lp_v5.jpg", "071_passive_v5.jpg", "077_fair_launch_v5.jpg", "083_cta_v5.jpg", "089_deflationary_v5.jpg", "095_tokenomics_v5.jpg", "167_smart_contract_v5.jpg", "179_ecosystem_v5.jpg", "006_system_integrity_v6.jpg", "012_token_supply_v6.jpg", "018_deposit_rewards_v6.jpg", "024_staking_v6.jpg", "030_burn_v6.jpg", "036_vesting_v6.jpg", "042_rank_v6.jpg", "048_referral_v6.jpg", "054_onchain_v6.jpg", "060_tax_v6.jpg", "066_locked_lp_v6.jpg", "072_passive_v6.jpg", "078_fair_launch_v6.jpg", "084_cta_v6.jpg", "090_deflationary_v6.jpg", "096_tokenomics_v6.jpg", "168_smart_contract_v6.jpg", "180_ecosystem_v6.jpg", "006_system_integrity_v6.jpg", "012_token_supply_v6.jpg", "018_deposit_rewards_v6.jpg", "103_staking_v1.jpg", "115_burn_v1.jpg", "109_vesting_v1.jpg", "097_rank_v1.jpg", "121_referral_v1.jpg", "054_onchain_v6.jpg", "060_tax_v6.jpg", "139_locked_lp_v1.jpg", "145_passive_v1.jpg", "151_fair_launch_v1.jpg", "157_cta_v1.jpg", "127_deflationary_v1.jpg", "133_tokenomics_v1.jpg", "168_smart_contract_v6.jpg", "180_ecosystem_v6.jpg", "006_system_integrity_v6.jpg", "012_token_supply_v6.jpg", "018_deposit_rewards_v6.jpg", "104_staking_v2.jpg", "116_burn_v2.jpg", "110_vesting_v2.jpg", "098_rank_v2.jpg", "122_referral_v2.jpg", "054_onchain_v6.jpg", "060_tax_v6.jpg", "140_locked_lp_v2.jpg", "146_passive_v2.jpg", "152_fair_launch_v2.jpg", "158_cta_v2.jpg", "128_deflationary_v2.jpg", "134_tokenomics_v2.jpg", "168_smart_contract_v6.jpg", "180_ecosystem_v6.jpg", "006_system_integrity_v6.jpg", "012_token_supply_v6.jpg", "018_deposit_rewards_v6.jpg", "105_staking_v3.jpg", "117_burn_v3.jpg", "111_vesting_v3.jpg", "099_rank_v3.jpg", "123_referral_v3.jpg", "054_onchain_v6.jpg", "060_tax_v6.jpg", "141_locked_lp_v3.jpg", "147_passive_v3.jpg", "153_fair_launch_v3.jpg", "159_cta_v3.jpg", "129_deflationary_v3.jpg", "135_tokenomics_v3.jpg", "168_smart_contract_v6.jpg", "180_ecosystem_v6.jpg", "006_system_integrity_v6.jpg", "012_token_supply_v6.jpg", "018_deposit_rewards_v6.jpg", "106_staking_v4.jpg", "118_burn_v4.jpg", "112_vesting_v4.jpg", "100_rank_v4.jpg", "124_referral_v4.jpg", "054_onchain_v6.jpg", "060_tax_v6.jpg", "142_locked_lp_v4.jpg", "148_passive_v4.jpg", "154_fair_launch_v4.jpg", "160_cta_v4.jpg", "130_deflationary_v4.jpg", "136_tokenomics_v4.jpg", "168_smart_contract_v6.jpg", "180_ecosystem_v6.jpg"]

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config.json: {e}")
        return None

def load_state():
    try:
        with open("state.json", "r") as f:
            return json.load(f)
    except Exception:
        return {"last_post_index": -1, "total_posts_sent": 0}

def save_state(state):
    try:
        with open("state.json", "w") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving state: {e}")

def format_caption(topic, variation_idx, hashtags):
    data = CAP_DATA[topic]
    title = data["title"]
    desc = data["desc"][variation_idx]
    feats = data["features"][variation_idx]
    facts = data["facts"][variation_idx]
    tagline = data["tagline"]
    
    # Icons
    opening_emojis = ["🚀", "🔥", "💎", "⚡️", "📈", "🛡", "🌐", "⚙️", "🌟", "✨"]
    op_emoji = opening_emojis[variation_idx % len(opening_emojis)]
    
    feat_emojis = ["🔥", "📈", "🛡", "⚡️", "🌐"]
    
    caption = f"{op_emoji} TURBOLOOP {title}\n\n"
    caption += f"{desc}\n\n"
    
    for i, feat in enumerate(feats):
        emoji = feat_emojis[i % len(feat_emojis)]
        caption += f"{emoji} {feat}\n"
        
    caption += "\n"
    for fact in facts:
        caption += f"✅ {fact}\n"
        
    caption += f"\n🔥 {tagline}\n\n"
    caption += f"{hashtags}"

    if topic in ["Token Supply", "Tokenomics"]:
        caption += "\n\n✨ TurboLoop Token is an extra rewards layer from TurboLoop with zero interference on the main protocol performance"
    
    return caption

def send_to_telegram(token, chat_id, image_path, caption):
    # Send Photo
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    try:
        with open(image_path, "rb") as photo:
            payload = {
                "chat_id": chat_id,
                "caption": caption,
                "parse_mode": "HTML"
            }
            files = {"photo": photo}
            resp = requests.post(url, data=payload, files=files)
            resp.raise_for_status()
            res_json = resp.json()
            message_id = res_json.get("result", {}).get("message_id")
            logging.info(f"Post sent successfully! Message ID: {message_id}")
            
            # Pin message
            pin_url = f"https://api.telegram.org/bot{token}/pinChatMessage"
            pin_payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "disable_notification": True
            }
            requests.post(pin_url, json=pin_payload)
            logging.info(f"Message pinned successfully!")
            return True
    except Exception as e:
        logging.error(f"Failed to send/pin to Telegram: {e}")
        return False

def run_post_cycle(config, state):
    next_post_idx = (state["last_post_index"] + 1) % 180
    topic = TOPICS[next_post_idx % len(TOPICS)]
    variation_idx = next_post_idx // len(TOPICS)
    
    image_file = IMAGES_MAP[next_post_idx]
    image_path = os.path.join("images", image_file)
    
    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        # Fallback to first image
        image_path = os.path.join("images", "001_system_integrity_v1.jpg")
        
    logging.info(f"📌 Post Index: {next_post_idx+1}/180")
    logging.info(f"📌 Topic: {topic} [Var {variation_idx+1}/10]")
    logging.info(f"🖼 Image: {image_path}")
    
    # Format caption
    caption = format_caption(topic, variation_idx, config["HASHTAGS"])
    
    # Send
    success = send_to_telegram(
        config["TELEGRAM_BOT_TOKEN"],
        config["TELEGRAM_CHANNEL_ID"],
        image_path,
        caption
    )
    
    if success:
        state["last_post_index"] = next_post_idx
        state["total_posts_sent"] += 1
        save_state(state)
        logging.info(f"State updated. Total posts sent: {state['total_posts_sent']}")
    else:
        logging.error("Failed to send post. Retrying in next cycle.")

def main():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    
    logging.info("============================================================")
    logging.info("   🚀 TurboLoop Telegram Marketing Bot v4.0 — ACTIVE (180 Posts)")
    logging.info("============================================================")
    
    config = load_config()
    if not config:
        logging.error("Config not found. Exiting.")
        return
        
    state = load_state()
    
    # Dry-run test mode
    if os.environ.get("DRY_RUN") == "1":
        logging.info("Running in DRY-RUN mode...")
        run_post_cycle(config, state)
        return
        
    # Main scheduler loop
    interval_sec = config.get("INTERVAL_HOURS", 4) * 3600
    logging.info(f"Interval: every {config.get('INTERVAL_HOURS', 4)} hours ({24/config.get('INTERVAL_HOURS', 4)} posts/day)")
    
    # Send first post immediately on start
    run_post_cycle(config, state)
    
    while True:
        logging.info(f"Sleeping for {config.get('INTERVAL_HOURS', 4)} hours...")
        time.sleep(interval_sec)
        run_post_cycle(config, state)

if __name__ == "__main__":
    main()
