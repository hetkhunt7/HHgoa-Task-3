# Face Identification & Blockchain Verification

A proof-of-concept pipeline for **face identification, reverse image search, social-media evidence discovery, and blockchain-based evidence integrity verification**.

This project was developed for **HH Goa 2026 – Shortlisting Task 3: Face Identification & Blockchain Verification**.

---

## Overview

The system takes a face image as input and processes it through an end-to-end pipeline:

```text
Face Image
    ↓
Face Detection
    ↓
ArcFace Face Embedding
    ↓
Google Lens Reverse Image Search
    ↓
Social-Media Candidate Discovery
    ↓
Evidence JSON
    ↓
SHA-256 Fingerprint
    ↓
Polygon Amoy Blockchain
    ↓
On-Chain Verification
```

The goal is to demonstrate how discovered web evidence can be given a tamper-evident fingerprint and independently verified using blockchain.

> **Important:** Blockchain verifies the integrity of the recorded evidence. It does not independently prove that a person owns a social-media account or that a discovered post is the original source.

---

# Features

* Face detection using **RetinaFace**
* Face representation using **ArcFace**
* 512-dimensional face embedding
* Local image upload to SerpApi
* Google Lens reverse-image search
* Extraction of visual and exact matches
* Detection of social-media results
* Structured evidence generation
* Deterministic evidence canonicalization
* SHA-256 evidence fingerprinting
* Polygon Amoy testnet blockchain recording
* On-chain hash retrieval
* Evidence integrity verification

---

# Technology Stack

| Component             | Technology              |
| --------------------- | ----------------------- |
| Programming Language  | Python                  |
| Face Detection        | RetinaFace              |
| Face Recognition      | DeepFace                |
| Face Model            | ArcFace                 |
| Reverse Image Search  | Google Lens via SerpApi |
| Blockchain            | Polygon Amoy            |
| Smart Contract        | Solidity                |
| Blockchain Library    | Web3.py                 |
| Hashing               | SHA-256                 |
| Environment Variables | python-dotenv           |

---

# Project Structure

```text
face-chain-verifier/
│
├── app.py
├── face_encoder.py
├── web_search.py
├── evidence.py
├── blockchain.py
│
├── contracts/
│   └── EvidenceRegistry.sol
│
├── evidence.json
├── face_crop.jpg
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

# Pipeline

## 1. Face Detection and Encoding

The input image is processed using DeepFace.

RetinaFace detects the face and ArcFace generates a facial embedding.

The generated embedding contains:

```text
512 dimensions
```

The system also extracts and saves the detected face as:

```text
face_crop.jpg
```

This demonstrates the face-identification component of the task.

---

## 2. Reverse Image Search

The original local image is uploaded to the SerpApi Image API.

SerpApi returns an `image_id`.

That ID is then used to perform a Google Lens search.

The search can return:

* Exact matches
* Visual matches
* Web pages
* Social-media posts
* Other visually related content

---

## 3. Social-Media Candidate Discovery

The Google Lens results are inspected for publicly indexed social-media URLs.

Currently supported platforms include:

```text
Instagram
X / Twitter
Facebook
TikTok
YouTube
Reddit
```

The system extracts information such as:

```text
Platform
Title
URL
Source
Match type
Thumbnail
```

Example:

```text
Platform : instagram.com
Title    : ...
URL      : https://www.instagram.com/...
Type     : visual
```

### Important limitation

A reverse-image-search result is not automatically considered the original post.

A social-media result may be:

* An original post
* A repost
* A fan account
* A news page
* A visually similar image

Therefore, the system treats the result as a **discovered candidate/evidence source**, rather than automatically claiming ownership or originality.

---

# 4. Evidence Generation

After a social-media candidate is selected, the system creates a structured evidence record.

Example:

```json
{
    "timestamp": "2026-09-07T...",
    "face": {
        "model": "ArcFace",
        "embedding_dimensions": 512
    },
    "social_match": {
        "platform": "instagram.com",
        "title": "Example post",
        "url": "https://www.instagram.com/example/",
        "source": "Instagram",
        "match_type": "visual"
    }
}
```

The evidence is saved locally as:

```text
evidence.json
```

---

# 5. SHA-256 Fingerprinting

The evidence JSON is converted into a deterministic canonical representation.

The system then calculates a SHA-256 hash:

```text
Evidence JSON
      ↓
