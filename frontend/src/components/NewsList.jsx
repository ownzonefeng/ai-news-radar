import { Clock, ExternalLink, Newspaper, Star } from "lucide-react";
import { dayLabel, formatStars, relativeTime, sourceStyle } from "../lib.js";

function NewsCard({ item }) {
  const displayTitle = item.title_zh || item.title;
  const isGithub = item.source_type === "github_trending";
  return (
    <a
      href={item.url}
      target="_blank"
      rel="noreferrer"
      className="group block rounded-lg border border-zinc-200 bg-white p-4 transition hover:border-zinc-300 hover:shadow-sm dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700"
    >
      <h3 className="text-[15px] font-medium leading-snug text-zinc-900 group-hover:text-teal-700 dark:text-zinc-100 dark:group-hover:text-teal-400">
        {displayTitle}
        <ExternalLink
          size={12}
          className="ml-1 inline opacity-0 transition group-hover:opacity-60"
        />
      </h3>
      {item.summary && (
        <p className="mt-1.5 text-sm leading-relaxed text-zinc-500 dark:text-zinc-400">
          {item.summary}
        </p>
      )}
      <div className="mt-2.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-zinc-400 dark:text-zinc-500">
        <span className={"rounded px-1.5 py-0.5 font-medium " + sourceStyle(item.source)}>
          {item.source}
        </span>
        {isGithub && item.stars != null && (
          <span className="flex items-center gap-1">
            <Star size={12} className="text-amber-500" />
            {formatStars(item.stars)}
          </span>
        )}
        {item.language && <span>{item.language}</span>}
        {item.topic && <span className="text-zinc-500 dark:text-zinc-400">{item.topic}</span>}
        {item.tags?.slice(0, 4).map((t) => (
          <span key={t}>#{t}</span>
        ))}
        <span className="ml-auto flex items-center gap-1">
          <Clock size={12} />
          {relativeTime(item.published_at || item.collected_at)}
        </span>
      </div>
    </a>
  );
}

function Skeleton() {
  return (
    <div className="space-y-2.5">
      {[...Array(6)].map((_, i) => (
        <div
          key={i}
          className="animate-pulse rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900"
        >
          <div className="h-4 w-3/4 rounded bg-zinc-100 dark:bg-zinc-800" />
          <div className="mt-3 h-3 w-1/2 rounded bg-zinc-100 dark:bg-zinc-800" />
        </div>
      ))}
    </div>
  );
}

export default function NewsList({ items, total, loading, error, onLoadMore }) {
  if (loading && items.length === 0) return <Skeleton />;
  if (error) {
    return (
      <div className="rounded-lg border border-zinc-200 bg-white p-10 text-center text-sm text-zinc-500 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-400">
        {error}
      </div>
    );
  }
  if (!items.length) {
    return (
      <div className="rounded-lg border border-dashed border-zinc-200 p-12 text-center dark:border-zinc-800">
        <Newspaper size={28} className="mx-auto text-zinc-300 dark:text-zinc-700" />
        <p className="mt-3 text-sm text-zinc-400">暂无新闻，爬虫会按小时自动抓取</p>
      </div>
    );
  }
  const groups = [];
  for (const item of items) {
    const label = dayLabel(item.published_at || item.collected_at);
    const last = groups[groups.length - 1];
    if (last && last.label === label) last.items.push(item);
    else groups.push({ label, items: [item] });
  }
  return (
    <div className="space-y-6">
      {groups.map((g) => (
        <section key={g.label}>
          <h2 className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-zinc-400">
            {g.label}
            <span className="h-px flex-1 bg-zinc-200 dark:bg-zinc-800" />
          </h2>
          <div className="space-y-2.5">
            {g.items.map((item) => (
              <NewsCard key={item.id} item={item} />
            ))}
          </div>
        </section>
      ))}
      {items.length < total && (
        <button
          onClick={onLoadMore}
          className="mx-auto flex items-center gap-1.5 rounded-full border border-zinc-200 px-4 py-2 text-sm text-zinc-600 transition hover:border-zinc-300 hover:text-zinc-900 dark:border-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-100"
        >
          加载更多（共 {total} 条）
        </button>
      )}
    </div>
  );
}
