import { useEffect, useState } from "react";
import Header from "./components/Header.jsx";
import FilterBar from "./components/FilterBar.jsx";
import NewsList from "./components/NewsList.jsx";

export default function App() {
  const [topic, setTopic] = useState("全部");
  const [days, setDays] = useState(7);
  const [source, setSource] = useState("");
  const [page, setPage] = useState(1);
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [counts, setCounts] = useState({ total: 0, topics: {} });
  const [sources, setSources] = useState([]);
  const [meta, setMeta] = useState(null);
  const [visitors, setVisitors] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem("theme");
    if (saved) return saved === "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    const params = new URLSearchParams({ page: "1", page_size: "60" });
    if (days) params.set("days", String(days));
    if (topic !== "全部") params.set("topic", topic);
    if (source) params.set("source", source);
    fetch(`/api/news?${params}`)
      .then((r) => {
        if (!r.ok) throw new Error("bad status");
        return r.json();
      })
      .then((data) => {
        if (cancelled) return;
        setItems(data.items);
        setTotal(data.total);
        setPage(1);
      })
      .catch(() => {
        if (!cancelled) setError("加载失败，请稍后重试");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [topic, days, source]);

  useEffect(() => {
    const params = new URLSearchParams({ days: String(days) });
    fetch(`/api/topics?${params}`)
      .then((r) => r.json())
      .then(setCounts)
      .catch(() => {});
    fetch("/api/sources")
      .then((r) => r.json())
      .then((d) => setSources(d.sources))
      .catch(() => {});
    fetch("/api/meta")
      .then((r) => r.json())
      .then(setMeta)
      .catch(() => {});
  }, [days]);

  useEffect(() => {
    fetch("/api/visit")
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => d && setVisitors(d.visitors))
      .catch(() => {});
  }, []);

  useEffect(() => {
    const id = setInterval(() => {
      if (page !== 1) return;
      const params = new URLSearchParams({ page: "1", page_size: "60" });
      if (days) params.set("days", String(days));
      if (topic !== "全部") params.set("topic", topic);
      if (source) params.set("source", source);
      fetch(`/api/news?${params}`)
        .then((r) => (r.ok ? r.json() : null))
        .then((data) => {
          if (data) {
            setItems(data.items);
            setTotal(data.total);
          }
        })
        .catch(() => {});
    }, 15000);
    return () => clearInterval(id);
  }, [topic, days, source, page]);

  const loadMore = () => {
    const nextPage = page + 1;
    const params = new URLSearchParams({ page: String(nextPage), page_size: "60" });
    if (days) params.set("days", String(days));
    if (topic !== "全部") params.set("topic", topic);
    if (source) params.set("source", source);
    fetch(`/api/news?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setItems((prev) => [...prev, ...data.items]);
        setPage(nextPage);
      })
      .catch(() => {});
  };

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
        <Header dark={dark} onToggleTheme={() => setDark((v) => !v)} updatedAt={meta?.last_updated} visitors={visitors} />
      <main className="mx-auto w-full max-w-3xl px-4 pb-20">
        <FilterBar
          topic={topic}
          onTopic={setTopic}
          days={days}
          onDays={setDays}
          source={source}
          onSource={setSource}
          counts={counts}
          sources={sources}
        />
        <NewsList items={items} total={total} loading={loading} error={error} onLoadMore={loadMore} />
      </main>
      <footer className="border-t border-zinc-200 py-6 text-center text-xs text-zinc-400 dark:border-zinc-800 dark:text-zinc-600">
        © 2026 AI News Radar · wefeng486@gmail.com
        <div className="mt-1 flex items-center justify-center gap-1.5">
          <a
            href="https://github.com/ownzonefeng/ai-news-radar"
            target="_blank"
            rel="noopener noreferrer"
            className="underline decoration-zinc-300 underline-offset-2 transition hover:text-zinc-600 dark:hover:text-zinc-300"
          >
            开源仓库
          </a>
          <span>·</span>
          <span>MIT License</span>
          <span>·</span>
          <span>本项目由 Codex 辅助生成</span>
        </div>
      </footer>
    </div>
  );
}
