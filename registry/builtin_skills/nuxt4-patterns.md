# Skill: Nuxt 4 Patterns

## When to Use
- Hydration mismatches between server HTML and client state
- Route-level rendering decisions such as prerender, SWR, ISR, or client-only sections
- Performance work around lazy loading, lazy hydration, or payload size
- Page or component data fetching with `useFetch`, `useAsyncData`, or `$fetch`
- Nuxt routing issues tied to route params, middleware, or SSR/client differences

## Policy
Level: ALLOW

## Instructions
## Hydration Safety

- Keep the first render deterministic. Do not put `Date.now()`, `Math.random()`, browser-only APIs, or storage reads directly into SSR-rendered template state.
- Move browser-only logic behind `onMounted()`, `import.meta.client`, `ClientOnly`, or a `.client.vue` component when the server cannot produce the same markup.
- Use Nuxt's `useRoute()` composable, not the one from `vue-router`.
- Do not use `route.fullPath` to drive SSR-rendered markup. URL fragments are client-only, which can create hydration mismatches.
- Treat `ssr: false` as an escape hatch for truly browser-only areas, not a default fix for mismatches.

## Data Fetching

- Prefer `await useFetch()` for SSR-safe API reads in pages and components. It forwards server-fetched data into the Nuxt payload and avoids a second fetch on hydration.
- Use `useAsyncData()` when the fetcher is not a simple `$fetch()` call, when you need a custom key, or when you are composing multiple async sources.
- Give `useAsyncData()` a stable key for cache reuse and predictable refresh behavior.
- Keep `useAsyncData()` handlers side-effect free. They can run during SSR and hydration.
- Use `$fetch()` for user-triggered writes or client-only actions, not top-level page data that should be hydrated from SSR.
- Use `lazy: true`, `useLazyFetch()`, or `useLazyAsyncData()` for non-critical data that should not block navigation. Handle `status === 'pending'` in the UI.
- Use `server: false` only for data that is not needed for SEO or the first paint.
- Trim payload size with `pick` and prefer shallower payloads when deep reactivity is unnecessary.

```ts
const route = useRoute()

const { data: article, status, error, refresh } = await useAsyncData(
  () => `article:${route.params.slug}`,
  () => $fetch(`/api/articles/${route.params.slug}`),
)

const { data: comments } = await useFetch(`/api/articles/${route.params.slug}/comments`, {
  lazy: true,
  server: false,
})
```

## Route Rules

Prefer `routeRules` in `nuxt.config.ts` for rendering and caching strategy:

```ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/products/**': { swr: 3600 },
    '/blog/**': { isr: true },
    '/admin/**': { ssr: false },
    '/api/**': { cache: { maxAge: 60 * 60 } },
  },
})
```

- `prerender`: static HTML at build time
- `swr`: serve cached content and revalidate in the background
- `isr`: incremental static regeneration on supported platforms
- `ssr: false`: client-rendered route
- `cache` or `redirect`: Nitro-level response behavior

Pick route rules per route group, not globally. Marketing pages, catalogs, dashboards, and APIs usually need different strategies.

## Lazy Loading and Performance

- Nuxt already code-splits pages by route. Keep route boundaries meaningful before micro-optimizing component splits.
- Use the `Lazy` prefix to dynamically import non-critical components.
- Conditionally render lazy components with `v-if` so the chunk is not loaded until the 

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with nuxt 4 patterns"
Agent: [follows the skill instructions to complete the task]
