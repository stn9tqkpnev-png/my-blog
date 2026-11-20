export const SITE_TITLE = 'Workbench Note';
export const SITE_DESCRIPTION = 'Workbench Noteへようこそ！ガジェットや技術、日々の記録を発信するブログです。';

export const CATEGORIES = [
  { name: 'スマートウォッチ', slug: 'smartwatch', tags: ['Amazfit', 'T-Rex 2', 'T-Rex 3', 'スマートウォッチ'] },
  { name: 'スマートホーム', slug: 'smarthome', tags: ['SESAME', 'スマートホーム'] },
  { name: 'アプリ', slug: 'app', tags: ['Androidアプリ', '音声入力', 'アプリ'] },
  { name: '買い物', slug: 'shopping', tags: ['AliExpress', '買い物'] },
];

export function getCategoryOf(tags: string[] | undefined) {
  const t = tags || [];
  for (const cat of CATEGORIES) {
    if (t.some(tag => cat.tags.includes(tag))) {
      return cat;
    }
  }
  return { name: 'その他', slug: 'other', tags: [] };
}
