# 🔍 Merkle Tree Contract Verification (PoC)

## 📜 Overview
Merkle Trees enhance **contract integrity** in **smart contracts and digital agreements** by ensuring **security, efficiency, and verifiability**.

### **🔒 Security & Tamper Detection**
- **Even the smallest change—whether it’s a word, punctuation, or spacing—completely alters the Merkle root.**
- Every clause is **hashed individually**, meaning **any modification cascades upward**, affecting parent nodes and ultimately the root.
- Used in **legal agreements**, blockchain-based **smart contracts**, and **digital audits**.

### **⚡ Efficiency**
- **Only the Merkle root** is stored instead of entire contracts, reducing storage needs while maintaining **proof of integrity**.  
- Common in **document management systems**, **compliance tracking**, and **blockchain applications**.

### **✅ Easy Verification**
- Instead of comparing entire contracts line by line, **only the Merkle roots are checked**.  
- If the roots match, contracts are **identical**; if not, a change has been **detected**.  
- Used by **lawyers, auditors, and distributed systems** for quick verification.

---

## 💼 Legal Control & Compliance
Merkle Trees can be used to **validate and enforce compliance in legal contracts**, ensuring **document authenticity and tamper-proof tracking**.

✅ **Auditable Contracts** – Businesses and legal firms can verify contract versions **without exposing sensitive details**.  
✅ **Regulatory Compliance** – Government and financial institutions can store **Merkle Roots for signed agreements**, ensuring compliance while keeping terms private.  
✅ **Tamper-Proof Agreement Storage** – If a dispute arises, the original contract **Merkle Root can verify legitimacy** without requiring full disclosure.  
✅ **Privacy-Preserving Legal Proofs** – A Merkle proof can **confirm specific contract clauses exist** while hiding unrelated terms.

## Blockchain Smart Contracts**  
In **Ethereum and Bitcoin**, Merkle Trees help track transactions efficiently. When dealing with legal contracts stored on the blockchain, the Merkle root ensures authenticity **without revealing confidential contract details**.

---

## 🛠 How It Works
1️⃣ **Contracts are split into individual clauses** → Each clause is **hashed separately** using **SHA-256**.  
2️⃣ **Merkle Tree is built** → Hashes are combined **layer by layer** until a **single root hash** is generated.  
3️⃣ **Any Clause Change Alters the Entire Tree** → Since **each level depends on lower hashes**, a **single modification propagates upward**, changing **every dependent node** and ultimately the **Merkle Root**.  
4️⃣ **Merkle Roots are compared** → If they match, contracts are identical; otherwise, modifications occurred.  
5️⃣ **Clause-Level Comparison** → If roots don’t match, hash differences help **pinpoint changed sections**.  
6️⃣ **Merkle Proofs are generated** → Allows verification of **specific clauses** without revealing the full contract.  

---

## 🚀 Features
✅ **Merkle Tree Generation** – Converts contract clauses into a **hierarchical hash structure**.  
✅ **Contract Integrity Checking** – Compares Merkle Roots to detect modifications.  
✅ **Clause-Level Verification** – Identifies specific changes in contract clauses.  
✅ **Merkle Proof Generation** – Provides cryptographic validation for **individual clauses**.  
✅ **Logging & Auditing** – Saves verification results for **historical tracking**.  
✅ **Preserves Formatting** – Ensures spaces in contracts are **maintained for accuracy**.  

---

## 💻 Installation & Usage

### 1️⃣ Install Dependencies
This project uses **Python 3.x**. No external dependencies required.

```bash
git clone <repo-url>
cd merkle-proof-verification
python3 contract_verification.py
```

### 2️⃣ Example Contract Comparison
Modify `contract_v1` and `contract_v2` in `contract_verification.py`, then run:

```bash
python3 contract_verification.py
```

Example output:
```
🔑 Merkle Root V1: abc123...
🔑 Merkle Root V2: xyz456...
🛡️ Contracts are different.
🔎 Clause-Level Comparison:
   Clause 2: ❌ Difference
      🔹 V1: The seller provides a 1-year warranty.
      🔹 V2: The seller provides a 2-year warranty.
```

---

## 🛡️ Merkle Proof Verification
If you only need to verify a **single clause**, use Merkle proofs:

```python
proof = get_merkle_proof(tree_v2, hashes_v2[1])  # Clause 2
verified = verify_merkle_proof(proof, hashes_v2[1], root_v2)
print("Proof Verification:", verified)  # ✅ True if Clause 2 is valid
```

---
