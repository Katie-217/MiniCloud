Firebase Auth Web 5.15.3 from pub.dev, BSD license retained.
Patch: attach the local Auth emulator before awaiting restored session initialization when MINICLOUD_LOCAL_EMULATORS=true. Upstream restored emulator settings only in debug mode. No production Firebase configuration included.