Canonical JSON
      ↓
SHA-256
      ↓
64-character hexadecimal fingerprint
```

Example:

```text
7e8c4c....................
```

The fingerprint acts as a compact representation of the evidence record.

If any recorded information changes, the resulting SHA-256 hash changes.

For example:

```text
Original URL
    ↓
SHA-256 A

Modified URL
    ↓
SHA-256 B
```

Therefore:

```text
SHA-256 A ≠ SHA-256 B
```

---

# 6. Blockchain Verification

The SHA-256 evidence fingerprint is recorded on the **Polygon Amoy testnet** using a Solidity smart contract.

The blockchain record contains:

```text
Evidence Hash
Source URL
Timestamp
Submitter Address
```

The actual image and face embedding are not stored on-chain.

This keeps the blockchain record lightweight while providing a tamper-evident reference to the evidence.

---

# Smart Contract

The project uses an `EvidenceRegistry` Solidity contract.

Main function:

```solidity
registerEvidence(
    string memory evidenceHash,
    string memory sourceUrl
)
```

Evidence can later be retrieved using its blockchain record ID.

The retrieved hash is compared with a newly calculated hash:

```text
Current Evidence
      ↓
SHA-256
      ↓
Calculated Hash
      ↓
Compare
      ↑
On-Chain Hash
```

If both hashes match:

```text
✓ VERIFIED
```

If they differ:

```text
✗ VERIFICATION FAILED
```

---

# Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd face-chain-verifier
```

---

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file:

```text
SERPAPI_KEY=your_serpapi_key

POLYGON_RPC_URL=your_polygon_amoy_rpc_url

PRIVATE_KEY=your_test_wallet_private_key

CONTRACT_ADDRESS=your_deployed_contract_address
```

### Security

Never commit `.env` to GitHub.

The private key should belong to a **test wallet only**.

The repository should contain:

```text
.env.example
```

instead of the real `.env`.

Example:

```text
SERPAPI_KEY=

POLYGON_RPC_URL=

PRIVATE_KEY=

CONTRACT_ADDRESS=
```

---

# Running the Application

Run:

```powershell
python app.py
```

The application asks for the path of an image:

```text
Enter image path:
```

Example:

```text
../srk.jpg
```

The pipeline then performs:

```text
[1/6] Processing face...
[2/6] Uploading image...
[3/6] Searching Google Lens...
[4/6] Finding social-media match...
[5/6] Creating evidence fingerprint...
[6/6] Blockchain verification...
```

---

# Example Output

```text
╔══════════════════════════════════════════════╗
║       FACE → WEB → BLOCKCHAIN                ║
║          Evidence Verification               ║
╚══════════════════════════════════════════════╝

Enter image path: ../image.jpg

[1/6] Processing face...
      ✓ Face detected
      ✓ ArcFace embedding generated
      Embedding dimensions: 512

[2/6] Uploading image to SerpApi...
      ✓ Image uploaded

[3/6] Searching Google Lens...
      ✓ Google Lens search completed
      ✓ Results returned: 12

[4/6] Finding social-media match...
      ✓ Social-media candidate found

[5/6] Creating evidence fingerprint...
      ✓ Evidence saved: evidence.json
      ✓ SHA-256 fingerprint generated

[6/6] Blockchain verification...
      ✓ Evidence registered
      ✓ Transaction confirmed
      ✓ On-chain hash retrieved
      ✓ Hashes match

══════════════════════════════════════════════
             VERIFICATION SUCCESS
══════════════════════════════════════════════

Evidence Integrity : VERIFIED
Blockchain Network  : Polygon Amoy
```

