# API calls

How the frontend calls the API, keeps views fresh, and hands off to sign-in.

## Rules

01. one API client module wraps `fetch`, sends the session cookie, parses JSON, and turns a non-2xx response into an error with the server's message.
02. a 401 from any call starts the sign-in redirect.
03. money arrives as decimal strings and stays a string until a calculation needs it.

## Lessons

### refresh every view of changed data and keep in-progress input

After a write, every view that shows the changed data reloads: the list, the detail, and any total or balance. A refresh merges the server data with the fields the user is editing, so half-typed input survives.

**why**: a saved change left its list stale, a queue stayed stale after a background run, and a refresh replaced the whole form model and erased half-typed input.

Example, with a query cache:

```tsx
const save = useMutation({
  mutationFn: (body: EntryIn) => api.post(`/api/accounts/${accountId}/entries`, body),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["entries", accountId] });
    queryClient.invalidateQueries({ queryKey: ["balance", accountId] });
    queryClient.invalidateQueries({ queryKey: ["statements"] });
  },
});
```

### capture the requested path before redirecting to sign-in

Store the requested path in a variable first, then redirect. Reading the location after the redirect has started returns the sign-in page itself.

**why**: a chained call read the path after the redirect had changed it, so sign-in returned to the sign-in page. The design snippet carried the same defect.

Example:

```ts
export function redirectToSignIn() {
  const next = window.location.pathname + window.location.search;
  window.location.assign(`/auth/login?next=${encodeURIComponent(next)}`);
}
```
