# Tests

Backend API and encrypted-storage integration tests are in
`backend/tests/`. The cross-component test layout is reserved for Windows
service lifecycle, offline desktop and packaged restore tests.

The current test plan, including offline and negative cases, is in the
[first offline slice contract](../docs/implementation/first-offline-slice.md).
All fixtures, uploaded documents, logs and backups must be synthetic.
