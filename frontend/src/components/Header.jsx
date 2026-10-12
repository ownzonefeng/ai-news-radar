import { Github, Moon, Radar, RefreshCw, Sun, Users } from "lucide-react";
import { formatFullTime } from "../lib.js";

export default function Header({ dark, onToggleTheme, updatedAt, visitors }) {
  return (
    <header className="sticky top-0 z-20 border-b border-zinc-200 bg-white/80 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/80">
      <div className="mx-auto grid h-14 w-full max-w-3xl grid-cols-3 items-center px-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-white">
            <Radar size={18} />
          </div>
          <div>
            <h1 className="text-[15px] font-semibold leading-tight tracking-tight">AI 新闻雷达</h1>
            <p className="text-[11px] leading-tight text-zinc-400">AI News Radar</p>
          </div>
        </div>
        <div className="flex items-center justify-center gap-1.5 text-xs text-zinc-500 dark:text-zinc-400">
          <Users size={14} className="text-teal-600 dark:text-teal-400" />
          <span>
            你是该网站第 <span className="font-semibold text-zinc-900 dark:text-zinc-100">{visitors ?? 0}</span> 位访客
          </span>
        </div>
        <div className="flex items-center justify-end gap-3">
          {updatedAt && (
            <span className="hidden text-xs text-zinc-400 sm:block">
              <RefreshCw size={12} className="mr-1 inline" />
              {formatFullTime(updatedAt)}
            </span>
          )}
          <button
            onClick={onToggleTheme}
            aria-label="切换主题"
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 text-zinc-500 transition hover:border-zinc-300 hover:text-zinc-700 dark:border-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200"
          >
            {dark ? <Sun size={15} /> : <Moon size={15} />}
          </button>
          <a
            href="https://github.com/ownzonefeng/ai-news-radar"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub repository"
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 text-zinc-500 transition hover:border-zinc-300 hover:text-zinc-700 dark:border-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200"
          >
            <Github size={15} />
          </a>
        </div>
      </div>
    </header>
  );
}
