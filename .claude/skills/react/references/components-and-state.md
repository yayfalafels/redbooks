# Components and state

How components hold state and how forms convert their values.

## Rules

01. one component per file, named for what it shows.
02. server data lives in the query cache. Component state holds only what the user is editing or choosing.
03. a form validates on submit and shows each error beside its field.
04. a component that loads data renders its loading, empty and error states.

## Lessons

### treat form values as strings at the boundary

Select and input values are strings. Keep them as strings in form state, and convert ids and amounts once, at submit.

**why**: a numeric id bound to a select whose option values are strings matched nothing, silently.

Example:

```tsx
const [accountId, setAccountId] = useState<string>("");
const [amount, setAmount] = useState<string>("");

function onSubmit() {
  save.mutate({ account_id: Number(accountId), amount: amount.trim() });  // amount stays a decimal string
}

<select value={accountId} onChange={(e) => setAccountId(e.target.value)}>
  {accounts.map((a) => <option key={a.id} value={String(a.id)}>{a.name}</option>)}
</select>
```
