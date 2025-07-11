export async function fetchHealth() {
  const response = await fetch('/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '{ health }' }),
  });
  const { data } = await response.json();
  return data?.health || 'Unavailable';
} 