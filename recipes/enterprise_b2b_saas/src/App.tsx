import { useQuery } from '@tanstack/react-query';
import {
  createColumnHelper,
  createSortedRowModel,
  rowSortingFeature,
  sortFn_alphanumeric,
  tableFeatures,
  useTable,
} from '@tanstack/react-table';
import { z } from 'zod';

// One schema validates the API response and gives the row type.
const Account = z.object({
  id: z.string(),
  name: z.string().min(1),
  plan: z.enum(['free', 'team', 'enterprise']),
  seats: z.number().int().nonnegative(),
});
type Account = z.infer<typeof Account>;

// Mock API: a local promise, no network.
const MOCK_ACCOUNTS: unknown = [
  { id: 'a1', name: 'Acme Corp', plan: 'enterprise', seats: 420 },
  { id: 'a2', name: 'Globex', plan: 'team', seats: 35 },
  { id: 'a3', name: 'Initech', plan: 'free', seats: 3 },
  { id: 'a4', name: 'Umbrella', plan: 'enterprise', seats: 1200 },
];

async function fetchAccounts(): Promise<Account[]> {
  const raw = await new Promise<unknown>((resolve) => setTimeout(() => resolve(MOCK_ACCOUNTS), 300));
  return z.array(Account).parse(raw);
}

// Features and columns live at module scope so they stay stable across renders.
const features = tableFeatures({
  rowSortingFeature,
  sortedRowModel: createSortedRowModel(),
  sortFns: { alphanumeric: sortFn_alphanumeric },
});
const helper = createColumnHelper<typeof features, Account>();
const columns = helper.columns([
  helper.accessor('name', { header: 'Account' }),
  helper.accessor('plan', { header: 'Plan' }),
  helper.accessor('seats', { header: 'Seats' }),
]);
const EMPTY: Account[] = [];

export function App() {
  const { data, isPending, error } = useQuery({ queryKey: ['accounts'], queryFn: fetchAccounts });
  const table = useTable({ features, columns, data: data ?? EMPTY });

  return (
    <main className="mx-auto max-w-3xl p-8 font-sans text-slate-900">
      <h1 className="mb-4 text-2xl font-semibold">Accounts</h1>
      {isPending && <p className="text-slate-500">Loading...</p>}
      {error && <p className="text-red-600">Could not load accounts: {error.message}</p>}
      {data && (
        <table className="w-full border-collapse text-left text-sm">
          <thead>
            {table.getHeaderGroups().map((group) => (
              <tr key={group.id} className="border-b border-slate-300">
                {group.headers.map((header) => (
                  <th key={header.id} className="p-2 font-medium">
                    <button
                      type="button"
                      className="cursor-pointer hover:underline"
                      onClick={header.column.getToggleSortingHandler()}
                    >
                      <table.FlexRender header={header} />
                      {{ asc: ' ▲', desc: ' ▼', none: '' }[header.column.getIsSorted() || 'none']}
                    </button>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="border-b border-slate-100 hover:bg-slate-50">
                {row.getAllCells().map((cell) => (
                  <td key={cell.id} className="p-2">
                    <table.FlexRender cell={cell} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
