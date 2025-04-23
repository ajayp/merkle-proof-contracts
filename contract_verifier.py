import hashlib
from typing import List, Tuple, Literal

# --- Helpers ---
def hash_data(data: str) -> str:
    """Generate SHA-256 hash for the given string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_merkle_tree(leaf_hashes: List[str]) -> List[List[str]]:
    """Builds a Merkle Tree ensuring unpaired nodes are properly hashed."""
    if not leaf_hashes:
        return [] # Handle empty input

    tree = [leaf_hashes]
    while len(tree[-1]) > 1:
        level = tree[-1]
        next_level = []

        # Process in pairs, properly hashing unpaired nodes
        for i in range(0, len(level), 2):
            left_child = level[i]
            # Handle odd number of nodes by duplicating the last one
            right_child = level[i + 1] if i + 1 < len(level) else level[i]

            # Hash the pair (left + right)
            combined = hash_data(left_child + right_child)
            next_level.append(combined)

        tree.append(next_level)
    return tree

def get_merkle_root(tree: List[List[str]]) -> str:
    """Returns the Merkle root."""
    return tree[-1][0] if tree and tree[-1] else 'EMPTY_CONTRACT' # Check if root level is not empty

def compare_merkle_roots(root1: str, root2: str) -> bool:
    """Compares two Merkle roots for equality."""
    return root1 == root2

def compare_and_print_clause_hashes(hashes_v1, hashes_v2, clauses_v1, clauses_v2):
    """
    Compares individual clause hashes and prints differecnes in content.
    Assumes clauses_v1 corresponds to hashes_v1 and clauses_v2 to hashes_v2.
    """
    print("\n🔎 Clause-Level Comparison:")
    min_len = min(len(hashes_v1), len(hashes_v2))
    max_len = max(len(hashes_v1), len(hashes_v2))

    for i in range(min_len):
        h1 = hashes_v1[i]
        h2 = hashes_v2[i]
        if h1 == h2:
            print(f"Clause {i+1}: ✅ Match")
        else:
            print(f"Clause {i+1}: ❌ Difference")
            print(f"   🔹 V1: {clauses_v1[i]}")
            print(f"   🔹 V2: {clauses_v2[i]}")

    # Report clauses only present in the longer version
    if max_len > min_len:
        print("\nAdditional Clauses:")
        if len(hashes_v1) > len(hashes_v2):
            # V1 is longer
            print("   🔹 V1 has additional clauses:")
            for i in range(min_len, max_len):
                print(f"      Clause {i+1}: {clauses_v1[i]}")
        else:
            # V2 is longer
            print("   🔹 V2 has additional clauses:")
            for i in range(min_len, max_len):
                 print(f"      Clause {i+1}: {clauses_v2[i]}")


# A Merkle proof is a list of (hash, side) tuples
# side is 'left' or 'right' indicating the position of the sibling
MerkleProof = List[Tuple[str, Literal['left', 'right']]]

def get_merkle_proof(tree: List[List[str]], target_hash: str) -> MerkleProof:
    """
    Generates a Merkle proof for a specific leaf hash.
    Proof consists of sibling hashes and their side relative to the target path.
    """
    if not tree or not tree[0]: # Ensure tree and leaf level are not empty
        return []

    proof_revised: MerkleProof = []
    current_hash_up = target_hash

    for level_index in range(len(tree) - 1): # Iterate up to the level before the root
        level = tree[level_index]
        found_in_level = False
        for i in range(0, len(level), 2):
            left_node = level[i]
            # Handle odd number of nodes by duplicating the last one, matching build_merkle_tree
            right_node = level[i + 1] if i + 1 < len(level) else level[i]

            if current_hash_up == left_node:
                # Target is the left node, sibling is the right
                # Append the sibling hash and its side ('right')
                proof_revised.append((right_node, 'right'))
                # Compute the parent hash for the next iteration (left + right)
                current_hash_up = hash_data(left_node + right_node)
                found_in_level = True
                break # Move to the next level up
            elif current_hash_up == right_node:
                 # Target is the right node, sibling is the left
                 # Append the sibling hash and its side ('left')
                 proof_revised.append((left_node, 'left'))
                 # Compute the parent hash for the next iteration (still left + right order as per build)
                 current_hash_up = hash_data(left_node + right_node)
                 found_in_level = True
                 break # Move to the next level up

        if not found_in_level:
            # This means the current_hash_up was not found in the expected level.
            # This could indicate an invalid target_hash or a broken tree structure.
            # For a POC, we can return an empty proof.
            return []

    # After the loop, current_hash_up should be the root.
    # The verification function will compare this computed root with the expected root.
    return proof_revised


def verify_merkle_proof(proof: MerkleProof, target_hash: str, merkle_root: str) -> bool:
    """
    Verifies a Merkle proof against the expected root.
    Uses the side information in the proof to correctly order hashes.
    """
    computed_hash = target_hash
    for sibling_hash, side in proof:
        if side == 'left':
            # Sibling is on the left, current_hash is on the right.
            # Concatenate sibling + current_hash
            computed_hash = hash_data(sibling_hash + computed_hash)
        elif side == 'right':
            # Sibling is on the right, current_hash is on the left.
            # Concatenate current_hash + sibling
            computed_hash = hash_data(computed_hash + sibling_hash)
        else:
            # Should not happen with Literal type hint, but good practice
            print(f"Error: Invalid side '{side}' in proof step.") # Added error print for debugging
            return False # Invalid side information

    # After processing all proof steps, computed_hash should be the root
    return computed_hash == merkle_root

def log_verification(root1: str, root2: str):
    """Logs contract verification results."""
    status = "✅ Identical" if root1 == root2 else "❌ Different"

    print(f"\n📜 [Verification Log]")
    print(f"Root V1: {root1}")
    print(f"Root V2: {root2}")
    print(f"Status: {status}")


def extract_clauses(text: str) -> List[str]:
    """Extracts clauses while preserving spaces and formatting."""
    # Split by newline and filter out lines that are empty *after* stripping whitespace
    return [line for line in text.strip().split("\n") if line.strip()]


# --- Example: Contract Analysis ---
contract_v1 = """
Clause 1: The buyer agrees to pay in full within 30 days.
Clause 2: The seller provides a 1-year warranty.
Clause 3: All disputes will be settled in California.
"""

contract_v2 = """
Clause 1: The buyer agrees to pay in full within 30 days.
Clause 2: The seller provides a 2-year warranty.
Clause 3: All disputes will be settled in California .
"""

contract_v3_identical_v1 = """
Clause 1: The buyer agrees to pay in full within 30 days.
Clause 2: The seller provides a 1-year warranty.
Clause 3: All disputes will be settled in California.
"""

contract_v4_different_clause_count = """
Clause 1: The buyer agrees to pay in full within 30 days.
Clause 2: The seller provides a 1-year warranty.
Clause 3: All disputes will be settled in California.
Clause 4: An additional clause.
"""


# Parse contracts
clauses_v1 = extract_clauses(contract_v1)
clauses_v2 = extract_clauses(contract_v2)
clauses_v3 = extract_clauses(contract_v3_identical_v1)
clauses_v4 = extract_clauses(contract_v4_different_clause_count)


# Hash each clause
hashes_v1 = [hash_data(clause) for clause in clauses_v1]
hashes_v2 = [hash_data(clause) for clause in clauses_v2]
hashes_v3 = [hash_data(clause) for clause in clauses_v3]
hashes_v4 = [hash_data(clause) for clause in clauses_v4]

# Build Merkle trees
tree_v1 = build_merkle_tree(hashes_v1)
tree_v2 = build_merkle_tree(hashes_v2)
tree_v3 = build_merkle_tree(hashes_v3)
tree_v4 = build_merkle_tree(hashes_v4)


# Compare roots
root_v1 = get_merkle_root(tree_v1)
root_v2 = get_merkle_root(tree_v2)
root_v3 = get_merkle_root(tree_v3)
root_v4 = get_merkle_root(tree_v4)


print("--- Overall Contract Comparison (using Merkle Root) ---")
print(f"V1 Root: {root_v1}")
print(f"V2 Root: {root_v2}")
print(f"V3 Root: {root_v3}")
print(f"V4 Root: {root_v4}")

print("\nV1 vs V2:", "Identical" if compare_merkle_roots(root_v1, root_v2) else "Different")
# Only print clause differences if roots differ AND the lists are non-empty for comparison
if not compare_merkle_roots(root_v1, root_v2) and clauses_v1 and clauses_v2:
    compare_and_print_clause_hashes(hashes_v1, hashes_v2, clauses_v1, clauses_v2)
elif not clauses_v1 or not clauses_v2:
     print("Cannot perform clause-level comparison due to empty clause lists.")


print("\nV1 vs V3:", "Identical" if compare_merkle_roots(root_v1, root_v3) else "Different")
# No need for clause comparison if identical

print("\nV1 vs V4:", "Identical" if compare_merkle_roots(root_v1, root_v4) else "Different")
# Only print clause differences if roots differ AND the lists are non-empty for comparison
if not compare_merkle_roots(root_v1, root_v4) and clauses_v1 and clauses_v4:
     compare_and_print_clause_hashes(hashes_v1, hashes_v4, clauses_v1, clauses_v4)
elif not clauses_v1 or not clauses_v4:
     print("Cannot perform clause-level comparison due to empty clause lists.")


print("\n\n--- Merkle Proof Demonstration ---")

# Demonstrate proof for a clause in V1 and verify it
clause_index_to_prove = 1 # Index 1 corresponds to Clause 2
if len(hashes_v1) > clause_index_to_prove:
    target_hash_v1 = hashes_v1[clause_index_to_prove]
    clause_content_v1 = clauses_v1[clause_index_to_prove]

    print(f"\nGenerating proof for: '{clause_content_v1}' (Clause {clause_index_to_prove + 1}) in V1")
    proof_v1 = get_merkle_proof(tree_v1, target_hash_v1)
    print("Proof:", proof_v1)

    is_verified_v1 = verify_merkle_proof(proof_v1, target_hash_v1, root_v1)
    print(f"Verification against V1 Root ({root_v1[:10]}...): {'✅ PASSED' if is_verified_v1 else '❌ FAILED'}")

    # Attempt to verify the same proof against the *incorrect* root V2
    print(f"Attempting verification against V2 Root ({root_v2[:10]}...):")
    is_verified_against_v2 = verify_merkle_proof(proof_v1, target_hash_v1, root_v2)
    print(f"Verification against V2 Root: {'✅ PASSED' if is_verified_against_v2 else '❌ FAILED'}")
    # This should fail because V2 has a different root
else:
    print(f"\nCannot demonstrate proof for Clause {clause_index_to_prove + 1} in V1 (not enough clauses).")


# Demonstrate proof for the corresponding clause in V2 (which is different)
if len(hashes_v2) > clause_index_to_prove:
    target_hash_v2 = hashes_v2[clause_index_to_prove]
    clause_content_v2 = clauses_v2[clause_index_to_prove]

    print(f"\nGenerating proof for: '{clause_content_v2}' (Clause {clause_index_to_prove + 1}) in V2")
    proof_v2 = get_merkle_proof(tree_v2, target_hash_v2)
    print("Proof:", proof_v2)

    is_verified_v2 = verify_merkle_proof(proof_v2, target_hash_v2, root_v2)
    print(f"Verification against V2 Root ({root_v2[:10]}...): {'✅ PASSED' if is_verified_v2 else '❌ FAILED'}")

    # Attempt to verify the proof from V2 against root V1
    print(f"Attempting verification against V1 Root ({root_v1[:10]}...):")
    is_verified_against_v1 = verify_merkle_proof(proof_v2, target_hash_v2, root_v1)
    print(f"Verification against V1 Root: {'✅ PASSED' if is_verified_against_v1 else '❌ FAILED'}")
     # This should fail because the proof is for the V2 tree structure/hashes
else:
     print(f"\nCannot demonstrate proof for Clause {clause_index_to_prove + 1} in V2 (not enough clauses).")

# Compare proofs directly (mostly for demonstration, not primary check)
# Only compare if both proofs were generated successfully
if 'proof_v1' in locals() and 'proof_v2' in locals():
    print("\nAre proofs for Clause 2 (V1 vs V2) identical?", proof_v1 == proof_v2) # Should be False
else:
    print("\nSkipping direct proof comparison as one or both proofs could not be generated.")


# Log the final comparison results for V1 and V2
log_verification(root_v1, root_v2)
