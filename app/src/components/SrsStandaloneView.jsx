/**
 * SrsStandaloneView — Màn hình Ôn tập Giãn Cách SRS riêng biệt.
 * Được điều hướng khi bấm vào ô "ĐẾN HẠN CẦN ÔN" trên Dashboard.
 */
import { ArrowLeft, Brain } from 'lucide-react';
import Tab3Srs from '../tabs/Tab3Srs.jsx';
import { useApp } from '../lib/store.jsx';
import { Button, Card } from './ui.jsx';

export default function SrsStandaloneView() {
  const { openDashboard, srsParams, lesson } = useApp();

  return (
    <div className="space-y-4">
      {/* Header tối giản */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" size="sm" onClick={openDashboard} className="font-extrabold text-[var(--color-duo-gray)] hover:text-[var(--color-duo-ink)]">
          <ArrowLeft className="h-4 w-4" />
          Dashboard
        </Button>
        <div className="flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-xl bg-[var(--color-duo-green-light)] text-[var(--color-duo-green-dark)]">
            <Brain className="h-4 w-4" />
          </span>
          <span className="text-sm font-black uppercase tracking-wider text-[var(--color-duo-ink)]">
            Ôn tập giãn cách
          </span>
        </div>
      </div>

      {/* Trạm ôn tập toàn cục với 2 chế độ gõ từ */}
      <Tab3Srs
        globalMode={true}
        lesson={lesson}
        initialFilter={srsParams?.filter || 'due'}
        initialThemeId={srsParams?.themeId || null}
        initialLessonId={srsParams?.lessonId || null}
      />
    </div>
  );
}
