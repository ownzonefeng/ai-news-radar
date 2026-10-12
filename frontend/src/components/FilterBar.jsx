import { ChevronDown } from "lucide-react";

const TOPICS = [
  "模型与产品发布",
  "开源项目",
  "研究前沿",
  "行业与融资",
  "工程实践",
  "政策与监管",
];

const RANGES = [
  { label: "24 小时", value: 1 },
  { label: "3 天", value: 3 },
  { label: "7 天", value: 7 },
  { label: "30 天", value: 30 },
];

export default function FilterBar({
  topic,
  onTopic,
  days,
  onDays,
  source,
  onSource,
  counts,
  sources,
}) {
  const tabs = ["全部", ...TOPICS];
  return (
    <div className="space-y-3 pb-2 pt-6">
      <div className="flex items-center gap-2 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {tabs.map((t) => {
          const active = t === topic;
          const count = t === "全部" ? counts.total : counts.topics?.[t] ?? 0;
          return (
            <button
              key={t}
              onClick={() => onTopic(t)}
              className={
                "shrink-0 rounded-full border px-3.5 py-1.5 text-sm transition " +
                (active
                  ? "border-zinc-900 bg-zinc-900 text-white dark:border-zinc-100 dark:bg-zinc-100 dark:text-zinc-900"
                  : "border-zinc-200 bg-white text-zinc-600 hover:border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-400 dark:hover:border-zinc-700")
              }
            >
              {t}
              <span
                className={
                  "ml-1.5 text-xs " +
                  (active
                    ? "text-zinc-400 dark:text-zinc-500"
                    : "text-zinc-400 dark:text-zinc-600")
                }
              >
                {count}
              </span>
            </button>
          );
        })}
      </div>
      <div className="flex items-center justify-between gap-3">
        <div className="flex rounded-full border border-zinc-200 bg-zinc-100 p-0.5 dark:border-zinc-800 dark:bg-zinc-900">
          {RANGES.map((r) => (
            <button
              key={r.value}
              onClick={() => onDays(r.value)}
              className={
                "rounded-full px-3 py-1 text-xs transition " +
                (r.value === days
                  ? "bg-white text-zinc-900 shadow-sm dark:bg-zinc-700 dark:text-white"
                  : "text-zinc-500 dark:text-zinc-400")
              }
            >
              {r.label}
            </button>
          ))}
        </div>
        <label className="relative">
          <select
            value={source}
            onChange={(e) => onSource(e.target.value)}
            className="appearance-none rounded-full border border-zinc-200 bg-white py-1.5 pl-3 pr-8 text-xs text-zinc-600 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-400"
          >
            <option value="">全部来源</option>
            {sources.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <ChevronDown
            size={14}
            className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400"
          />
        </label>
      </div>
    </div>
  );
}
