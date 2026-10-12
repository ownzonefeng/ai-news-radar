export function relativeTime(iso) {
  if (!iso) return "";
  const then = parseUtc(iso);
  const minutes = Math.floor((Date.now() - then.getTime()) / 60000);
  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes} 分钟前`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} 小时前`;
  const day = Math.floor(hours / 24);
  if (day === 1) return "昨天";
  if (day < 7) return `${day} 天前`;
  return then.toLocaleDateString("zh-CN", { month: "numeric", day: "numeric" });
}

function sameDay(a, b) {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

export function dayLabel(iso) {
  const d = parseUtc(iso);
  const now = new Date();
  const yesterday = new Date();
  yesterday.setDate(now.getDate() - 1);
  if (sameDay(d, now)) return "今天";
  if (sameDay(d, yesterday)) return "昨天";
  return d.toLocaleDateString("zh-CN", { month: "long", day: "numeric", weekday: "short" });
}

export function formatStars(n) {
  if (n == null) return null;
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, "") + "k";
  return String(n);
}

export function formatFullTime(iso) {
  if (!iso) return "";
  const d = parseUtc(iso);
  return new Intl.DateTimeFormat("zh-CN", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(d);
}

function parseUtc(iso) {
  return new Date(iso.endsWith("Z") ? iso : iso + "Z");
}

const SOURCE_STYLES = {
  "机器之心": "bg-sky-100 text-sky-700 dark:bg-sky-950 dark:text-sky-300",
  "量子位": "bg-violet-100 text-violet-700 dark:bg-violet-950 dark:text-violet-300",
  "AI科技评论": "bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300",
  "TechCrunch AI": "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300",
  "VentureBeat AI": "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300",
  "Hacker News": "bg-orange-100 text-orange-700 dark:bg-orange-950 dark:text-orange-300",
  "GitHub Trending": "bg-zinc-900 text-zinc-100 dark:bg-zinc-100 dark:text-zinc-900",
};

export function sourceStyle(source) {
  return SOURCE_STYLES[source] || "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300";
}
