"""Offline bot-only rehydration, no foreign system activation."""
from bot_runtime import SHA, validate_system

def rehydrate(manifest, pointer, observed_head, expected_branch):
    blockers = list(validate_system(manifest, pointer)['blockers'])
    if not SHA.fullmatch(str(observed_head)):
        blockers.append('INVALID_OBSERVED_HEAD')
    if pointer.get('canonical_branch') != expected_branch:
        blockers.append('BRANCH_MISMATCH')
    if manifest.get('source_branch') != expected_branch:
        blockers.append('MANIFEST_BRANCH_MISMATCH')
    if manifest.get('identity_authority') != 'native_LYVRA_external':
        blockers.append('NATIVE_IDENTITY_BOUNDARY_MISMATCH')
    return {'status': 'BLOCKED' if blockers else 'PARTIAL', 'blockers': blockers, 'observed_head': observed_head, 'release_ready': False, 'discord_deployment': False, 'native_lyvra_rehydrated': False}