---

# Blockchain Verification Demonstration

The project can demonstrate tamper detection.

### Original evidence

```text
Evidence
   ↓
SHA-256 A
   ↓
Blockchain
```

After modifying the evidence:

```text
Modified Evidence
   ↓
SHA-256 B
```

The system compares:

```text
SHA-256 A
     vs
SHA-256 B
```

Since:

```text
A ≠ B
```

the system reports:

```text
✗ VERIFICATION FAILED
```

This demonstrates that the evidence record has been modified after the blockchain fingerprint was recorded.

---

# Why Blockchain?

Traditional storage can allow previously recorded evidence to be modified without an obvious historical reference.

This project stores the evidence fingerprint on a blockchain.

The blockchain provides:

* Timestamped recording
* Tamper-evident history
* Public verification
* Independent hash comparison

Only the fingerprint and relevant metadata are stored on-chain.

---

# Privacy and Security

The project is designed around publicly available web evidence.

The system should only be used with:

* Images you have permission to process
* Publicly accessible content
* Authorized demonstrations
* Public figures or test subjects where appropriate

Do not use the system to identify or track private individuals without appropriate authorization.

Sensitive raw biometric data should not be stored on the blockchain.

---

# Limitations

This is a proof-of-concept system and has several limitations.

### Face recognition

Face embeddings indicate similarity; they do not constitute absolute proof of identity.

### Reverse image search

Google Lens results depend on what content is publicly indexed and available to the search engine.

### Social-media discovery

A discovered social-media post may be a repost or visually similar result rather than the original publication.

### Blockchain

Blockchain verifies the integrity of the recorded evidence fingerprint. It does not independently verify:

* Who owns the account
* Whether the discovered post is authentic
* Whether the person in the image is actually the claimed person
* Whether the source originally created the image

---

# Future Improvements

Possible improvements include:

* Better ranking of social-media candidates
* Original-post detection
* Official-account verification
* Multiple-source evidence aggregation
* Confidence scoring
* Face similarity thresholds
* Evidence screenshots
* IPFS storage for evidence artifacts
* Automatic blockchain verification
* Web interface
* Multi-face detection
* Database-based evidence history
* Support for additional blockchain networks

---

# Competition Requirement Mapping

| Requirement            | Implementation               |
| ---------------------- | ---------------------------- |
| Face scan input        | Local image input            |
| Face detection         | RetinaFace                   |
| Face encoding          | ArcFace                      |
| Web/social search      | Google Lens via SerpApi      |
| Matching content       | Visual/exact Lens results    |
| Social-media discovery | Social-domain filtering      |
| Evidence creation      | `evidence.py`                |
| Fingerprinting         | SHA-256                      |
| Blockchain             | Polygon Amoy                 |
| Blockchain storage     | `EvidenceRegistry.sol`       |
| Verification           | On-chain hash comparison     |
| Demonstration          | Terminal end-to-end pipeline |

---

# Project Flow

```text
                 ┌─────────────────┐
                 │   Face Image    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ RetinaFace      │
                 │ Face Detection  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ ArcFace         │
                 │ 512D Embedding  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ SerpApi Image   │
                 │ Upload          │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Google Lens     │
                 │ Reverse Search  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Social-Media    │
                 │ Candidate       │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Evidence JSON   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ SHA-256 Hash    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Polygon Amoy    │
                 │ Blockchain      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Retrieve Hash   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Hash Comparison │
                 └────────┬────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
              MATCH             MISMATCH
                 │                 │
                 ▼                 ▼
             VERIFIED          TAMPERED
```

---

# Conclusion

This project demonstrates an end-to-end approach to connecting **computer vision, reverse image search, web evidence discovery, cryptographic hashing, and blockchain verification**.

The key principle is:

```text
Discover → Record → Hash → Store → Recalculate → Verify
```

The blockchain provides a tamper-evident reference for the evidence discovered during the pipeline, while the face-recognition and reverse-search components provide the initial evidence discovery mechanism.
